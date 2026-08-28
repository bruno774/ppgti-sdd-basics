from src.backend.settings import MAX_PDF_BINARY_SIZE_BYTES


def test_max_pdf_binary_size_is_100_megabytes():
    assert MAX_PDF_BINARY_SIZE_BYTES == 100 * 1024 * 1024
