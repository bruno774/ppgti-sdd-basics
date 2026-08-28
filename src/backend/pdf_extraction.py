from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

DEFAULT_MAX_PDF_SIZE_BYTES = 50 * 1024 * 1024


class PdfExtractionError(Exception):
    """Raised when a PDF cannot be safely read for text extraction."""


class PdfTextUnavailableError(PdfExtractionError):
    """Raised when a PDF has no usable text layer."""


def extract_pdf_text(
    pdf_path: str | Path,
    *,
    max_size_bytes: int = DEFAULT_MAX_PDF_SIZE_BYTES,
) -> str:
    """Return the text layer of a searchable PDF without retaining its contents."""
    input_path = Path(pdf_path)

    if max_size_bytes <= 0:
        raise ValueError("O limite de tamanho deve ser maior que zero.")
    if input_path.suffix.lower() != ".pdf":
        raise PdfExtractionError("O arquivo de entrada deve ter extensao .pdf.")
    if not input_path.is_file():
        raise PdfExtractionError("O arquivo PDF nao foi encontrado ou nao pode ser lido.")
    if input_path.stat().st_size > max_size_bytes:
        raise PdfExtractionError("O arquivo PDF excede o limite de tamanho permitido.")

    try:
        pdf_reader = PdfReader(input_path)
        if pdf_reader.is_encrypted:
            raise PdfExtractionError("O arquivo PDF esta protegido e nao pode ser lido.")
        page_texts = [page.extract_text() or "" for page in pdf_reader.pages]
    except PdfExtractionError:
        raise
    except (OSError, PdfReadError) as error:
        raise PdfExtractionError("Nao foi possivel ler o arquivo PDF.") from error

    extracted_text = "\n".join(page_texts)
    if not extracted_text.strip():
        raise PdfTextUnavailableError("O arquivo PDF nao possui camada de texto utilizavel.")

    return extracted_text
