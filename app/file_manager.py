from pathlib import Path
import shutil
from datetime import datetime
from logger_config import logger
import os






# --------------------------------------------------
# 1. LIST FILES
# --------------------------------------------------

def list_files(folder_path):
    folder = Path(folder_path)

    if not folder.is_dir():
        logger.warning("List files failed: invalid folder: %s", folder)
        return "Folder does not exist or is not a directory."

    try:
        files = [
            item.name
            for item in folder.iterdir()
            if item.is_file()
        ]

        logger.info(
            "Listed %d files in %s",
            len(files), folder
        )
        return files

    except OSError:
        logger.exception("Unable to list files in %s", folder)
        return "Unable to list files. Check folder permissions."


# --------------------------------------------------
# 2. LIST FOLDERS
# --------------------------------------------------

def list_folders(folder_path):
    folder = Path(folder_path)

    if not folder.is_dir():
        logger.warning("List folders failed: invalid folder: %s", folder)
        return "Folder does not exist or is not a directory."

    try:
        folders = [
            item.name
            for item in folder.iterdir()
            if item.is_dir()
        ]

        logger.info(
            "Listed %d folders in %s",
            len(folders), folder
        )
        return folders

    except OSError:
        logger.exception("Unable to list folders in %s", folder)
        return "Unable to list folders. Check folder permissions."


# --------------------------------------------------
# 3. SEARCH FOR FILES BY NAME
# --------------------------------------------------

def search_file(folder_path, filename):
    folder = Path(folder_path)

    if not folder.is_dir():
        logger.warning("Search failed: invalid folder: %s", folder)
        return "Folder does not exist or is not a directory."

    try:
        matches = [
            str(item)
            for item in folder.rglob("*")
            if item.is_file()
            and filename.casefold() in item.name.casefold()
        ]

        logger.info(
            "File search for '%s' in %s returned %d results",
            filename, folder, len(matches)
        )

        return matches if matches else "No matching files found."

    except OSError:
        logger.exception("Search failed in %s", folder)
        return "Unable to search this folder."


# --------------------------------------------------
# 4. FIND FILES BY EXTENSION
# --------------------------------------------------

def find_files(folder_path, extension):
    folder = Path(folder_path)

    if not folder.is_dir():
        logger.warning("Extension search failed: invalid folder: %s", folder)
        return "Folder does not exist or is not a directory."

    extension = extension.strip().casefold()

    if not extension:
        return "Please provide a file extension."

    if not extension.startswith("."):
        extension = "." + extension

    try:
        matches = [
            str(item)
            for item in folder.rglob("*")
            if item.is_file()
            and item.suffix.casefold() == extension
        ]

        logger.info(
            "Extension search '%s' in %s returned %d results",
            extension, folder, len(matches)
        )

        return matches if matches else "No matching files found."

    except OSError:
        logger.exception("Extension search failed in %s", folder)
        return "Unable to search this folder."


# --------------------------------------------------
# 5. FILE INFORMATION
# --------------------------------------------------

def file_information(file_path):
    path = Path(file_path)

    if not path.is_file():
        logger.warning("File information failed: invalid file: %s", path)
        return "File does not exist or is not a regular file."

    try:
        stat = path.stat()

        information = {
            "name": path.name,
            "extension": path.suffix,
            "size_bytes": stat.st_size,
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime,
            "absolute_path": str(path.resolve())
        }

        logger.info("Retrieved file information: %s", path)
        return information

    except OSError:
        logger.exception("Unable to retrieve file information: %s", path)
        return "Unable to retrieve file information."


# --------------------------------------------------
# 6. CREATE FOLDER
# --------------------------------------------------

def create_folder(folder_path):
    folder = Path(folder_path)

    if folder.exists():
        logger.warning("Create folder skipped: path already exists: %s", folder)
        return "A file or folder already exists at this path."

    try:
        folder.mkdir(parents=True, exist_ok=False)

        logger.info("Created folder: %s", folder)
        return "Folder created successfully."

    except (OSError, ValueError):
        logger.exception("Failed to create folder: %s", folder)
        return "Unable to create folder. Check the path and permissions."


# --------------------------------------------------
# 7. COPY FILE
# --------------------------------------------------

def copy_file(source, destination):
    source = Path(source)
    destination = Path(destination)

    if not source.is_file():
        logger.warning("Copy failed: source is not a file: %s", source)
        return "Source file does not exist."

    if destination.is_dir():
        destination = destination / source.name

    if destination.exists():
        logger.warning("Copy refused: destination already exists: %s", destination)
        return "Destination already exists. Choose a new name or location."

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        logger.info("Copied file: %s -> %s", source, destination)
        return "File copied successfully."

    except (OSError, shutil.Error, ValueError):
        logger.exception("Failed to copy %s to %s", source, destination)
        return "Unable to copy file. Check the paths and permissions."


# --------------------------------------------------
# 8. MOVE FILE
# --------------------------------------------------

def move_file(source, destination):
    source = Path(source)
    destination = Path(destination)

    if not source.is_file():
        logger.warning("Move failed: source is not a file: %s", source)
        return "Source file does not exist."

    if destination.is_dir():
        destination = destination / source.name

    if destination.exists():
        logger.warning("Move refused: destination already exists: %s", destination)
        return "Destination already exists. Choose a new name or location."

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))

        logger.info("Moved file: %s -> %s", source, destination)
        return "File moved successfully."

    except (OSError, shutil.Error, ValueError):
        logger.exception("Failed to move %s to %s", source, destination)
        return "Unable to move file. Check the paths and permissions."


# --------------------------------------------------
# 9. RENAME FILE
# --------------------------------------------------

