from pathlib import Path
import os

def validate_path(path):

    print("🔐 SECURITY: validate_path() is running")

    if not path or not path.strip():
        return False, "Path cannot be empty."

    if not os.path.isabs(path):
        return False, "Please provide an absolute path."

    return True, "Path is valid."
# def validate_path(path):
#     path = Path(path)

#     if not path.exists():
#         return False, "Path does not exist."

#     return True, "Path is valid."

# -------------------------------------------


def validate_file(file_path):

    print("🔐 SECURITY: validate_file() is running")

    path = Path(file_path)

    if not path.exists():
        return False, "File does not exist."

    if not path.is_file():
        return False, "The given path is not a file."

    return True, "File is valid."

# ---------------------------------------------------------------------------

def validate_folder(folder_path):

    path = Path(folder_path)

    if not path.exists():
        return False, "Folder does not exist."

    if not path.is_dir():
        return False, "The given path is not a folder."

    return True, "Folder is valid."

# -----------------------------------------------------------------------------

def confirm_action(action, target):

    print("\n⚠️ WARNING")
    print(f"Action: {action}")
    print(f"Target: {target}")

    answer = input("Do you want to continue? (yes/no): ")

    return answer.lower() == "yes"

if __name__ == "__main__":

    path = input("Enter a file path: ")

    valid, message = validate_file(path)

    print("Valid:", valid)
    print("Message:", message)