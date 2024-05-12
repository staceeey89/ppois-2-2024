from file_manager import FileManager


def main_menu():
    file_manager = FileManager(base_folder="D:\\labs\\pythonProject_filemanager")

    while True:
        print("\nМеню:")
        print("1. Создать файл")
        print("2. Копировать файл")
        print("3. Удалить файл")
        print("4. Переместить файл")
        print("5. Архивировать файлы")
        print("6. Разархивировать файлы")
        print("7. Создать резервную копию файлов")
        print("8. Управление правами доступа к файлу")
        print("9. Изменить содержимое файла")
        print("10. Изменить базовую папку")
        print("11. Переместить на другой диск")
        print("12. Вывести информацию о файле")
        print("13. Создать папку")
        print("0. Выйти")

        user_choice = input("Выберите операцию (введите номер): ")

        if user_choice == '1':
            new_file_name = input("Введите имя файла: ")
            file_content = input("Введите содержимое файла: ")
            file_manager.create_file(new_file_name, file_content)
        elif user_choice == '2':
            source_file = input("Введите имя исходного файла: ")
            destination_file = input("Введите имя целевого файла: ")
            file_manager.copy_file(source_file, destination_file)
        elif user_choice == '3':
            file_to_delete = input("Введите имя файла для удаления: ")
            file_manager.delete_file(file_to_delete)
        elif user_choice == '4':
            source_file = input("Введите имя исходного файла: ")
            destination_folder = input("Введите имя целевой папки: ")
            file_manager.move_file(source_file, destination_folder)
        elif user_choice == '5':
            files_to_archive = input("Введите имена файлов для архивации (через запятую): ").split(', ')
            archive_filename = input("Введите имя архива: ")
            file_manager.archive_files(files_to_archive, archive_filename)
        elif user_choice == '6':
            archive_filename = input("Введите имя архива для разархивации: ")
            extraction_folder = input("Введите имя папки для разархивации: ")
            file_manager.extract_archive(archive_filename, extraction_folder)
        elif user_choice == '7':
            files_to_backup = input("Введите имена файлов для резервного копирования (через запятую): ").split(', ')
            backup_folder = input("Введите имя папки для резервного копирования: ")
            file_manager.backup_files(files_to_backup, backup_folder)
        elif user_choice == '8':
            file_to_manage = input("Введите имя файла для управления правами доступа: ")
            access_choice = input(
                "Выберите права доступа:\n1. Только чтение (r)\n2. Чтение и запись (w)\nВведите номер права доступа: ")
            file_manager.manage_file_permissions(file_to_manage, access_choice)
        elif user_choice == '9':
            file_to_edit = input("Введите имя файла для изменения содержимого: ")
            new_content = input("Введите новое содержимое файла: ")
            file_manager.edit_file_content(file_to_edit, new_content)
        elif user_choice == '10':
            new_base_folder = input("Введите новый путь к базовой папке: ")
            file_manager.change_base_folder(new_base_folder)
        elif user_choice == '11':
            source_file = input("Введите имя файла для перемещения: ")
            destination_disk = input("Введите букву диска (пример: D:): ")
            file_manager.move_to_another_disk(source_file, destination_disk)
        elif user_choice == '12':
            file_to_inspect = input("Введите имя файла для получения информации: ")
            file_info_result = file_manager.file_info(file_to_inspect)
            print(file_info_result)
        elif user_choice == '13':
            new_folder_name = input("Введите имя новой папки: ")
            file_manager.create_folder(new_folder_name)
        elif user_choice == '0':
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите корректный номер операции.")


if __name__ == "__main__":
    main_menu()
