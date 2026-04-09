import pypdf

def parse_txt(file_path: str) -> str:
    """Reads a TXT file and returns its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def parse_pdf(file_path: str) -> str:
    """Reads a PDF file and returns its textual content using pypdf."""
    text = ""
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
