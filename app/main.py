from command_handler import handle_command
from logger_config import logger


if __name__ == "__main__":
    handle_command()

# from document_reader import extract_pdf_text, get_pdf_metadata

# pdf_path = input("Enter the full path of a PDF: ").strip().strip('"')

# print("\n===== PDF METADATA =====")
# print(get_pdf_metadata(pdf_path))

# print("\n===== PDF CONTENT =====")
# print(extract_pdf_text(pdf_path))



# logger.info("Jarvis started successfully.")
# logger.warning("This is a warning test.")
# logger.error("This is an error test.")