"""Gerenciamento de execuções de anonimização."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from src.backend.entrada_multicanal import DocumentoOrigem


@dataclass
class ExecucaoAnonimizacao:
    """Rastreia uma execução de anonimização."""

    id_origem: str = ""
    categorias_selecionadas: list[str] = None
    canal_entrada: str = ""
    perfil_ativo: str = "operador"

    def __post_init__(self):
        if self.categorias_selecionadas is None:
            self.categorias_selecionadas = []


class GerenciadorOrigens:
    """Gerencia retenção de textos de origem com expiração."""

    def __init__(self, ttl_segundos: int = 3600):
        self.ttl = ttl_segundos
        self._textos: dict[str, str] = {}

    def reter_texto(self, documento: DocumentoOrigem) -> str:
        """Retem um texto e retorna seu ID."""
        id_origem = str(uuid4())
        self._textos[id_origem] = documento.texto
        return id_origem
