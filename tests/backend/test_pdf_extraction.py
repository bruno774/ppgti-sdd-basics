from unittest.mock import Mock, patch

import pytest

from src.backend.pdf_extraction import (
    PdfExtractionError,
    PdfTextUnavailableError,
    extract_pdf_text,
)


def test_extract_pdf_text_returns_text_from_each_page(tmp_path):
    pdf_path = tmp_path / "documento.pdf"
    pdf_path.write_bytes(b"%PDF")
    first_page = Mock()
    first_page.extract_text.return_value = "Primeira pagina"
    second_page = Mock()
    second_page.extract_text.return_value = "Segunda pagina"
    pdf_reader = Mock(is_encrypted=False, pages=[first_page, second_page])

    with patch("src.backend.pdf_extraction.PdfReader", return_value=pdf_reader):
        extracted_text = extract_pdf_text(pdf_path)

    assert extracted_text == "Primeira pagina\nSegunda pagina"


def test_extract_pdf_text_rejects_pdf_without_text_layer(tmp_path):
    pdf_path = tmp_path / "sem_texto.pdf"
    pdf_path.write_bytes(b"%PDF")
    blank_page = Mock()
    blank_page.extract_text.return_value = ""
    pdf_reader = Mock(is_encrypted=False, pages=[blank_page])

    with patch("src.backend.pdf_extraction.PdfReader", return_value=pdf_reader):
        with pytest.raises(PdfTextUnavailableError):
            extract_pdf_text(pdf_path)


def test_extract_pdf_text_rejects_protected_pdf(tmp_path):
    pdf_path = tmp_path / "protegido.pdf"
    pdf_path.write_bytes(b"%PDF")
    pdf_reader = Mock(is_encrypted=True)

    with patch("src.backend.pdf_extraction.PdfReader", return_value=pdf_reader):
        with pytest.raises(PdfExtractionError, match="protegido"):
            extract_pdf_text(pdf_path)
