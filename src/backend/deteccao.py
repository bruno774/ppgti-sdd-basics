"""Detecção de entidades pessoais e sensíveis em texto normalizado."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.backend.categorias import CategoriaEntidade, Catalogo
from src.backend.entrada_multicanal import DocumentoOrigem
from src.backend.regras_deteccao import AplicadorRegrasDeteccao


OrigemDeteccao = Literal["regra", "modelo", "combinado"]


@dataclass(frozen=True)
class EntidadeDetectada:
    """Representa uma entidade detectada no texto."""

    id: str
    tipo: str
    inicio: int
    fim: int
    confianca: float
    origem: OrigemDeteccao
    sensivel: bool

    def __post_init__(self):
        if not (0.0 <= self.confianca <= 1.0):
            raise ValueError(f"Confiança deve estar entre 0.0 e 1.0, recebido {self.confianca}")
        if self.inicio >= self.fim:
            raise ValueError(f"Intervalo inválido: início={self.inicio} deve ser menor que fim={self.fim}")


class DetectorEntidades:
    """Orquestra a detecção de entidades em texto normalizado."""

    LIMIAR_SENSIVEL = 0.75
    LIMIAR_PADRAO = 0.5

    def __init__(self, catalogo: Catalogo | None = None):
        self.catalogo = catalogo or Catalogo()
        self._aplicador = AplicadorRegrasDeteccao(self.catalogo)
        self._contador_por_tipo: dict[str, int] = {}

    def detectar(self, documento: DocumentoOrigem) -> list[EntidadeDetectada]:
        """Detecta todas as entidades no texto do documento."""
        self._contador_por_tipo.clear()
        deteccoes = self._aplicador.executar(documento.texto)

        entidades: list[EntidadeDetectada] = []
        for det in deteccoes:
            categoria = self._obter_categoria(det["tipo"])
            if categoria is None:
                continue

            limiar = self.LIMIAR_SENSIVEL if categoria.sensivel else self.LIMIAR_PADRAO
            if det["confianca"] < limiar:
                continue

            indice = self._contador_por_tipo.get(det["tipo"], 0) + 1
            self._contador_por_tipo[det["tipo"]] = indice
            id_entidade = f"{categoria.prefixo_marcador}{indice}"

            entidade = EntidadeDetectada(
                id=id_entidade,
                tipo=det["tipo"],
                inicio=det["inicio"],
                fim=det["fim"],
                confianca=det["confianca"],
                origem=det["origem"],
                sensivel=categoria.sensivel,
            )
            entidades.append(entidade)

        entidades.sort(key=lambda e: (e.inicio, e.tipo))
        return entidades

    def _obter_categoria(self, tipo: str) -> CategoriaEntidade | None:
        """Busca categoria pelo tipo canônico."""
        for cat in self.catalogo.categorias_disponiveis():
            if cat.tipo_canonico == tipo:
                return cat
        return None
