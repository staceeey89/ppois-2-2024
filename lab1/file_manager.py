from typing import List
import os
import shutil
from folder import Folder
from disk import Disk
from archiveManager import ArchiveManager


class FileManager(Disk, ArchiveManager, Folder):
    def __init__(self, base_folder: str):
        super().__init__(base_folder)

    def create_file(self, new_filename: str, content: str) -> None:
        try:
            with open(self.get_full_path(new_filename), 'w') as file:
                file.write(content)
            print(f"Файл {new_filename} успешно создан в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при создании файла: {e}")

    def copy_file(self, source_filename: str, destination_filename: str) -> None:
        try:
            source_path = self.get_full_path(source_filename)
            destination_path = self.get_full_path(destination_filename)

            shutil.copy(source_path, destination_path)

            print(f"Файл {source_filename} успешно скопирован в {destination_filename} в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при копировании файла: {e}")

    def delete_file(self, delete: str) -> None:
        try:
            os.remove(self.get_full_path(delete))
            print(f"Файл {delete} успешно удален из {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

    def move_file(self, file: str, target_folder: str) -> None:
        try:
            shutil.move(self.get_full_path(file), self.get_full_path(target_folder))
            print(f"Файл {file} успешно перемещен в папку {target_folder}")
        except Exception as e:
            print(f"Ошибка при перемещении файла: {e}")

    def backup_files(self, files: List[str], folder: str) -> None:
        try:
            if not os.path.exists(self.get_full_path(folder)):
                os.makedirs(self.get_full_path(folder))

            for file in files:
                shutil.copy(self.get_full_path(file),
                            self.get_full_path(os.path.join(folder, os.path.basename(file))))
            print(f"Файлы успешно скопированы в папку резервного копирования {folder} в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при создании резервной копии файлов: {e}")

    def manage_file_permissions(self, file: str, access_choice: str) -> None:
        if access_choice == '1':
            os.chmod(self.get_full_path(file), 0o444)
            print(f"Права доступа к файлу {file} изменены: только чтение.")
        elif access_choice == '2':
            os.chmod(self.get_full_path(file), 0o222)
            print(f"Права доступа к файлу {file} изменены: только запись.")
        else:
            print("Некорректный выбор. Права доступа не изменены.")

    def edit_file_content(self, file_edit: str, updated_content: str) -> None:
        try:
            with open(self.get_full_path(file_edit), 'w') as file:
                file.write(updated_content)
            print(f"Содержимое файла {file_edit} успешно изменено.")
        except Exception as e:
            print(f"Ошибка при изменении содержимого файла: {e}")

    def file_info(self, file_inspect: str) -> str:
        try:
            full_path = self.get_full_path(file_inspect)
            result = []

            stat_info = os.stat(full_path)
            result.append(f"Информация о файле {file_inspect}:")
            result.append(f"Размер: {stat_info.st_size} байт")

            file_extension = os.path.splitext(file_inspect)[1]
            result.append(f"Расширение файла: {file_extension}")

            with open(full_path, 'r') as file:
                content_preview = ''.join(file.readlines()[:10])
                result.append(f"Содержимое файла:\n{content_preview}")

            return '\n'.join(result)
        except FileNotFoundError:
            return f"Файл {file_inspect} не найден."
        except Exception as e:
            return f"Ошибка при получении информации о файле: {e}"
