from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument
from pydantic import BaseModel, Field, field_validator

from src.backend.pdf_extraction import (
    PdfExtractionError,
    PdfTextUnavailableError,
    extract_pdf_text,
)

MAX_DOCUMENT_SIZE_BYTES = 10 * 1024 * 1024
MAX_TEXT_SIZE_BYTES = 10 * 1024 * 1024


class EntradaMulticanalError(Exception):
    """Erro base para qualquer problema de entrada de documento."""


class PdfInputError(EntradaMulticanalError):
    """Erro de entrada de PDF."""


class DocxExtractionError(EntradaMulticanalError):
    """Erro de leitura ou parsing de documento DOCX."""


class DocumentoOrigem(BaseModel):
    """Representa uma entrada de origem de documento após normalização do canal."""

    canal: str = Field(..., pattern="^(pdf|docx|texto|extensao)$")
    texto: str
    identificador_origem: str
    tamanho_bytes: int

    @field_validator("texto")
    @classmethod
    def _texto_nao_vazio(cls, valor: str) -> str:
        if not isinstance(valor, str):
            raise TypeError("Texto da origem deve ser uma string.")
        return valor

    @field_validator("tamanho_bytes")
    @classmethod
    def _tamanho_positivo(cls, valor: int) -> int:
        if valor < 0:
            raise ValueError("Tamanho do documento nao pode ser negativo.")
        return valor


def extrair_documento_pdf(caminho: str | Path) -> DocumentoOrigem:
    """Adapta a extração existente de PDF para o contrato de entrada multicanal."""
    input_path = Path(caminho)
    texto = extract_pdf_text(input_path)
    try:
        tamanho_bytes = input_path.stat().st_size
    except FileNotFoundError:
        tamanho_bytes = len(texto.encode("utf-8"))
    return DocumentoOrigem(
        canal="pdf",
        texto=texto,
        identificador_origem=str(input_path),
        tamanho_bytes=tamanho_bytes,
    )


def extrair_documento_docx(caminho: str | Path, *, max_size_bytes: int = MAX_DOCUMENT_SIZE_BYTES) -> DocumentoOrigem:
    """Extrai texto de um arquivo DOCX usando python-docx."""
    input_path = Path(caminho)

    if input_path.suffix.lower() != ".docx":
        raise DocxExtractionError("O arquivo de entrada deve ter extensao .docx.")
    if not input_path.is_file():
        raise DocxExtractionError("O arquivo DOCX nao foi encontrado ou nao pode ser lido.")
    if input_path.stat().st_size > max_size_bytes:
        raise DocxExtractionError("O arquivo DOCX excede o limite de tamanho permitido.")

    try:
        doc = DocxDocument(str(input_path))
        paragrafos = [paragrafo.text for paragrafo in doc.paragraphs if paragrafo.text.strip()]
        texto = "\n".join(paragrafos)
    except Exception as error:  # noqa: BLE001
        raise DocxExtractionError("O arquivo DOCX esta corrompido ou invalido.") from error

    if not texto.strip():
        raise DocxExtractionError("O arquivo DOCX nao possui texto utilizavel.")

    return DocumentoOrigem(
        canal="docx",
        texto=texto,
        identificador_origem=str(input_path),
        tamanho_bytes=input_path.stat().st_size,
    )


def criar_documento_texto(valor: str, *, max_size_bytes: int = MAX_TEXT_SIZE_BYTES) -> DocumentoOrigem:
    """Cria um documento a partir de texto colado ou clipboard."""
    if not isinstance(valor, str):
        raise TypeError("O texto fornecido deve ser uma string.")
    if len(valor.encode("utf-8")) > max_size_bytes:
        raise ValueError("O texto excede o limite de tamanho permitido.")

    return DocumentoOrigem(
        canal="texto",
        texto=valor,
        identificador_origem="clipboard",
        tamanho_bytes=len(valor.encode("utf-8")),
    )


def criar_documento_extensao(texto: str, identificador_origem: str, *, max_size_bytes: int = MAX_TEXT_SIZE_BYTES) -> DocumentoOrigem:
    """Cria um documento proveniente de texto capturado por extensão de navegador."""
    if not isinstance(texto, str):
        raise TypeError("O texto da extensao deve ser uma string.")
    if len(texto.encode("utf-8")) > max_size_bytes:
        raise ValueError("O texto da extensao excede o limite de tamanho permitido.")

    return DocumentoOrigem(
        canal="extensao",
        texto=texto,
        identificador_origem=identificador_origem,
        tamanho_bytes=len(texto.encode("utf-8")),
    )
