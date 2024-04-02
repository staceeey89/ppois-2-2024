import os
import shutil
from folder import Folder


class Disk(Folder):
    def move_to_another_disk(self, source_file2: str, destination_disks: str) -> None:
        try:
            destination_path = os.path.join(destination_disks, os.path.basename(source_file2))
            shutil.move(self.get_full_path(source_file2), destination_path)
            print(f"Файл {source_file2} успешно перемещен на диск {destination_disks}.")
        except Exception as e:
            print(f"Ошибка при перемещении файла на другой диск: {e}")