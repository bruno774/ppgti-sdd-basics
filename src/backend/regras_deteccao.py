"""Regras e heurísticas para detecção de entidades por tipo."""

import re
from typing import TypedDict

from src.backend.categorias import Catalogo


class DeteccaoRaw(TypedDict):
    """Resultado bruto de uma detecção antes de validação."""

    tipo: str
    inicio: int
    fim: int
    confianca: float
    origem: str


class AplicadorRegrasDeteccao:
    """Aplica regras de detecção por tipo canônico."""

    def __init__(self, catalogo: Catalogo) -> None:
        self.catalogo = catalogo

    def executar(self, texto: str) -> list[DeteccaoRaw]:
        """Executa todas as regras sobre o texto e retorna detecções brutas."""
        deteccoes: list[DeteccaoRaw] = []

        deteccoes.extend(self._detectar_cpf(texto))
        deteccoes.extend(self._detectar_rg(texto))
        deteccoes.extend(self._detectar_email(texto))
        deteccoes.extend(self._detectar_telefone(texto))
        deteccoes.extend(self._detectar_endereco(texto))
        deteccoes.extend(self._detectar_nome(texto))
        deteccoes.extend(self._detectar_cid_doenca(texto))
        deteccoes.extend(self._detectar_religiao(texto))
        deteccoes.extend(self._detectar_genero_sexual(texto))
        deteccoes.extend(self._detectar_cor_pele(texto))
        deteccoes.extend(self._detectar_classe_social(texto))

        return deteccoes

    def _detectar_cpf(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta CPF em formato 000.000.000-00 ou 00000000000."""
        deteccoes: list[DeteccaoRaw] = []
        padrao_formatado = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        for match in re.finditer(padrao_formatado, texto):
            deteccoes.append(DeteccaoRaw(tipo="CPF", inicio=match.start(), fim=match.end(), confianca=0.95, origem="regra"))
        padrao_simples = r"\d{11}"
        for match in re.finditer(padrao_simples, texto):
            if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto[match.start():match.end()]):
                deteccoes.append(DeteccaoRaw(tipo="CPF", inicio=match.start(), fim=match.end(), confianca=0.80, origem="regra"))
        return deteccoes

    def _detectar_rg(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta RG em formato de 7-9 dígitos com letra ou traço."""
        deteccoes: list[DeteccaoRaw] = []
        padrao = r"\d{7,9}[-\s]?[a-zA-Z]?"
        for match in re.finditer(padrao, texto):
            texto_match = texto[match.start():match.end()].strip()
            if re.match(r"^\d{7,9}$", texto_match) or re.match(r"^\d{7,9}[-\s][a-zA-Z]$", texto_match):
                deteccoes.append(DeteccaoRaw(tipo="RG", inicio=match.start(), fim=match.end(), confianca=0.70, origem="regra"))
        return deteccoes

    def _detectar_email(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta endereço de email."""
        deteccoes: list[DeteccaoRaw] = []
        padrao = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        for match in re.finditer(padrao, texto):
            deteccoes.append(DeteccaoRaw(tipo="EMAIL", inicio=match.start(), fim=match.end(), confianca=0.95, origem="regra"))
        return deteccoes

    def _detectar_telefone(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta telefone com DDD/DDI."""
        deteccoes: list[DeteccaoRaw] = []
        padrao = r"(?:\+\d{1,3}\s)?(?:\(\d{2}\)\s?)?\d{4,5}-?\d{4}"
        for match in re.finditer(padrao, texto):
            deteccoes.append(DeteccaoRaw(tipo="TELEFONE", inicio=match.start(), fim=match.end(), confianca=0.85, origem="regra"))
        return deteccoes

    def _detectar_endereco(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta endereço (padrão simplificado)."""
        deteccoes: list[DeteccaoRaw] = []
        padrao = r"(?:Rua|Avenida|Av|Travessa|Praça|Beco|Largo|Estrada|Rodovia)\s+[A-Z][a-záéíóúãõç\s]+(?:,?\s*\d+)?(?:,?\s*(?:Apto|Apt|Lote|Sala)\s*\d+)?(?:,?\s*\d{5}-?\d{3})?"
        for match in re.finditer(padrao, texto, re.IGNORECASE):
            if len(match.group()) > 10:
                deteccoes.append(DeteccaoRaw(tipo="ENDERECO", inicio=match.start(), fim=match.end(), confianca=0.75, origem="regra"))
        return deteccoes

    def _detectar_nome(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta nomes próprios (padrão permissivo)."""
        deteccoes: list[DeteccaoRaw] = []
        padrao = r"\b(?:[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+){1,3})\b"
        for match in re.finditer(padrao, texto):
            palavras = match.group().split()
            if len(palavras) >= 2 and len(match.group()) >= 6:
                confianca = min(0.6 + (len(palavras) * 0.1), 0.85)
                deteccoes.append(DeteccaoRaw(tipo="NOME", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes

    def _detectar_cid_doenca(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta menção a doenças (tipo sensível)."""
        deteccoes: list[DeteccaoRaw] = []
        doencas = {"diabetes": 0.90, "hipertensão": 0.90, "gripe": 0.85, "covid": 0.95, "câncer": 0.95, "tuberculose": 0.90, "hepatite": 0.90, "depressão": 0.85, "ansiedade": 0.75, "asma": 0.90}
        for doenca, confianca in doencas.items():
            padrao = rf"\b{re.escape(doenca)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                deteccoes.append(DeteccaoRaw(tipo="CID_DOENCA", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes

    def _detectar_religiao(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta menção a religiões (tipo sensível)."""
        deteccoes: list[DeteccaoRaw] = []
        religioes = {"católica": 0.90, "evangélica": 0.90, "islâmica": 0.90, "judaica": 0.90, "budista": 0.90, "espírita": 0.85, "protestante": 0.85, "cristã": 0.80}
        for religiao, confianca in religioes.items():
            padrao = rf"\b{re.escape(religiao)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                deteccoes.append(DeteccaoRaw(tipo="RELIGIAO", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes

    def _detectar_genero_sexual(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta menção a orientação sexual (tipo sensível)."""
        deteccoes: list[DeteccaoRaw] = []
        orientacoes = {"homossexual": 0.95, "heterossexual": 0.95, "bissexual": 0.95, "lésbica": 0.95, "gay": 0.85, "LGBT": 0.80}
        for orientacao, confianca in orientacoes.items():
            padrao = rf"\b{re.escape(orientacao)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                deteccoes.append(DeteccaoRaw(tipo="GENERO_SEXUAL", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes

    def _detectar_cor_pele(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta menção a cor/raça (tipo sensível)."""
        deteccoes: list[DeteccaoRaw] = []
        cores = {"branco": 0.85, "negro": 0.90, "preto": 0.85, "pardo": 0.85, "moreno": 0.70, "asiático": 0.85, "indígena": 0.85, "afro": 0.90}
        for cor, confianca in cores.items():
            padrao = rf"\b{re.escape(cor)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                deteccoes.append(DeteccaoRaw(tipo="COR_PELE", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes

    def _detectar_classe_social(self, texto: str) -> list[DeteccaoRaw]:
        """Detecta menção a classe social (tipo sensível)."""
        deteccoes: list[DeteccaoRaw] = []
        classes = {"pobre": 0.80, "carente": 0.75, "abastado": 0.80, "milionário": 0.90, "operário": 0.75, "elite": 0.75, "classe média": 0.70, "baixa renda": 0.85, "alta renda": 0.85}
        for classe, confianca in classes.items():
            padrao = rf"\b{re.escape(classe)}\b"
            for match in re.finditer(padrao, texto, re.IGNORECASE):
                deteccoes.append(DeteccaoRaw(tipo="CLASSE_SOCIAL", inicio=match.start(), fim=match.end(), confianca=confianca, origem="regra"))
        return deteccoes
