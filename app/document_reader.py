
from pathlib import Path
import pymupdf as fitz


# -----------------------------------------
# 1. Validate PDF path
# -----------------------------------------
def validate_pdf(pdf_path):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError("PDF file does not exist.")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The selected file is not a PDF.")

    return path


# -----------------------------------------
# 2. Extract text from all PDF pages
# -----------------------------------------
def extract_pdf_text(pdf_path, password=None):
    try:
        path = validate_pdf(pdf_path)

        with fitz.open(path) as document:
            if document.needs_pass:
                if password is None:
                    return "This PDF requires a password."

                if not document.authenticate(password):
                    return "Incorrect PDF password."

            pages = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text()
                pages.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

            result = "\n".join(pages)

            if not result.strip():
                return "No selectable text found in this PDF."

            return result

    except (OSError, ValueError, RuntimeError) as error:
        return f"Unable to read PDF: {error}"


# -----------------------------------------
# 3. Get PDF metadata
# -----------------------------------------
def get_pdf_metadata(pdf_path, password=None):
    try:
        path = validate_pdf(pdf_path)

        with fitz.open(path) as document:
            if document.needs_pass:
                if password is None:
                    return "This PDF requires a password."

                if not document.authenticate(password):
                    return "Incorrect PDF password."

            return {
                "filename": path.name,
                "page_count": len(document),
                "metadata": document.metadata
            }

    except (OSError, ValueError, RuntimeError) as error:
        return f"Unable to read PDF metadata: {error}"


# -----------------------------------------
# 4. Count PDF pages
# -----------------------------------------
def count_pdf_pages(pdf_path, password=None):
    try:
        path = validate_pdf(pdf_path)

        with fitz.open(path) as document:
            if document.needs_pass:
                if password is None:
                    return "This PDF requires a password."

                if not document.authenticate(password):
                    return "Incorrect PDF password."

            return len(document)

    except (OSError, ValueError, RuntimeError) as error:
        return f"Unable to count pages: {error}"


# -----------------------------------------
# 5. Extract text from the first page
# -----------------------------------------
def read_first_page(pdf_path, password=None):
    try:
        path = validate_pdf(pdf_path)

        with fitz.open(path) as document:
            if document.needs_pass:
                if password is None:
                    return "This PDF requires a password."

                if not document.authenticate(password):
                    return "Incorrect PDF password."

            if len(document) == 0:
                return "This PDF has no pages."

            return document[0].get_text()

    except (OSError, ValueError, RuntimeError) as error:
        return f"Unable to read first page: {error}"


# -----------------------------------------
# 6. Count words in a PDF
# -----------------------------------------
def count_pdf_words(pdf_path, password=None):
    text = extract_pdf_text(pdf_path, password)

    if not isinstance(text, str) or text.startswith(
        ("Unable to", "Error:", "This PDF", "Incorrect", "No selectable")
    ):
        return text

    return len(text.split())


# -----------------------------------------
# 7. Save extracted PDF text to a TXT file
# -----------------------------------------
def save_pdf_as_text(pdf_path, output_path, password=None):
    text = extract_pdf_text(pdf_path, password)

    if not isinstance(text, str) or text.startswith(
        ("Unable to", "Error:", "This PDF", "Incorrect", "No selectable")
    ):
        return text

    try:
        output = Path(output_path)

        if output.suffix.lower() != ".txt":
            return "Output filename must end with .txt."

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")

        return f"Text successfully saved to: {output.resolve()}"

    except (OSError, ValueError) as error:
        return f"Unable to save text: {error}"


# -----------------------------------------
# 8. Search for a keyword in one PDF
# -----------------------------------------
def search_pdf(pdf_path, keyword, password=None):
    if not keyword or not keyword.strip():
        return "Please enter a keyword."

    try:
        path = validate_pdf(pdf_path)
        matches = []

        with fitz.open(path) as document:
            if document.needs_pass:
                if password is None:
                    return "This PDF requires a password."

                if not document.authenticate(password):
                    return "Incorrect PDF password."

            for page_number, page in enumerate(document, start=1):
                text = page.get_text()

                if keyword.casefold() in text.casefold():
                    matches.append({
                        "filename": path.name,
                        "page": page_number,
                        "snippet": get_snippet(text, keyword)
                    })

        return matches

    except (OSError, ValueError, RuntimeError) as error:
        return f"Unable to search PDF: {error}"


