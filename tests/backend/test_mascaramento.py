import pytest

from src.backend.categorias import Catalogo, CategoriaEntidade
from src.backend.mascaramento import (
    EntidadeDetectada,
    aplicar_mascaramento,
    atribuir_indices_entidades,
    validar_sobreposicao,
)


def test_atribui_indice_reaproveitado_para_mesma_entidade_e_distinto_para_outra():
    entidades = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=8, texto="Maria", confianca=0.9, identificador="ent-1"),
        EntidadeDetectada(tipo="NOME", inicio=20, fim=28, texto="maria", confianca=0.9, identificador="ent-2"),
        EntidadeDetectada(tipo="NOME", inicio=40, fim=48, texto="Joao", confianca=0.8, identificador="ent-3"),
    ]

    resultado = atribuir_indices_entidades(entidades)

    assert [entidade.indice for entidade in resultado] == [1, 1, 2]


def test_validar_sobreposicao_aceita_sem_sobreposicao_e_rejeita_parcial():
    sem_sobreposicao = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=5, texto="Maria", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="CPF", inicio=10, fim=20, texto="123", confianca=0.9, identificador="e2"),
    ]
    sobreposicao_total = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=5, texto="Maria", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="NOME", inicio=0, fim=5, texto="Maria", confianca=0.9, identificador="e2"),
    ]
    sobreposicao_parcial = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=10, texto="Maria Silva", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="CPF", inicio=5, fim=15, texto="123", confianca=0.9, identificador="e2"),
    ]

    validar_sobreposicao(sem_sobreposicao)
    validar_sobreposicao(sobreposicao_total)
    with pytest.raises(ValueError, match="sobreposicao"):
        validar_sobreposicao(sobreposicao_parcial)


def test_aplicar_mascaramento_preserva_categorias_nao_selecionadas_e_indice_por_tipo():
    catalogo = Catalogo()
    texto = "Nome: Maria e endereco: Rua A."
    entidades = [
        EntidadeDetectada(tipo="NOME", inicio=6, fim=11, texto="Maria", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="ENDERECO", inicio=25, fim=33, texto="Rua A.", confianca=0.8, identificador="e2"),
    ]

    resultado = aplicar_mascaramento(
        texto,
        entidades,
        categorias_selecionadas=["NOME"],
        catalogo=catalogo,
    )

    assert "Maria" not in resultado["texto"]
    assert "Rua A." in resultado["texto"]
    assert "nom1" in resultado["texto"]
    assert "endereco" in resultado["texto"]


def test_aplicar_mascaramento_preserva_acentuacao_paragrafos_e_nao_exibe_valor_original():
    catalogo = Catalogo()
    texto = "João\n\nCPF: 123.456.789-09\n"
    entidades = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=4, texto="João", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="CPF", inicio=10, fim=26, texto="123.456.789-09", confianca=0.95, identificador="e2"),
    ]

    resultado = aplicar_mascaramento(texto, entidades, categorias_selecionadas=["NOME", "CPF"], catalogo=catalogo)

    assert "João" not in resultado["texto"]
    assert "123.456.789-09" not in resultado["texto"]
    assert "\n\n" in resultado["texto"]
    assert "nom1" in resultado["texto"] and "cpf1" in resultado["texto"]


def test_aplicar_mascaramento_reporta_contagem_por_tipo():
    catalogo = Catalogo()
    texto = "Maria e Maria e João"
    entidades = [
        EntidadeDetectada(tipo="NOME", inicio=0, fim=5, texto="Maria", confianca=0.9, identificador="e1"),
        EntidadeDetectada(tipo="NOME", inicio=9, fim=14, texto="Maria", confianca=0.9, identificador="e2"),
        EntidadeDetectada(tipo="NOME", inicio=18, fim=22, texto="João", confianca=0.8, identificador="e3"),
    ]

    resultado = aplicar_mascaramento(texto, entidades, categorias_selecionadas=["NOME"], catalogo=catalogo)

    assert resultado["contagem_por_tipo"]["NOME"] == 3
    assert "nom1" in resultado["texto"]
    assert "nom2" in resultado["texto"]
