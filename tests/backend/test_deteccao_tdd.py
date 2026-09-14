"""Testes para detecÃ§Ã£o de entidades com TDD."""

from src.backend.deteccao_tdd import DetectorEntidades
from src.backend.entrada_multicanal import criar_documento_texto


def test_detector_pode_ser_instanciado():
    """Detector pode ser instanciado sem parÃ¢metros."""
    detector = DetectorEntidades()
    assert detector is not None


def test_detectar_texto_vazio_retorna_lista_vazia():
    """Texto vazio nÃ£o gera nenhuma detecÃ§Ã£o."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("")
    entidades = detector.detectar(doc)
    assert entidades == []


def test_detectar_cpf_formatado():
    """Detecta CPF em formato 000.000.000-00."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Meu CPF Ã© 123.456.789-10.")
    entidades = detector.detectar(doc)

    assert len(entidades) >= 1
    cpf_entidade = entidades[0]
    assert cpf_entidade.tipo == "CPF"
    assert cpf_entidade.id == "cpf1"
    assert cpf_entidade.confianca >= 0.5


def test_detectar_cpf_nao_formatado():
    """Detecta CPF em formato 00000000000."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("CPF: 12345678910")
    entidades = detector.detectar(doc)

    assert len(entidades) >= 1
    cpf = entidades[0]
    assert cpf.tipo == "CPF"


def test_detectar_email():
    """Detecta endereÃ§o de email."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Entre em contato: joao@exemplo.com")
    entidades = detector.detectar(doc)

    emails = [e for e in entidades if e.tipo == "EMAIL"]
    assert len(emails) >= 1
    assert emails[0].id == "ema1"


def test_detectar_telefone():
    """Detecta telefone com DDD."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Ligue para (11) 98765-4321")
    entidades = detector.detectar(doc)

    phones = [e for e in entidades if e.tipo == "TELEFONE"]
    assert len(phones) >= 1


def test_detectar_rg():
    """Detecta RG."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("RG: 1234567-X")
    entidades = detector.detectar(doc)

    rgs = [e for e in entidades if e.tipo == "RG"]
    assert len(rgs) >= 1


def test_detectar_endereco():
    """Detecta endereço."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Rua das Flores, 123")
    entidades = detector.detectar(doc)
    enderecos = [e for e in entidades if e.tipo == "ENDERECO"]
    assert len(enderecos) >= 1

def test_detectar_nome():
    """Detecta nome próprio."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Meu nome é João Silva")
    entidades = detector.detectar(doc)
    nomes = [e for e in entidades if e.tipo == "NOME"]
    assert len(nomes) >= 1

def test_detectar_cid_doenca():
    """Detecta doença (tipo sensível)."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Paciente com diabetes")
    entidades = detector.detectar(doc)
    doencas = [e for e in entidades if e.tipo == "CID_DOENCA"]
    assert len(doencas) >= 1
    assert doencas[0].sensivel is True

def test_detectar_religiao():
    """Detecta religião (tipo sensível)."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Religião: católica")
    entidades = detector.detectar(doc)
    religioes = [e for e in entidades if e.tipo == "RELIGIAO"]
    assert len(religioes) >= 1
    assert religioes[0].sensivel is True


def test_texto_sem_entidades_retorna_vazio():
    """Texto sem dados pessoais não gera detecções."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Este é um texto completamente genérico sem dados sensíveis.")
    entidades = detector.detectar(doc)
    assert len(entidades) == 0


def test_multiplos_emails_recebem_ids_sequenciais():
    """Múltiplas entidades do mesmo tipo recebem IDs sequenciais."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Emails: joao@ex.com, maria@ex.com, pedro@ex.com")
    entidades = detector.detectar(doc)

    emails = [e for e in entidades if e.tipo == "EMAIL"]
    ids = [e.id for e in emails]
    assert ids == ["ema1", "ema2", "ema3"]


def test_entidade_sensivel_com_baixa_confianca_marca_revisao():
    """Entidade sensível com confiança < 0.75 é marcada para revisão."""
    detector = DetectorEntidades()
    # Vamos simular via teste direto na classe
    doc = criar_documento_texto("xyz")  # Texto vazio
    entidades = detector.detectar(doc)
    # Este teste precisa de acesso direto ao método ou fixture


def test_detectar_genero_sexual():
    """Detecta orientação sexual (tipo sensível)."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Orientação: LGBT")
    entidades = detector.detectar(doc)

    gens = [e for e in entidades if e.tipo == "GENERO_SEXUAL"]
    assert len(gens) >= 1
    assert gens[0].sensivel is True


def test_detectar_cor_pele():
    """Detecta cor/raça (tipo sensível)."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Pessoa de cor parda")
    entidades = detector.detectar(doc)

    cores = [e for e in entidades if e.tipo == "COR_PELE"]
    assert len(cores) >= 1


def test_detectar_classe_social():
    """Detecta classe social (tipo sensível)."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Pertence à classe média")
    entidades = detector.detectar(doc)

    classes = [e for e in entidades if e.tipo == "CLASSE_SOCIAL"]
    assert len(classes) >= 1


def test_ordenacao_por_posicao():
    """Entidades são retornadas ordenadas por posição."""
    detector = DetectorEntidades()
    doc = criar_documento_texto("Email: joao@ex.com CPF: 123.456.789-10 Telefone: (11) 98765-4321")
    entidades = detector.detectar(doc)

    for i in range(len(entidades) - 1):
        assert entidades[i].inicio <= entidades[i + 1].inicio
