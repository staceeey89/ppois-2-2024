import unittest
import os
from file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_base_folder = "Test"
        if not os.path.exists(self.test_base_folder):
            os.makedirs(self.test_base_folder)

        self.file_manager = FileManager(base_folder=self.test_base_folder)

    def test_create_file(self):
        file_name = "test_file_2.txt"
        content = "Test 1. Create file"
        self.file_manager.create_file(file_name, content)
        full_path = os.path.join(self.test_base_folder, file_name)
        self.assertTrue(os.path.isfile(full_path))

    def test_copy_file(self):
        source_file_name = "test_file_1.txt"
        destination_filename = "test_file_3.txt"
        destination_path = os.path.join(self.test_base_folder, destination_filename)

        source_content = "Test 2. Copy file"
        self.file_manager.create_file(source_file_name, source_content)

        self.file_manager.copy_file(source_file_name, destination_filename)
        self.assertTrue(os.path.isfile(destination_path))

    def test_archive_files_and_delete(self):
        files_to_archive = ["test_file_4.txt", "test_file_5.txt", "test_file_6.txt"]
        archive_name = "archive.zip"

        for file_name in files_to_archive:
            content = "Test 3. Archive file"
            self.file_manager.create_file(file_name, content)

        self.file_manager.archive_files(files_to_archive, archive_name)
        archive_path = os.path.join(self.test_base_folder, archive_name)
        self.assertTrue(os.path.isfile(archive_path))

        for file_name in files_to_archive:
            self.file_manager.delete_file(file_name)

        for file_name in files_to_archive:
            full_path = os.path.join(self.test_base_folder, file_name)
            self.assertFalse(os.path.isfile(full_path))

    def test_extract_archive(self):
        source_file = "test_file_7.txt"
        destination_folder = "extracted"
        archive_name = "archive2.zip"

        content = "Test 4. Extract archive"
        self.file_manager.create_file(source_file, content)

        self.file_manager.archive_files([source_file], archive_name)

        self.file_manager.extract_archive(archive_name, destination_folder)
        extracted_file_path = os.path.join(self.test_base_folder, destination_folder, source_file)
        self.assertTrue(os.path.isfile(extracted_file_path))

    def test_file_info(self):
        file_name = "test_file_8.txt"
        content = "Test 5. File info"
        self.file_manager.create_file(file_name, content)

        file_extension = ".txt"
        self.assertTrue(file_name.endswith(file_extension), f"Файл не имеет расширения {file_extension}.")

    def test_delete_file(self):
        file_name = "test_file_to_delete.txt"
        content = "Test 6. Content of the file to delete."
        file_path = os.path.join(self.test_base_folder, file_name)
        self.file_manager.create_file(file_name, content)

        self.assertTrue(os.path.isfile(file_path))

        self.file_manager.delete_file(file_name)

        self.assertFalse(os.path.isfile(file_path))

    def test_move_file(self):
        source_file = "test_file_move.txt"
        content = "Test 7. Content of the file to be moved."
        self.file_manager.create_file(source_file, content)

        source_path = os.path.join(self.test_base_folder, source_file)
        self.assertTrue(os.path.isfile(source_path))

        target_folder = "Folder to move"

        self.file_manager.create_folder(target_folder)

        self.file_manager.move_file(source_file, target_folder)

        target_path = os.path.join(self.test_base_folder, target_folder)
        moved_file_path = os.path.join(target_path, source_file)
        self.assertTrue(os.path.isfile(moved_file_path))

    def test_move_to_another_disk(self):
        source_file = "test_file_move_to_disk.txt"
        content = "Test 8. Content of the file to be moved to another disk."
        self.file_manager.create_file(source_file, content)
        destination_disk = "D:\\"

        self.file_manager.move_to_another_disk(source_file, destination_disk)

        destination_path = os.path.join(destination_disk, source_file)
        self.assertTrue(os.path.isfile(destination_path))


if __name__ == '__main__':
    unittest.main()
