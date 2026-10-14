from pathlib import Path
import pymupdf as fitz


def search_pdf_folder(folder_path, query):
    folder = Path(folder_path)

    if not folder.is_dir():
        return {"error": "Folder does not exist."}

    query = query.strip()

    if not query:
        return {"error": "Search query cannot be empty."}

    results = []

    for pdf_path in folder.rglob("*.pdf"):
        try:
            with fitz.open(pdf_path) as document:
                for page_number, page in enumerate(document, start=1):
                    text = page.get_text()

                    if query.casefold() in text.casefold():
                        results.append({
                            "file": pdf_path.name,
                            "path": str(pdf_path),
                            "page": page_number,
                            "match": query
                        })

        except (OSError, ValueError, RuntimeError):
            # Skip unreadable or invalid PDFs.
            continue

    return results