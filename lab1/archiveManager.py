import os
import zipfile
from typing import List
from folder import Folder


class ArchiveManager(Folder):
    def archive_files(self, files_for_archiving: List[str], archive_name: str) -> None:
        try:
            with zipfile.ZipFile(self.get_full_path(archive_name), 'w') as archive:
                for file in files_for_archiving:
                    archive.write(self.get_full_path(file), os.path.basename(file))
            print(f"Файлы успешно архивированы в {archive_name} в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при архивировании файлов: {e}")

    def extract_archive(self, archive_name: str, folder: str) -> None:
        try:
            with zipfile.ZipFile(self.get_full_path(archive_name), 'r') as archive:
                archive.extractall(self.get_full_path(folder))
            print(f"Архив {archive_name} успешно разархивирован в {folder} в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при разархивировании файла: {e}")
