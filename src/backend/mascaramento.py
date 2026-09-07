from __future__ import annotations

from collections import defaultdict

from pydantic import BaseModel

from src.backend.categorias import Catalogo


class EntidadeDetectada(BaseModel):
    """Entidade detectada com tipo, offsets e confiança."""

    tipo: str
    inicio: int
    fim: int
    texto: str
    confianca: float
    identificador: str
    indice: int | None = None


class SobreposicaoEntidadeError(ValueError):
    """Erro ao tentar mascarar entidades que se sobrepõem parcialmente."""


class ResultadoMascaramento(dict):
    """Dicionário com suporte a consulta por substring no texto mascarado."""

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item in self.get("texto", "")
        return super().__contains__(item)


def _normalizar_texto(texto: str) -> str:
    return " ".join(texto.strip().lower().split())


def atribuir_indices_entidades(entidades: list[EntidadeDetectada]) -> list[EntidadeDetectada]:
    """Atribui índices estáveis por tipo, reaproveitando índice para a mesma entidade."""
    contadores_por_tipo: dict[str, int] = defaultdict(int)
    indice_por_chave: dict[tuple[str, str], int] = {}
    resultado: list[EntidadeDetectada] = []

    for entidade in entidades:
        chave = (entidade.tipo, _normalizar_texto(entidade.texto))
        if not chave[1]:
            continue
        if chave not in indice_por_chave:
            contadores_por_tipo[entidade.tipo] += 1
            indice_por_chave[chave] = contadores_por_tipo[entidade.tipo]
        entidade.indice = indice_por_chave[chave]
        resultado.append(entidade)

    return resultado


def validar_sobreposicao(entidades: list[EntidadeDetectada]) -> None:
    """Valida sobreposição: total é ignorada, parcial é rejeitada."""
    entidades_ordenadas = sorted(entidades, key=lambda item: (item.inicio, item.fim))
    for indice_atual in range(len(entidades_ordenadas) - 1):
        atual = entidades_ordenadas[indice_atual]
        proximo = entidades_ordenadas[indice_atual + 1]
        if atual.inicio == proximo.inicio and atual.fim == proximo.fim:
            continue
        if atual.fim > proximo.inicio:
            raise SobreposicaoEntidadeError("sobreposicao parcial entre entidades detectadas.")


def aplicar_mascaramento(
    texto: str,
    entidades: list[EntidadeDetectada],
    *,
    categorias_selecionadas: list[str],
    catalogo: Catalogo,
) -> ResultadoMascaramento:
    """Aplica substituição por marcadores conforme tipos selecionados."""
    selecionadas = set(categorias_selecionadas)
    entidades_validas = [entidade for entidade in atribuir_indices_entidades(entidades) if entidade.tipo in selecionadas]
    validar_sobreposicao(entidades_validas)

    entidades_ordenadas = sorted(entidades_validas, key=lambda item: (item.inicio, item.fim))
    prefixos: dict[str, str] = {
        categoria.tipo_canonico: categoria.prefixo_marcador
        for categoria in catalogo.categorias_disponiveis()
        if categoria.tipo_canonico in selecionadas
    }

    contagem: dict[str, int] = defaultdict(int)
    segmentos: list[str] = []
    cursor = 0

    for entidade in entidades_ordenadas:
        tipo = entidade.tipo
        if entidade.inicio < cursor:
            continue
        segmentos.append(texto[cursor: entidade.inicio])
        prefixo = prefixos.get(tipo, tipo.lower())
        contagem[tipo] += 1
        marcador = f"{prefixo}{entidade.indice or contagem[tipo]}"
        segmentos.append(marcador)
        cursor = entidade.fim

    segmentos.append(texto[cursor:])
    resultado = "".join(segmentos)

    total_por_tipo = {tipo: sum(1 for entidade in entidades_validas if entidade.tipo == tipo) for tipo in sorted({e.tipo for e in entidades_validas})}
    return ResultadoMascaramento({"texto": resultado, "contagem_por_tipo": total_por_tipo})
