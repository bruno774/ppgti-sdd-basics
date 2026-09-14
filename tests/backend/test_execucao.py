"""Testes para gerenciamento de execuções e retenção de origem."""

from src.backend.execucao import ExecucaoAnonimizacao, GerenciadorOrigens
from src.backend.entrada_multicanal import criar_documento_texto


def test_execucao_anonimizacao_pode_ser_criada():
    """ExecucaoAnonimizacao pode ser instanciada com parâmetros."""
    exec_anon = ExecucaoAnonimizacao(
        id_origem="orig-123",
        categorias_selecionadas=["NOME", "CPF"],
        canal_entrada="pdf",
        perfil_ativo="operador",
    )

    assert exec_anon.id_origem == "orig-123"
    assert exec_anon.categorias_selecionadas == ["NOME", "CPF"]
    assert exec_anon.canal_entrada == "pdf"
    assert exec_anon.perfil_ativo == "operador"


def test_gerenciador_origens_retem_texto():
    """Gerenciador pode reter um texto e retornar seu ID."""
    gerenciador = GerenciadorOrigens(ttl_segundos=60)
    doc = criar_documento_texto("Este é um texto de teste.")

    id_origem = gerenciador.reter_texto(doc)

    assert id_origem is not None
    assert isinstance(id_origem, str)
    assert len(id_origem) > 0
