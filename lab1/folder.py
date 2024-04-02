import os


class Folder:
    def __init__(self, base_folder: str):
        self.base_folder = base_folder

    def get_full_path(self, filename: str) -> str:
        return os.path.join(self.base_folder, filename)

    def set_base_folder(self, base_folder: str) -> None:
        self.base_folder = base_folder

    def change_base_folder(self, new_folder: str) -> None:
        try:
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            self.set_base_folder(new_folder)
            print(f"Базовая папка изменена на {new_folder}.")
        except Exception as e:
            print(f"Ошибка при изменении базовой папки: {e}")

    def create_folder(self, folder_name: str) -> None:
        try:
            folder_path = self.get_full_path(folder_name)
            os.makedirs(folder_path)
            print(f"Папка {folder_name} успешно создана в {self.base_folder}.")
        except Exception as e:
            print(f"Ошибка при создании папки {folder_name}: {e}")