from unittest.mock import Mock, patch

import pytest

from src.backend.pdf_binary_extraction import (
    PdfBinaryExtractionError,
    PdfBinaryTextUnavailableError,
    extract_pdf_text_from_bytes,
)

PDF_BYTES = b"%PDF-1.7\nconteudo-de-teste"


def test_extract_pdf_text_from_bytes_returns_clear_portuguese_text():
    page = Mock()
    page.extract_text.return_value = "O documento esta em portugues."
    pdf_reader = Mock(is_encrypted=False, pages=[page])

    with patch("src.backend.pdf_binary_extraction.PdfReader", return_value=pdf_reader):
        extracted_text = extract_pdf_text_from_bytes(PDF_BYTES)

    assert extracted_text == "O documento esta em portugues."


def test_extract_pdf_text_from_bytes_rejects_non_pdf_content():
    with pytest.raises(PdfBinaryExtractionError, match="nao corresponde"):
        extract_pdf_text_from_bytes(b"conteudo invalido")


def test_extract_pdf_text_from_bytes_rejects_signed_pdf():
    with pytest.raises(PdfBinaryExtractionError, match="assinados"):
        extract_pdf_text_from_bytes(b"%PDF-1.7\n/ByteRange [0 1 2 3]")


def test_extract_pdf_text_from_bytes_rejects_pdf_without_text_layer():
    page = Mock()
    page.extract_text.return_value = ""
    pdf_reader = Mock(is_encrypted=False, pages=[page])

    with patch("src.backend.pdf_binary_extraction.PdfReader", return_value=pdf_reader):
        with pytest.raises(PdfBinaryTextUnavailableError, match="digitalizados"):
            extract_pdf_text_from_bytes(PDF_BYTES)


def test_extract_pdf_text_from_bytes_rejects_non_portuguese_text():
    page = Mock()
    page.extract_text.return_value = "This document is written in English."
    pdf_reader = Mock(is_encrypted=False, pages=[page])

    with patch("src.backend.pdf_binary_extraction.PdfReader", return_value=pdf_reader):
        with pytest.raises(PdfBinaryTextUnavailableError, match="portugues"):
            extract_pdf_text_from_bytes(PDF_BYTES)
