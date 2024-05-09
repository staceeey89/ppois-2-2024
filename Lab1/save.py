import pickle


def save_changes(OS):
    with open("info.pickle", "wb") as file:
        pickle.dump(OS, file)
