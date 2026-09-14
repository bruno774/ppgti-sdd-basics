"""DetecÃ§Ã£o de entidades com TDD."""

import re
from dataclasses import dataclass
from typing import Literal

from src.backend.categorias import CategoriaEntidade, Catalogo
from src.backend.entrada_multicanal import DocumentoOrigem


OrigemDeteccao = Literal["regra", "modelo", "combinado"]


@dataclass(frozen=True)
class EntidadeDetectada:
    """Entidade detectada no texto."""

    id: str
    tipo: str
    inicio: int
    fim: int
    confianca: float
    origem: OrigemDeteccao
    sensivel: bool
    requer_revisao: bool = False

    def __post_init__(self) -> None:
        if not (0.0 <= self.confianca <= 1.0):
            raise ValueError(f"ConfianÃ§a deve estar entre 0.0 e 1.0, recebido {self.confianca}")
        if self.inicio >= self.fim:
            raise ValueError(f"Intervalo invÃ¡lido: inÃ­cio={self.inicio} deve ser menor que fim={self.fim}")


class DetectorEntidades:
    """Detector de entidades."""

    LIMIAR_PADRAO = 0.5
    LIMIAR_SENSIVEL = 0.75

    def __init__(self, catalogo: Catalogo | None = None) -> None:
        self.catalogo = catalogo or Catalogo()
        self._contador_por_tipo: dict[str, int] = {}

    def detectar(self, documento: DocumentoOrigem) -> list[EntidadeDetectada]:
        """Detecta entidades no texto."""
        self._contador_por_tipo.clear()
        entidades: list[EntidadeDetectada] = []

        # Detectar CPF
        entidades.extend(self._detectar_cpf(documento.texto))
        # Detectar EMAIL
        entidades.extend(self._detectar_email(documento.texto))
        # Detectar TELEFONE
        entidades.extend(self._detectar_telefone(documento.texto))
        # Detectar RG
        entidades.extend(self._detectar_rg(documento.texto))
        # Detectar ENDERECO
        entidades.extend(self._detectar_endereco(documento.texto))
        # Detectar NOME
        entidades.extend(self._detectar_nome(documento.texto))
        # Detectar CID_DOENCA
        entidades.extend(self._detectar_cid_doenca(documento.texto))
        # Detectar RELIGIAO
        entidades.extend(self._detectar_religiao(documento.texto))
        # Detectar GENERO_SEXUAL
        entidades.extend(self._detectar_genero_sexual(documento.texto))
        # Detectar COR_PELE
        entidades.extend(self._detectar_cor_pele(documento.texto))
        # Detectar CLASSE_SOCIAL
        entidades.extend(self._detectar_classe_social(documento.texto))

        # Filtrar por confianÃ§a, gerar IDs, ordenar
        resultado = []
        for ent in entidades:
            categoria = self._obter_categoria(ent.tipo)
            if categoria is None:
                continue

            limiar = self.LIMIAR_SENSIVEL if categoria.sensivel else self.LIMIAR_PADRAO

            # Se Ã© sensÃ­vel e confianÃ§a baixa, marcar para revisÃ£o
            if categoria.sensivel and ent.confianca < limiar:
                object.__setattr__(ent, 'requer_revisao', True)
            elif not categoria.sensivel and ent.confianca < limiar:
                continue

            # Gerar ID estÃ¡vel
            indice = self._contador_por_tipo.get(ent.tipo, 0) + 1
            self._contador_por_tipo[ent.tipo] = indice
            id_entidade = f"{categoria.prefixo_marcador}{indice}"

            # Criar nova instÃ¢ncia com ID atualizado
            ent_com_id = EntidadeDetectada(
                id=id_entidade,
                tipo=ent.tipo,
                inicio=ent.inicio,
                fim=ent.fim,
                confianca=ent.confianca,
                origem=ent.origem,
                sensivel=ent.sensivel,
                requer_revisao=ent.requer_revisao,
            )
            resultado.append(ent_com_id)

        resultado.sort(key=lambda e: (e.inicio, e.tipo))
        return resultado

    def _detectar_cpf(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta CPF em formato 000.000.000-00 ou 00000000000."""
        deteccoes: list[EntidadeDetectada] = []

        # Formato com pontuaÃ§Ã£o
        padrao_formatado = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        for match in re.finditer(padrao_formatado, texto):
            ent = EntidadeDetectada(
                id="cpf_temp",
                tipo="CPF",
                inicio=match.start(),
                fim=match.end(),
                confianca=0.95,
                origem="regra",
                sensivel=False,
            )
            deteccoes.append(ent)

        # Formato sem pontuaÃ§Ã£o
        padrao_simples = r"\d{11}"
        for match in re.finditer(padrao_simples, texto):
            # Evitar duplicaÃ§Ã£o
            texto_match = texto[match.start() : match.end()]
            if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto_match):
                ent = EntidadeDetectada(
                    id="cpf_temp",
                    tipo="CPF",
                    inicio=match.start(),
                    fim=match.end(),
                    confianca=0.80,
                    origem="regra",
                    sensivel=False,
                )
                deteccoes.append(ent)

        return deteccoes

    def _detectar_email(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta endereÃ§o de email."""
        deteccoes: list[EntidadeDetectada] = []
        padrao = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        for match in re.finditer(padrao, texto):
            ent = EntidadeDetectada(
                id="ema_temp",
                tipo="EMAIL",
                inicio=match.start(),
                fim=match.end(),
                confianca=0.95,
                origem="regra",
                sensivel=False,
            )
            deteccoes.append(ent)

        return deteccoes

    def _detectar_telefone(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta telefone com DDD/DDI."""
        deteccoes: list[EntidadeDetectada] = []
        padrao = r"(?:\+\d{1,3}\s)?(?:\(\d{2}\)\s?)?\d{4,5}-?\d{4}"

        for match in re.finditer(padrao, texto):
            ent = EntidadeDetectada(
                id="tel_temp",
                tipo="TELEFONE",
                inicio=match.start(),
                fim=match.end(),
                confianca=0.85,
                origem="regra",
                sensivel=False,
            )
            deteccoes.append(ent)

        return deteccoes

    def _detectar_rg(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta RG (7-9 dÃ­gitos com letra)."""
        deteccoes: list[EntidadeDetectada] = []
        padrao = r"\d{7,9}[-\s]?[a-zA-Z]?"

        for match in re.finditer(padrao, texto):
            texto_match = texto[match.start() : match.end()].strip()
            if re.match(r"^\d{7,9}$", texto_match) or re.match(r"^\d{7,9}[-\s][a-zA-Z]$", texto_match):
                ent = EntidadeDetectada(
                    id="rg_temp",
                    tipo="RG",
                    inicio=match.start(),
                    fim=match.end(),
                    confianca=0.70,
                    origem="regra",
                    sensivel=False,
                )
                deteccoes.append(ent)

        return deteccoes

    def _detectar_endereco(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta endereço."""
        deteccoes: list[EntidadeDetectada] = []
        padrao = r"(?:Rua|Avenida|Av|Travessa|Praça)\s+[A-Z][a-záéíóúãõç\s]+(?:,?\s*\d+)?"
        for match in re.finditer(padrao, texto, re.IGNORECASE):
            if len(match.group()) > 10:
                ent = EntidadeDetectada(
                    id="end_temp", tipo="ENDERECO", origem="regra", sensivel=False,
                    inicio=match.start(), fim=match.end(), confianca=0.75
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_nome(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta nome próprio."""
        deteccoes: list[EntidadeDetectada] = []
        padrao = r"\b(?:[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+){1,3})\b"
        for match in re.finditer(padrao, texto):
            palavras = match.group().split()
            if len(palavras) >= 2 and len(match.group()) >= 6:
                confianca = min(0.6 + (len(palavras) * 0.1), 0.85)
                ent = EntidadeDetectada(
                    id="nom_temp", tipo="NOME", origem="regra", sensivel=False,
                    inicio=match.start(), fim=match.end(), confianca=confianca
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_cid_doenca(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta doença (tipo sensível)."""
        deteccoes: list[EntidadeDetectada] = []
        doencas = {"diabetes": 0.90, "hipertensão": 0.90, "gripe": 0.85, "covid": 0.95, "câncer": 0.95}
        for doenca, conf in doencas.items():
            padrao = rf"\b{re.escape(doenca)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                ent = EntidadeDetectada(
                    id="cid_temp", tipo="CID_DOENCA", origem="regra", sensivel=True,
                    inicio=match.start(), fim=match.end(), confianca=conf
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_religiao(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta religião (tipo sensível)."""
        deteccoes: list[EntidadeDetectada] = []
        religioes = {"católica": 0.90, "evangélica": 0.90, "islâmica": 0.90, "judaica": 0.90}
        for religiao, conf in religioes.items():
            padrao = rf"\b{re.escape(religiao)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                ent = EntidadeDetectada(
                    id="rel_temp", tipo="RELIGIAO", origem="regra", sensivel=True,
                    inicio=match.start(), fim=match.end(), confianca=conf
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_genero_sexual(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta orientação sexual (tipo sensível)."""
        deteccoes: list[EntidadeDetectada] = []
        orientacoes = {"homossexual": 0.95, "heterossexual": 0.95, "bissexual": 0.95, "lésbica": 0.95, "gay": 0.85, "LGBT": 0.80}
        for orient, conf in orientacoes.items():
            padrao = rf"\b{re.escape(orient)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                ent = EntidadeDetectada(
                    id="gen_temp", tipo="GENERO_SEXUAL", origem="regra", sensivel=True,
                    inicio=match.start(), fim=match.end(), confianca=conf
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_cor_pele(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta cor/raça (tipo sensível)."""
        deteccoes: list[EntidadeDetectada] = []
        cores = {"branco": 0.85, "negro": 0.90, "preto": 0.85, "pardo": 0.85, "parda": 0.85, "moreno": 0.70, "afro": 0.90}
        for cor, conf in cores.items():
            padrao = rf"\b{re.escape(cor)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                ent = EntidadeDetectada(
                    id="cor_temp", tipo="COR_PELE", origem="regra", sensivel=True,
                    inicio=match.start(), fim=match.end(), confianca=conf
                )
                deteccoes.append(ent)
        return deteccoes

    def _detectar_classe_social(self, texto: str) -> list[EntidadeDetectada]:
        """Detecta classe social (tipo sensível)."""
        deteccoes: list[EntidadeDetectada] = []
        classes = {"pobre": 0.80, "carente": 0.75, "abastado": 0.80, "classe média": 0.70, "baixa renda": 0.85}
        for cls, conf in classes.items():
            padrao = rf"\b{re.escape(cls)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                ent = EntidadeDetectada(
                    id="cls_temp", tipo="CLASSE_SOCIAL", origem="regra", sensivel=True,
                    inicio=match.start(), fim=match.end(), confianca=conf
                )
                deteccoes.append(ent)
        return deteccoes

    def _obter_categoria(self, tipo: str) -> CategoriaEntidade | None:
        """Busca categoria pelo tipo."""
        for cat in self.catalogo.categorias_disponiveis():
            if cat.tipo_canonico == tipo:
                return cat
        return None




