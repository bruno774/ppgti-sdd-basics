"""Perfil ativo e seleção de categorias pelo operador antes do processamento."""

from typing import Literal

from pydantic import BaseModel

from src.backend.categorias import Catalogo

Perfil = Literal["operador", "gestor", "suporte"]

PERFIL_PADRAO: Perfil = "operador"


class SelecaoCategorias(BaseModel):
    """Estado de seleção de categorias em uma execução: perfil, seleção e catálogo vigente."""

    perfil: Perfil
    categorias_selecionadas: list[str]
    categorias_disponiveis: list[str]


class SessaoOperador:
    """Sessão de trabalho com perfil ativo, catálogo vigente e categorias selecionadas."""

    def __init__(self, catalogo: Catalogo | None = None) -> None:
        self._perfil: Perfil = PERFIL_PADRAO
        self._catalogo = catalogo if catalogo is not None else Catalogo()
        self._categorias_selecionadas: list[str] = []

    @property
    def perfil(self) -> Perfil:
        """Perfil atualmente ativo na sessão."""
        return self._perfil

    def trocar_perfil(self, novo_perfil: Perfil) -> None:
        """Ativa explicitamente um novo perfil (operador, gestor ou suporte)."""
        self._perfil = novo_perfil

    def categorias_disponiveis(self) -> list[str]:
        """Tipos canônicos de todas as categorias do catálogo, padrão e customizadas."""
        return [categoria.tipo_canonico for categoria in self._catalogo.categorias_disponiveis()]

    def selecionar_categorias(self, tipos_canonicos: list[str]) -> None:
        """Define as categorias selecionadas para a execução corrente."""
        disponiveis = set(self.categorias_disponiveis())
        tipos_desconhecidos = [tipo for tipo in tipos_canonicos if tipo not in disponiveis]
        if tipos_desconhecidos:
            raise ValueError(f"Categorias desconhecidas no catalogo: {tipos_desconhecidos}.")
        self._categorias_selecionadas = list(tipos_canonicos)

    def selecao_atual(self) -> SelecaoCategorias:
        """Retorna o estado de seleção corrente como contrato de dados."""
        return SelecaoCategorias(
            perfil=self._perfil,
            categorias_selecionadas=list(self._categorias_selecionadas),
            categorias_disponiveis=self.categorias_disponiveis(),
        )