# -----------------------------------------
# 9. Helper: Get a short search-result snippet
# -----------------------------------------
def get_snippet(text, keyword, context=60):
    text_lower = text.casefold()
    keyword_lower = keyword.casefold()
    position = text_lower.find(keyword_lower)

    if position == -1:
        return ""

    start = max(0, position - context)
    end = min(len(text), position + len(keyword) + context)

    return text[start:end].replace("\n", " ").strip()


# -----------------------------------------
# 10. Search across all PDFs in a folder
# -----------------------------------------
def search_multiple_pdfs(folder_path, keyword):
    folder = Path(folder_path)

    if not folder.is_dir():
        return "Error: Folder does not exist."

    if not keyword or not keyword.strip():
        return "Please enter a keyword."

    results = []

    # Find PDFs in this folder and its subfolders.
    for pdf_path in folder.rglob("*"):
        if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
            continue

        matches = search_pdf(pdf_path, keyword)

        if isinstance(matches, list):
            results.extend(matches)

    return results


# -----------------------------------------
# 11. Display search results
# -----------------------------------------
def display_search_results(results):
    if isinstance(results, str):
        print(results)
        return

    if not results:
        print("No matching keyword found.")
        return

    print(f"\nFound {len(results)} matching page(s):\n")

    for result in results:
        print(f"PDF: {result['filename']}")
        print(f"Page: {result['page']}")
        print(f"Context: {result['snippet']}")
        print("-" * 50)


# -----------------------------------------
# TEST MENU
# -----------------------------------------
if __name__ == "__main__":
    while True:
        print("\n===== JARVIS PDF READER =====")
        print("1. Extract all PDF text")
        print("2. Get PDF metadata")
        print("3. Count PDF pages")
        print("4. Read first page")
        print("5. Count words")
        print("6. Save PDF text as TXT")
        print("7. Search in one PDF")
        print("8. Search across a folder of PDFs")
        print("9. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "9":
            print("Jarvis PDF Reader closed.")
            break

        if choice in {"1", "2", "3", "4", "5", "6", "7"}:
            pdf_path = input("Enter the full PDF path: ").strip().strip('"')

            if choice == "1":
                print(extract_pdf_text(pdf_path))

            elif choice == "2":
                print(get_pdf_metadata(pdf_path))

            elif choice == "3":
                print("Page count:", count_pdf_pages(pdf_path))

            elif choice == "4":
                print(read_first_page(pdf_path))

            elif choice == "5":
                print("Word count:", count_pdf_words(pdf_path))

            elif choice == "6":
                output_path = input(
                    "Enter the output TXT path: "
                ).strip().strip('"')

                print(save_pdf_as_text(pdf_path, output_path))

            elif choice == "7":
                keyword = input("Enter the keyword to search: ")
                results = search_pdf(pdf_path, keyword)
                display_search_results(results)

        elif choice == "8":
            folder_path = input(
                "Enter the folder containing PDFs: "
            ).strip().strip('"')

            keyword = input("Enter the keyword to search: ")
            results = search_multiple_pdfs(folder_path, keyword)
            display_search_results(results)

        else:
            print("Invalid choice. Please enter 1 to 9.")



# import pymupdf as fitz

# import  fitz
# from pathlib import Path


# def extract_pdf_text(pdf_path):
#     pdf_path = Path(pdf_path)

#     if not pdf_path.is_file():
#         return "Error: PDF file does not exist."

#     if pdf_path.suffix.lower() != ".pdf":
#         return "Error: The selected file is not a PDF."

#     try:
#         with fitz.open(pdf_path) as document:
#             pages = []

#             for page_number, page in enumerate(document, start=1):
#                 text = page.get_text()

#                 pages.append(
#                     f"\n--- Page {page_number} ---\n{text}"
#                 )

#             return "\n".join(pages)

#     except (OSError, ValueError, RuntimeError) as error:
#         return f"Unable to read PDF: {error}"


# def get_pdf_metadata(pdf_path):
#     pdf_path = Path(pdf_path)

#     if not pdf_path.is_file():
#         return "Error: PDF file does not exist."

#     if pdf_path.suffix.lower() != ".pdf":
#         return "Error: The selected file is not a PDF."

#     try:
#         with fitz.open(pdf_path) as document:
#             return {
#                 "filename": pdf_path.name,
#                 "page_count": len(document),
#                 "metadata": document.metadata
#             }

#     except (OSError, ValueError, RuntimeError) as error:
#         return f"Unable to read PDF: {error}"