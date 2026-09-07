import pytest
from pydantic import ValidationError

from src.backend.categorias import (
    CATALOGO_PADRAO,
    Catalogo,
    CategoriaConflitanteError,
    CategoriaEntidade,
    CategoriaNaoEncontradaError,
    CategoriaPadraoNaoRemovivelError,
    validar_unicidade,
)

TIPOS_PADRAO_ESPERADOS = {
    "NOME",
    "CPF",
    "RG",
    "ENDERECO",
    "EMAIL",
    "TELEFONE",
    "CID_DOENCA",
    "RELIGIAO",
    "GENERO_SEXUAL",
    "COR_PELE",
    "CLASSE_SOCIAL",
}


def test_categoria_entidade_rejects_empty_tipo_canonico():
    with pytest.raises(ValidationError):
        CategoriaEntidade(tipo_canonico="", prefixo_marcador="nom", sensivel=False, origem="padrao")


def test_categoria_entidade_rejects_empty_prefixo_marcador():
    with pytest.raises(ValidationError):
        CategoriaEntidade(tipo_canonico="NOME", prefixo_marcador="", sensivel=False, origem="padrao")


def test_categoria_entidade_rejects_lowercase_tipo_canonico():
    with pytest.raises(ValidationError):
        CategoriaEntidade(tipo_canonico="nome", prefixo_marcador="nom", sensivel=False, origem="padrao")


def test_categoria_entidade_rejects_uppercase_prefixo_marcador():
    with pytest.raises(ValidationError):
        CategoriaEntidade(tipo_canonico="NOME", prefixo_marcador="NOM", sensivel=False, origem="padrao")


def test_catalogo_padrao_contem_todos_os_tipos_com_origem_padrao():
    tipos_encontrados = {categoria.tipo_canonico for categoria in CATALOGO_PADRAO}
    assert tipos_encontrados == TIPOS_PADRAO_ESPERADOS
    assert all(categoria.origem == "padrao" for categoria in CATALOGO_PADRAO)


def test_validar_unicidade_detecta_colisao_de_tipo_canonico():
    categoria_conflitante = CategoriaEntidade(
        tipo_canonico="NOME", prefixo_marcador="nm2", sensivel=False, origem="customizada"
    )
    with pytest.raises(CategoriaConflitanteError):
        validar_unicidade(list(CATALOGO_PADRAO), categoria_conflitante)


def test_validar_unicidade_detecta_colisao_de_prefixo_marcador():
    categoria_conflitante = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="nom", sensivel=False, origem="customizada"
    )
    with pytest.raises(CategoriaConflitanteError):
        validar_unicidade(list(CATALOGO_PADRAO), categoria_conflitante)


def test_validar_unicidade_aceita_categoria_sem_colisao():
    categoria_valida = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )
    validar_unicidade(list(CATALOGO_PADRAO), categoria_valida)


def test_cadastrar_categoria_customizada_valida():
    catalogo = Catalogo()
    categoria_valida = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )

    catalogo.cadastrar_categoria_customizada(categoria_valida)

    tipos_disponiveis = {categoria.tipo_canonico for categoria in catalogo.categorias_disponiveis()}
    assert "IDENTIFICADOR_INTERNO" in tipos_disponiveis


def test_cadastrar_categoria_customizada_rejeita_prefixo_conflitante_com_padrao():
    catalogo = Catalogo()
    categoria_conflitante = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="nom", sensivel=False, origem="customizada"
    )

    with pytest.raises(CategoriaConflitanteError):
        catalogo.cadastrar_categoria_customizada(categoria_conflitante)


def test_cadastrar_categoria_customizada_rejeita_prefixo_conflitante_com_outra_customizada():
    catalogo = Catalogo()
    primeira_categoria = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )
    catalogo.cadastrar_categoria_customizada(primeira_categoria)
    categoria_conflitante = CategoriaEntidade(
        tipo_canonico="OUTRO_TIPO_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )

    with pytest.raises(CategoriaConflitanteError):
        catalogo.cadastrar_categoria_customizada(categoria_conflitante)


def test_remover_categoria_padrao_e_rejeitada():
    catalogo = Catalogo()

    with pytest.raises(CategoriaPadraoNaoRemovivelError):
        catalogo.remover_categoria("NOME")

    tipos_disponiveis = {categoria.tipo_canonico for categoria in catalogo.categorias_disponiveis()}
    assert "NOME" in tipos_disponiveis


def test_remover_categoria_customizada_funciona():
    catalogo = Catalogo()
    categoria_customizada = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )
    catalogo.cadastrar_categoria_customizada(categoria_customizada)

    catalogo.remover_categoria("IDENTIFICADOR_INTERNO")

    tipos_disponiveis = {categoria.tipo_canonico for categoria in catalogo.categorias_disponiveis()}
    assert "IDENTIFICADOR_INTERNO" not in tipos_disponiveis


def test_remover_categoria_inexistente_levanta_erro():
    catalogo = Catalogo()

    with pytest.raises(CategoriaNaoEncontradaError):
        catalogo.remover_categoria("TIPO_QUE_NAO_EXISTE")
