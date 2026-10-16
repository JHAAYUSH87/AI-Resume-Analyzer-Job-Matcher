from io import BytesIO
from PyPDF2 import PdfReader


def extract_resume_text(pdf_bytes: bytes) -> tuple[str, int]:
    """Extract readable text from a PDF resume."""
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        reader = PdfReader(BytesIO(pdf_bytes))

        if reader.is_encrypted:
            raise ValueError(
                "This PDF is password-protected. Upload an unlocked PDF."
            )

        pages = [
            (page.extract_text() or "").strip()
            for page in reader.pages
        ]
        text = "\n\n".join(page for page in pages if page).strip()

        if not text:
            raise ValueError(
                "No readable text found. This may be a scanned PDF; "
                "please upload a text-based PDF."
            )

        return text, len(reader.pages)

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            "Could not read this PDF. Please try another valid PDF."
        ) from exc
