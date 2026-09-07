import pytest

from src.backend.categorias import CategoriaEntidade
from src.backend.selecao import SelecaoCategorias, SessaoOperador


def test_selecao_categorias_model_valida_e_serializa():
    selecao = SelecaoCategorias(
        perfil="operador",
        categorias_selecionadas=["NOME", "CPF"],
        categorias_disponiveis=["NOME", "CPF", "RG"],
    )

    dados = selecao.model_dump()

    assert dados["perfil"] == "operador"
    assert dados["categorias_selecionadas"] == ["NOME", "CPF"]
    assert SelecaoCategorias.model_validate(dados) == selecao


def test_nova_sessao_assume_perfil_operador_por_padrao():
    sessao = SessaoOperador()

    assert sessao.perfil == "operador"


def test_ausencia_de_troca_nunca_ativa_perfil_elevado():
    sessao = SessaoOperador()

    sessao.selecionar_categorias(["NOME"])

    assert sessao.perfil == "operador"


def test_troca_explicita_de_perfil_funciona():
    sessao = SessaoOperador()

    sessao.trocar_perfil("gestor")
    assert sessao.perfil == "gestor"

    sessao.trocar_perfil("suporte")
    assert sessao.perfil == "suporte"


def test_categorias_disponiveis_sempre_inclui_categorias_padrao():
    sessao = SessaoOperador()
    sessao.selecionar_categorias(["NOME"])

    disponiveis = set(sessao.categorias_disponiveis())

    assert {"NOME", "CPF", "RG", "ENDERECO", "EMAIL", "TELEFONE"}.issubset(disponiveis)
    assert "CID_DOENCA" in disponiveis


def test_categorias_disponiveis_inclui_categoria_customizada_cadastrada():
    sessao = SessaoOperador()
    categoria_customizada = CategoriaEntidade(
        tipo_canonico="IDENTIFICADOR_INTERNO", prefixo_marcador="idi", sensivel=False, origem="customizada"
    )
    sessao._catalogo.cadastrar_categoria_customizada(categoria_customizada)

    assert "IDENTIFICADOR_INTERNO" in sessao.categorias_disponiveis()


def test_selecionar_categoria_desconhecida_levanta_erro():
    sessao = SessaoOperador()

    with pytest.raises(ValueError):
        sessao.selecionar_categorias(["TIPO_QUE_NAO_EXISTE"])
