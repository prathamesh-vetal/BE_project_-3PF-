
from security import (
    validate_path,
    validate_file,
    validate_folder,
    confirm_action
)

from file_manager import (
    list_files,
    list_folders,
    find_files,
    file_information,
    search_file,
    create_folder,
    copy_file,
    move_file,
    rename_file,
    delete_file
)
from document_reader import extract_pdf_text, get_pdf_metadata
from document_search import search_pdf_folder


def handle_command():

    while True:

        print("\n===== OFFLINE AI ASSISTANT =====")
        print("1. List files")
        print("2. List folders")
        print("3. Find files by extension")
        print("4. File information")
        print("5. Search file")
        print("6. Create folder")
        print("7. Copy file")
        print("8. Move file")
        print("9. Rename file")
        print("10. Delete file")
        print("11. Read PDF document")
        print("12. Search inside PDF documents")
        print("13. Exit")

        choice = input("\nEnter your choice: ").strip()

        # 1. List files
        if choice == "1":

            folder_path = input("Enter folder path: ").strip()

            valid, message = validate_folder(folder_path)
            if not valid:
                print(message)
                continue

            result = list_files(folder_path)

            print("\nFiles:")
            if isinstance(result, list):
                for file in result:
                    print(file)
            else:
                print(result)

        # 2. List folders
        elif choice == "2":

            folder_path = input("Enter folder path: ").strip()

            valid, message = validate_folder(folder_path)
            if not valid:
                print(message)
                continue

            result = list_folders(folder_path)

            print("\nFolders:")
            if isinstance(result, list):
                for folder in result:
                    print(folder)
            else:
                print(result)

        # 3. Find files by extension
        elif choice == "3":

            folder_path = input("Enter folder path: ").strip()
            extension = input(
                "Enter extension (example: .pdf): "
            ).strip()

            valid, message = validate_folder(folder_path)
            if not valid:
                print(message)
                continue

            if not extension:
                print("Please enter a file extension.")
                continue

            if not extension.startswith("."):
                extension = "." + extension

            result = find_files(folder_path, extension)

            print("\nMatching files:")
            if isinstance(result, list):
                if result:
                    for file in result:
                        print(file)
                else:
                    print("No matching files found.")
            else:
                print(result)

        # 4. File information
        elif choice == "4":

            file_path = input("Enter file path: ").strip()

            valid, message = validate_file(file_path)
            if not valid:
                print(message)
                continue

            result = file_information(file_path)

            print("\nFile Information:")
            if isinstance(result, dict):
                for key, value in result.items():
                    print(f"{key}: {value}")
            else:
                print(result)

        # 5. Search file
        elif choice == "5":

            folder_path = input("Enter folder path: ").strip()
            filename = input("Enter file name to search: ").strip()

            valid, message = validate_folder(folder_path)
            if not valid:
                print(message)
                continue

            if not filename:
                print("Please enter a file name.")
                continue

            result = search_file(folder_path, filename)

            print("\nSearch Results:")
            if isinstance(result, list):
                if result:
                    for file in result:
                        print(file)
                else:
                    print("No matching files found.")
            else:
                print(result)

        # 6. Create folder

        # elif choice == "6":

        #    folder_path = input(
        #      "Enter the full path of the new folder: "
        #     ).strip()

        #    print("DEBUG: Before validate_path")

        # valid, message = validate_path(folder_path)
        # print("DEBUG: After validate_path:", message)

        # if not valid:
        #    print(message)
        #    continue

        # if not confirm_action("CREATE FOLDER", folder_path):
        #    print("Folder creation cancelled.")
        #    continue

        # print("DEBUG: Before create_folder")

        # result = create_folder(folder_path)
        # print(result)
        elif choice == "6":

            folder_path = input(
                "Enter the full path of the new folder: "
            ).strip()

            # valid, message = validate_path(folder_path)
            # if not valid:
            #     print(message)
            #     continue

            # if not confirm_action("CREATE FOLDER", folder_path):
            #     print("Folder creation cancelled.")
            #     continue

            result = create_folder(folder_path)
            print(result)

        # 7. Copy file
        elif choice == "7":

            source = input("Enter source file path: ").strip()
            destination = input(
                "Enter destination file path: "
            ).strip()

            valid, message = validate_file(source)
            if not valid:
                print(message)
                continue

            valid, message = validate_path(destination)
            if not valid:
                print(message)
                continue

            if not confirm_action("COPY", source):
                print("Copy cancelled.")
                continue

            result = copy_file(source, destination)
            print(result)

        # 8. Move file
        elif choice == "8":

            source = input("Enter source file path: ").strip()
            destination = input(
                "Enter destination file path: "
            ).strip()

            valid, message = validate_file(source)
            if not valid:
                print(message)
                continue

            valid, message = validate_path(destination)
            if not valid:
                print(message)
                continue

            if not confirm_action("MOVE", source):
                print("Move cancelled.")
                continue

            result = move_file(source, destination)
            print(result)

        # 9. Rename file
        elif choice == "9":

            file_path = input("Enter file path: ").strip()
            new_name = input("Enter new file name: ").strip()

            valid, message = validate_file(file_path)
            if not valid:
                print(message)
                continue

            if not new_name:
                print("New file name cannot be empty.")
                continue

            if not confirm_action("RENAME", file_path):
                print("Rename cancelled.")
                continue

            result = rename_file(file_path, new_name)
            print(result)

        # 10. Delete file
        elif choice == "10":

            file_path = input("Enter file path: ").strip()

            valid, message = validate_file(file_path)
            if not valid:
                print(message)
                continue

            if not confirm_action("DELETE", file_path):
                print("Delete cancelled.")
                continue

            result = delete_file(file_path)
            print(result)

        # 11. Read PDF document
        elif choice == "11":

            pdf_path = input("Enter the full path of a PDF: ").strip().strip('"')

            valid, message = validate_file(pdf_path)
            if not valid:
                print(message)
                continue

            print("\n===== PDF METADATA =====")
            print(get_pdf_metadata(pdf_path))

            print("\n===== PDF CONTENT =====")
            print(extract_pdf_text(pdf_path))

        # 12. Search inside PDF documents
        elif choice == "12":

            folder_path = input("Enter folder path: ").strip().strip('"')
            query = input("Enter keyword or phrase: ")

            valid, message = validate_folder(folder_path)
            if not valid:
                print(message)
                continue

            results = search_pdf_folder(folder_path, query)

            if isinstance(results, dict) and "error" in results:
                print(results["error"])

            elif not results:
                print("No matching documents found.")

            else:
                print(f"\nFound {len(results)} matching page(s):\n")

                for result in results:
                    print(f"File: {result['file']}")
                    print(f"Page: {result['page']}")
                    print(f"Match: {result['match']}")
                    print(f"Path: {result['path']}")
                    print("-" * 40)

        # 13. Exit
        elif choice == "13":

            print("Jarvis shutting down...")
            break

        # # 11. Exit
        # elif choice == "11":

        #     print("Jarvis shutting down...")
        #     break

        # else:
        #     print("Invalid choice. Please try again.")


if __name__ == "__main__":
    handle_command()



