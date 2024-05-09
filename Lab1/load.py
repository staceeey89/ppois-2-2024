import pickle


def load_changes():
    with open("info.pickle", "rb") as file:
        try:
            os = pickle.load(file)
            return os
        except EOFError:
            # Обработка ошибки, если файл не содержит достаточного количества данных
            print("File does not contain enough data.")
            return None
