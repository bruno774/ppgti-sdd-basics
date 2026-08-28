from io import BytesIO
import re
from typing import Final

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from src.backend.settings import MAX_PDF_BINARY_SIZE_BYTES

PORTUGUESE_SIGNAL_WORDS: Final[frozenset[str]] = frozenset(
    {
        "a",
        "ao",
        "as",
        "com",
        "da",
        "das",
        "de",
        "do",
        "dos",
        "e",
        "em",
        "na",
        "nas",
        "no",
        "nos",
        "o",
        "os",
        "para",
        "por",
        "que",
        "uma",
        "um",
    }
)
WORD_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


class PdfBinaryExtractionError(Exception):
    """Raised when binary PDF content is unsafe or unsuitable for extraction."""


class PdfBinaryTextUnavailableError(PdfBinaryExtractionError):
    """Raised when a PDF has no usable Portuguese text layer."""


def extract_pdf_text_from_bytes(pdf_content: bytes) -> str:
    """Return readable Portuguese text from an unsigned, searchable PDF binary."""
    if not isinstance(pdf_content, bytes):
        raise TypeError("O conteudo do PDF deve ser fornecido em bytes.")
    if not pdf_content:
        raise PdfBinaryExtractionError("O arquivo PDF esta vazio.")
    if len(pdf_content) > MAX_PDF_BINARY_SIZE_BYTES:
        raise PdfBinaryExtractionError("O arquivo PDF excede o limite de tamanho permitido.")
    if not pdf_content.startswith(b"%PDF-"):
        raise PdfBinaryExtractionError("O conteudo fornecido nao corresponde a um PDF legivel.")
    if b"/ByteRange" in pdf_content or b"/Type /Sig" in pdf_content:
        raise PdfBinaryExtractionError("PDFs assinados nao sao aceitos para extracao.")

    try:
        pdf_reader = PdfReader(BytesIO(pdf_content), strict=True)
        if pdf_reader.is_encrypted:
            raise PdfBinaryExtractionError("O arquivo PDF esta protegido e nao pode ser lido.")
        page_texts = [page.extract_text() or "" for page in pdf_reader.pages]
    except PdfBinaryExtractionError:
        raise
    except (OSError, PdfReadError, ValueError) as error:
        raise PdfBinaryExtractionError("O conteudo PDF esta corrompido ou nao pode ser lido.") from error

    extracted_text = "\n".join(page_texts).strip()
    if not extracted_text:
        raise PdfBinaryTextUnavailableError(
            "O arquivo PDF nao possui camada de texto utilizavel; PDFs digitalizados nao sao aceitos."
        )
    if not _is_clear_portuguese_text(extracted_text):
        raise PdfBinaryTextUnavailableError(
            "O arquivo PDF nao contem texto claro e legivel em lingua portuguesa."
        )

    return extracted_text


def _is_clear_portuguese_text(text: str) -> bool:
    words = [word.lower() for word in WORD_PATTERN.findall(text)]
    return len(words) >= 3 and any(word in PORTUGUESE_SIGNAL_WORDS for word in words)
