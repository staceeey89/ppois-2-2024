# Лабораторная работа №1

## Цель: 
1. Изучить основные возможности языка Python для разработки программных систем с интерфейсом командной строки (CLI)
2. Разработать программную систему на языке Python согласно описанию предметной области
## Задача:
Разработать программную систему на языке Python. Модель файловой системы.

<em>
Предметная область: организация и управление файлами на компьютере.
Важные сущности: файл, папка, диск.
Операции: операция создания, копирования и удаления файлов, операция перемещения и организации в папки, операция управления правами доступа, операция архивирования и разархивирования, операция резервного копирования.
</em>

## Описание программы:

# класс FileManager методы:

- `def __init__(self, base_folder: str)` - конструктор класса
- `def create_file(self, new_filename: str, content: str)` - создание файла
- `def copy_file(self, source_filename: str, destination_filename: str)` - копирование файла
- `def delete_file(self, delete: str)` - удаление файла
- `def move_file(self, file: str, target_folder: str)` - перемещение файла
- `def backup_files(self, files: List[str], folder: str)` - резервное копирование файлов
- `def manage_file_permissions(self, file: str, access_choice: str)` - управление правами доступа файла
- `def edit_file_content(self, file_edit: str, updated_content: str)` - поменять содержимое файла
- `def file_info(self, file_inspect: str)` - узнать информацию о файле


# класс Folder методы:

- `def __init__(self, base_folder: str)` - конструктор класса
- `def get_full_path(self, filename: str)` - узнать полный путь
- `def set_base_folder(self, base_folder: str)` - установить базовую папку
- `def change_base_folder(self, new_folder: str)` - поменять базовую папку

# класс Disk методы:

- `def move_to_another_disk(self, source_file2: str, destination_disks: str)` - переместить на другой диск

# класс ArchiveManager методы:

- `def archive_files(self, files_for_archiving: List[str], archive_name: str)` - архивировать файлы
- `def extract_archive(self, archive_name: str, folder: str)` - разархивировать файлы

# Меню

на основе всех методов получаемое такой функционал

![2024-03-12](https://github.com/NikitaGryn/PPOIS_python/assets/114168438/209fe196-a07a-42cb-b7b6-b63f3ee53a73)


## Диаграмма классов
На основе выделенных сущностей и состояний созданы следующие классы:

![image_2024-03-11_14-33-04](https://github.com/NikitaGryn/PPOIS_python/assets/114168438/36ff1df1-253f-4956-ba59-c5859f3315a9)

## Диаграмма состояний

![2024-03-13_13-36-14](https://github.com/NikitaGryn/PPOIS_python/assets/114168438/f82f6761-abac-4c88-a28c-e6f26797401a)


## Тестирование:
Программа успешно прошла unit-тестирование:

![2024-03-11 (1)](https://github.com/NikitaGryn/PPOIS_python/assets/114168438/cf3aab82-7db7-4f2b-be31-ea39426d3aa5)

в результате чего получилось

![2024-03-11 (3)](https://github.com/NikitaGryn/PPOIS_python/assets/114168438/24192c8e-f540-4b9d-b1ff-0b58287d3147)

## Вывод:
В результате выполнения лабораторной работы были изучены ключевые возможности языка Python для создания программ с интерфейсом командной строки. Затем была успешно разработана программная система на Python, моделирующая функциональность файловой системы. Это позволило понять применимость Python для разработки эффективных и удобных CLI-приложений и создать работоспособную систему для управления задачами и данными в рамках модели файловой системы.
