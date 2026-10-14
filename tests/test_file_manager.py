
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from app.file_manager import (
    list_files,
    list_folders,
    search_file,
    file_information,
    create_folder,
    copy_file,
    move_file,
    rename_file,
    delete_file,
)


class TestFileManager(unittest.TestCase):

    def setUp(self):
        # Create a fresh temporary folder for each test
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        self.source = self.root / "source"
        self.destination = self.root / "destination"

        self.source.mkdir()
        self.destination.mkdir()

        # Create sample files and folders
        (self.source / "test.txt").write_text(
            "Hello Jarvis", encoding="utf-8"
        )
        (self.source / "report.pdf").write_text(
            "Sample report", encoding="utf-8"
        )
        (self.source / "College").mkdir()

    def tearDown(self):
        # Clean up temporary files after each test
        self.temp.cleanup()

    # 1. Test list_files()
    def test_list_files(self):
        result = list_files(self.source)

        self.assertIn("test.txt", result)
        self.assertIn("report.pdf", result)

    # 2. Test list_folders()
    def test_list_folders(self):
        result = list_folders(self.source)

        self.assertIn("College", result)

    # 3. Test search_file()
    def test_search_file(self):
        result = search_file(self.source, "test.txt")

        self.assertIn("test.txt", str(result))

    # 4. Test file_information()
    def test_file_information(self):
        file_path = self.source / "test.txt"

        result = file_information(file_path)

        self.assertIsNotNone(result)
        self.assertIn("test.txt", str(result))

    # 5. Test create_folder()
    def test_create_folder(self):
        new_folder = self.root / "Jarvis_Test"

        result = create_folder(new_folder)

        self.assertTrue(new_folder.is_dir())

    # 6. Test copy_file()
    def test_copy_file(self):
        source_file = self.source / "test.txt"
        destination_file = self.destination / "test.txt"

        result = copy_file(source_file, destination_file)

        self.assertTrue(destination_file.is_file())
        self.assertEqual(
            source_file.read_text(encoding="utf-8"),
            destination_file.read_text(encoding="utf-8"),
        )

        # Copy should preserve the original
        self.assertTrue(source_file.is_file())

    # 7. Test move_file()
    def test_move_file(self):
        source_file = self.source / "report.pdf"
        destination_file = self.destination / "report.pdf"

        result = move_file(source_file, destination_file)

        self.assertTrue(destination_file.is_file())
        self.assertFalse(source_file.exists())

    # 8. Test rename_file()
    def test_rename_file(self):
        old_file = self.source / "test.txt"
        new_name = "renamed.txt"

        result = rename_file(old_file, new_name)

        self.assertTrue((self.source / new_name).is_file())
        self.assertFalse(old_file.exists())

    # 9. Test delete_file() when user confirms
    @patch("builtins.input", return_value="YES")
    def test_delete_file_confirmed(self, mock_input):
        file_path = self.source / "test.txt"

        result = delete_file(file_path)

        self.assertFalse(file_path.exists())
        mock_input.assert_called_once()

    # 10. Test delete_file() when user cancels
    @patch("builtins.input", return_value="NO")
    def test_delete_file_cancelled(self, mock_input):
        file_path = self.source / "test.txt"

        result = delete_file(file_path)

        self.assertTrue(file_path.is_file())
        mock_input.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)



# import unittest
# import tempfile
# from pathlib import Path

# from app.file_manager import list_files


# class TestFileManager(unittest.TestCase):

#     def test_list_files(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             folder = Path(temp_dir)

#             (folder / "test.txt").write_text(
#                 "Hello Jarvis", encoding="utf-8"
#             )

#             result = list_files(folder)

#             self.assertIn("test.txt", result)


# if __name__ == "__main__":
#     unittest.main()