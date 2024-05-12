import tkinter
import tkinter.ttk as ttk

from src.view.abstract.subwindow import Subwindow
import src.utils as utils


class SearchUserWindow(Subwindow):
    window_title = "Searching users"

    events = (
        "<<ok_button_click>>",
        "<<find_button_click>>",
    )

    search_args: dict[str, tkinter.StringVar] = {}

    tree_columns = {
        "name": "Имя",
        "surname": "Фамилия",
        "patronymic": "Отчество",
        "account": "Счёт",
        "address": "Адрес",
        "mobile": "Мобильный",
        "landline": "Городской",
    }

    label_pack_args = {
        "padx": 5,
        "pady": 5,
        "ipadx": 2,
        "ipady": 2,
    }

    entry_pack_args = {
        "padx": 5,
        "pady": 5,
        "ipadx": 2,
        "ipady": 2,
    }

    button_pack_args = {
        "side": tkinter.LEFT,
        "expand": True,
        "fill": tkinter.BOTH,
        "padx": 10,
        "pady": 10,
        "ipadx": 2,
        "ipady": 2,
    }

    tree_pack_args = {
        "padx": 10,
        "pady": 10,
    }

    frame_pack_args = {
    }

    notebook_pack_args = {
        "expand": True,
        "fill": tkinter.BOTH,
        "padx": 10,
        "pady": 10,
    }

    def _build(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.add(
            self.__frame_for_search_by("surname", "mobile number"),
            text="Search by surname and mobile number"
        )
        self.notebook.add(
            self.__frame_for_search_by("account", "address"),
            text="Search by account and address"
        )
        self.notebook.add(
            self.__frame_for_search_by(
                "name",
                "surname",
                "patronymic",
                "numbers that included in the one of numbers"
            ),
            text="Search by surname and mobile number"
        )
        self.notebook.pack(**self.notebook_pack_args)

        tree_frame = tkinter.Frame(self)
        self.search_tree = utils.build_tree(
            self.tree_columns,
            tree_frame,
            self.tree_pack_args
        )
        tree_frame.pack(**self.frame_pack_args)

        button_frame = tkinter.Frame(self)

        find_button = tkinter.Button(
            button_frame,
            text="Find",
            command=lambda: self._notify("<<find_button_click>>")
        )
        find_button.pack(**self.button_pack_args)

        ok_button = tkinter.Button(
            button_frame,
            text="Ok",
            command=lambda: self._notify("<<ok_button_click>>")
        )
        ok_button.pack(**self.button_pack_args)

        button_frame.pack(**self.frame_pack_args, fill=tkinter.X)

    def __frame_for_search_by(self, *args) -> tkinter.Frame:
        entries_frame = tkinter.Frame(self)
        for arg in args:
            frame = tkinter.Frame(entries_frame)

            label = tkinter.Label(frame, text=arg.capitalize())
            label.pack(**self.label_pack_args)

            if arg in self.search_args:
                var = self.search_args[arg]
            else:
                var = tkinter.StringVar(self)
                self.search_args[arg] = var
            entry = tkinter.Entry(frame, textvariable=var)
            entry.pack(**self.entry_pack_args)

            frame.pack(
                **self.frame_pack_args,
                side=tkinter.LEFT,
                expand=True,
            )
        entries_frame.pack(**self.frame_pack_args, fill=tkinter.BOTH)
        return entries_frame


if __name__ == "__main__":
    window = SearchUserWindow(None)
    window.mainloop()