def rename_file(file_path, new_name):
    path = Path(file_path)
    new_name = new_name.strip()

    if not path.is_file():
        logger.warning("Rename failed: source is not a file: %s", path)
        return "File does not exist."

    # Accept a filename, not a path to another directory.
    if (
        not new_name
        or new_name in {".", ".."}
        or Path(new_name).name != new_name
        or "/" in new_name
        or "\\" in new_name
    ):
        logger.warning("Rename refused: invalid new name: %s", new_name)
        return "Enter a valid filename without a folder path."

    new_path = path.with_name(new_name)

    if new_path.exists():
        logger.warning("Rename refused: destination exists: %s", new_path)
        return "A file or folder with that name already exists."

    try:
        path.rename(new_path)

        logger.info("Renamed file: %s -> %s", path, new_path)
        return "File renamed successfully."

    except (OSError, ValueError):
        logger.exception("Failed to rename %s", path)
        return "Unable to rename file. Check the path and permissions."


# --------------------------------------------------
# 10. DELETE FILE
# --------------------------------------------------

def delete_file(file_path):
    path = Path(file_path)

    if not path.is_file():
        logger.warning("Delete failed: source is not a file: %s", path)
        return "File does not exist."

    # Extra protection against accidentally deleting an important file.
    try:
        confirmation = input(
            f"Delete '{path.name}' permanently? Type YES to confirm: "
        )
    except (EOFError, KeyboardInterrupt):
        logger.warning("Delete cancelled: confirmation unavailable.")
        return "Delete cancelled."

    if confirmation != "YES":
        logger.info("Delete cancelled by user: %s", path)
        return "Delete cancelled."

    try:
        path.unlink()

        logger.info("Deleted file: %s", path)
        return "File deleted successfully."

    except (OSError, ValueError):
        logger.exception("Failed to delete file: %s", path)
        return "Unable to delete file. Check the path and permissions."



# def list_files(folder_path):
#     folder = Path(folder_path)

#     if not folder.exists():
#         return "Folder does not exist."

#     if not folder.is_dir():
#         return "The given path is not a folder."

#     files = []

#     for item in folder.iterdir():
#         if item.is_file():
#             files.append(item.name)

#     return files

# # ---------------------------------------------------------------------

# def search_file(folder_path, filename):
#     folder = Path(folder_path)

#     if not folder.exists():
#         return "Folder does not exist."

#     if not folder.is_dir():
#         return "The given path is not a folder."

#     results = []

#     for file in folder.rglob("*"):
#         if file.is_file() and filename.lower() in file.name.lower():
#             results.append(file)

#     return results

# # -----------------------------------------------------------------------------


# def file_information(file_path):
#     file = Path(file_path)

#     if not file.exists():
#         return "File does not exist."

#     if not file.is_file():
#         return "The given path is not a file."

#     information = {
#         "name": file.name,
#         "extension": file.suffix,
#         "size_bytes": file.stat().st_size,
#         "created": datetime.fromtimestamp(
#             file.stat().st_ctime
#         ),
#         "modified": datetime.fromtimestamp(
#             file.stat().st_mtime
#         ),
#     }

#     return information

# # ----------------------------------------------------------------

# def find_files(folder_path, extension):
#     folder = Path(folder_path)

#     if not folder.exists():
#         return "Folder does not exist."

#     if not folder.is_dir():
#         return "The given path is not a folder."

#     found_files = []

#     for file in folder.rglob("*"):
#         if file.is_file() and file.suffix.lower() == extension.lower():
#             found_files.append(file)

#     return found_files


# # -----------------------------------------------------------




# def list_folders(folder_path):
#     folder = Path(folder_path)

#     if not folder.exists():
#         return "Folder does not exist."

#     if not folder.is_dir():
#         return "The given path is not a folder."

#     folders = []

#     for item in folder.iterdir():
#         if item.is_dir():
#             folders.append(item.name)

#     return folders

# # -------------------------------------------------------------------



# def create_folder(folder_path):
#     folder = Path(folder_path)

#     if folder.exists():
#         return "Folder already exists."

#     folder.mkdir(parents=True)
#     return "Folder created successfully."

# # ------------------------------------------------------------------------







# def copy_file(source, destination):
#     source = Path(source)
#     destination = Path(destination)

#     if not source.is_file():
#         logger.warning("Copy failed: source file not found.")
#         return "Source file does not exist."

#     try:
#         shutil.copy2(source, destination)
#         logger.info("File copied: %s -> %s", source, destination)
#         return "File copied successfully."

#     except OSError:
#         logger.exception("File copy failed.")
#         return "Unable to copy file. Check the path and permissions."

# # ------------------------------------------------------------------------


# def move_file(source, destination):
#     source = Path(source)
#     destination = Path(destination)

#     if not source.exists():
#         return "Source file does not exist."

#     shutil.move(source, destination)

#     return "File moved successfully."

# # ----------------------------------------------------------------------------------

# def rename_file(file_path, new_name):
#     file_path = Path(file_path)

#     if not file_path.exists():
#         return "File does not exist."

#     new_path = file_path.parent / new_name

#     file_path.rename(new_path)

#     return "File renamed successfully."

# # ---------------------------------------------------------------------------------------------

# def delete_file(file_path):
#     file_path = Path(file_path)

#     if not file_path.exists():
#         return "File does not exist."

#     confirmation = input(
#         f"Are you sure you want to delete {file_path.name}? (yes/no): "
#     )

#     if confirmation.lower() == "yes":
#         file_path.unlink()
#         return "File deleted successfully."

#     return "Delete cancelled."

# # ---------------------------------------------------------------------------