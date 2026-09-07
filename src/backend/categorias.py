"""Modelagem do catálogo de categorias de entidades (padrão e customizadas)."""

from typing import Literal

from pydantic import BaseModel, field_validator

OrigemCategoria = Literal["padrao", "customizada"]


class CategoriaError(Exception):
    """Erro base para operações sobre o catálogo de categorias."""


class CategoriaConflitanteError(CategoriaError):
    """Erro ao cadastrar uma categoria cujo tipo ou prefixo já existe no catálogo."""


class CategoriaPadraoNaoRemovivelError(CategoriaError):
    """Erro ao tentar remover uma categoria de origem padrão do catálogo."""


class CategoriaNaoEncontradaError(CategoriaError):
    """Erro ao tentar remover uma categoria que não existe no catálogo."""


class CategoriaEntidade(BaseModel):
    """Categoria de entidade do catálogo, com tipo canônico e prefixo de marcador."""

    tipo_canonico: str
    prefixo_marcador: str
    sensivel: bool
    origem: OrigemCategoria

    @field_validator("tipo_canonico")
    @classmethod
    def _validar_tipo_canonico(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O tipo canonico nao pode ser vazio.")
        if valor != valor.upper():
            raise ValueError("O tipo canonico deve estar em maiusculas.")
        return valor

    @field_validator("prefixo_marcador")
    @classmethod
    def _validar_prefixo_marcador(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O prefixo do marcador nao pode ser vazio.")
        if valor != valor.lower():
            raise ValueError("O prefixo do marcador deve estar em minusculas.")
        return valor


CATALOGO_PADRAO: tuple[CategoriaEntidade, ...] = (
    CategoriaEntidade(tipo_canonico="NOME", prefixo_marcador="nom", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="CPF", prefixo_marcador="cpf", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="RG", prefixo_marcador="rg", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="ENDERECO", prefixo_marcador="end", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="EMAIL", prefixo_marcador="ema", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="TELEFONE", prefixo_marcador="tel", sensivel=False, origem="padrao"),
    CategoriaEntidade(tipo_canonico="CID_DOENCA", prefixo_marcador="cid", sensivel=True, origem="padrao"),
    CategoriaEntidade(tipo_canonico="RELIGIAO", prefixo_marcador="rel", sensivel=True, origem="padrao"),
    CategoriaEntidade(tipo_canonico="GENERO_SEXUAL", prefixo_marcador="gen", sensivel=True, origem="padrao"),
    CategoriaEntidade(tipo_canonico="COR_PELE", prefixo_marcador="cor", sensivel=True, origem="padrao"),
    CategoriaEntidade(tipo_canonico="CLASSE_SOCIAL", prefixo_marcador="cls", sensivel=True, origem="padrao"),
)


def validar_unicidade(
    catalogo_existente: list[CategoriaEntidade],
    nova_categoria: CategoriaEntidade,
) -> None:
    """Impede que uma nova categoria colida com o tipo ou o prefixo de outra já existente."""
    for categoria in catalogo_existente:
        if categoria.tipo_canonico == nova_categoria.tipo_canonico:
            raise CategoriaConflitanteError(
                f"Ja existe uma categoria com o tipo canonico '{nova_categoria.tipo_canonico}'."
            )
        if categoria.prefixo_marcador == nova_categoria.prefixo_marcador:
            raise CategoriaConflitanteError(
                f"Ja existe uma categoria com o prefixo de marcador '{nova_categoria.prefixo_marcador}'."
            )


class Catalogo:
    """Catálogo de categorias vigente, com categorias padrão sempre presentes."""

    def __init__(self) -> None:
        self._categorias: list[CategoriaEntidade] = list(CATALOGO_PADRAO)

    def categorias_disponiveis(self) -> list[CategoriaEntidade]:
        """Retorna todas as categorias do catálogo (padrão e customizadas)."""
        return list(self._categorias)

    def cadastrar_categoria_customizada(self, categoria: CategoriaEntidade) -> None:
        """Adiciona uma categoria customizada, validando unicidade de tipo e prefixo."""
        if categoria.origem != "customizada":
            raise CategoriaError("Somente categorias de origem 'customizada' podem ser cadastradas.")
        validar_unicidade(self._categorias, categoria)
        self._categorias.append(categoria)

    def remover_categoria(self, tipo_canonico: str) -> None:
        """Remove uma categoria customizada; rejeita a remoção de categorias padrão."""
        for categoria in self._categorias:
            if categoria.tipo_canonico == tipo_canonico:
                if categoria.origem == "padrao":
                    raise CategoriaPadraoNaoRemovivelError(
                        f"A categoria padrao '{tipo_canonico}' nao pode ser removida do catalogo."
                    )
                self._categorias.remove(categoria)
                return
        raise CategoriaNaoEncontradaError(f"Categoria '{tipo_canonico}' nao encontrada no catalogo.")
