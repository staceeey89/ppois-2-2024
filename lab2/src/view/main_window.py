import tkinter
import tkinter.ttk

from src.view.abstract.window import Window
import src.utils as utils


class MainWindow(Window):
    window_title = "Main window"

    events = (
        # file commands events
        "<<save_to_xml_command_click>>",
        "<<load_from_xml_command_click>>",
        # data base commands events
        "<<create_data_base_command_click>>",
        "<<open_data_base_command_click>>",
        "<<commit_data_base_command_click>>",
        "<<close_data_base_button_click>>",
        # record commands events
        "<<add_user_command_click>>",
        "<<search_user_command_click>>",
        "<<delete_user_command_click>>",
        # buttons events
        "<<first_button_click>>",
        "<<prev_button_click>>",
        "<<inc_button_click>>",
        "<<dec_button_click>>",
        "<<next_button_click>>",
        "<<last_button_click>>",
        # checkbuttons events
        "<<tree_view_checkbutton_click>>",
    )

    users_tree_columns = {
        "name": "Имя",
        "surname": "Фамилия",
        "patronymic": "Отчество",
        "account": "Аккаунт",
        "address": "Адрес",
        "mobile": "Мобильный",
        "landline": "Городской",
    }

    frame_pack_args = {
        "fill": tkinter.BOTH,
        "side": tkinter.TOP,
    }

    tree_pack_args = {
        "fill": tkinter.BOTH,
        "side": tkinter.LEFT,
        "expand": True,
        "padx": 10,
        "pady": 10,
    }

    button_pack_args = {
        "fill": tkinter.X,
        "side": tkinter.LEFT,
        "expand": True,
        "padx": 10,
        "pady": 10,
        "ipadx": 2,
        "ipady": 2,
    }

    indexes = {
        "page size",
        "total records",
        "current page",
        "total pages",
    }

    def _build(self) -> None:
        # - file menu
        file_menu = tkinter.Menu(tearoff=0)
        file_menu.add_command(
            label="Save to XML",
            command=lambda: self._notify("<<save_to_xml_command_click>>"),
        )
        file_menu.add_command(
            label="Load from XML",
            command=lambda: self._notify("<<load_from_xml_command_click>>"),
        )
        # - db menu
        db_menu = tkinter.Menu(tearoff=0)
        db_menu.add_command(
            label="Create",
            command=lambda: self._notify("<<create_data_base_command_click>>")
        )
        db_menu.add_command(
            label="Open",
            command=lambda: self._notify("<<open_data_base_command_click>>")
        )
        db_menu.add_command(
            label="Commit",
            command=lambda: self._notify("<<commit_data_base_command_click>>")
        )
        # - record menu
        record_menu = tkinter.Menu(tearoff=0)
        record_menu.add_command(
            label="Add user",
            command=lambda: self._notify("<<add_user_command_click>>")
        )
        record_menu.add_command(
            label="Delete users",
            command=lambda: self._notify("<<delete_user_command_click>>")
        )
        record_menu.add_command(
            label="Search users", command=lambda:
            self._notify("<<search_user_command_click>>")
        )
        # main menu
        main_menu = tkinter.Menu()
        main_menu.add_cascade(
            label="File",
            menu=file_menu
        )
        main_menu.add_cascade(
            label="Record",
            menu=record_menu
        )
        main_menu.add_cascade(
            label="Data base",
            menu=db_menu
        )

        # window configuration
        self.config(menu=main_menu)

        tree_frame = tkinter.Frame()
        tree_frame.pack(**self.frame_pack_args, expand=True)

        self.users_tree = utils.build_tree(
            self.users_tree_columns,
            tree_frame,
            self.tree_pack_args
        )

        button_frame = tkinter.Frame()
        button_frame.pack(**self.frame_pack_args)

        # button to go to the first page
        first_button = tkinter.Button(
            button_frame,
            text="First",
            underline=0,
            command=lambda: self._notify("<<first_button_click>>")
        )
        first_button.pack(**self.button_pack_args)

        # button to go to the previous page
        prev_button = tkinter.Button(
            button_frame,
            text="Prev",
            underline=0,
            command=lambda: self._notify("<<prev_button_click>>")
        )
        prev_button.pack(**self.button_pack_args)

        # decrease page size button
        dec_button = tkinter.Button(
            button_frame,
            text='-',
            command=lambda: self._notify("<<dec_button_click>>")
        )
        dec_button.pack(**self.button_pack_args)

        # indexes start
        indexes_frame = tkinter.Frame(button_frame)

        self.indexes = {index: tkinter.IntVar() for index in self.indexes}
        for index, var in self.indexes.items():
            frame = tkinter.Frame(indexes_frame)

            label = tkinter.Label(
                frame,
                text=f"{index.capitalize()}: ",
            )
            label.pack(side=tkinter.LEFT)

            index_label = tkinter.Label(
                frame,
                textvariable=var,
            )
            index_label.pack(side=tkinter.LEFT)

            frame.pack()

        self.tree_view_enabled = tkinter.BooleanVar(indexes_frame)
        tree_view_checkbutton = tkinter.Checkbutton(
            variable=self.tree_view_enabled,
            text="Tree view",
            command=lambda: self._notify("<<tree_view_checkbutton_click>>")
        )
        tree_view_checkbutton.pack()

        indexes_frame.pack(**self.button_pack_args)
        # indexes end

        # increase page size button
        inc_button = tkinter.Button(
            button_frame,
            text='+',
            command=lambda: self._notify("<<inc_button_click>>")
        )
        inc_button.pack(**self.button_pack_args)

        # button to go to the next page
        next_button = tkinter.Button(
            button_frame,
            text="Next",
            underline=0,
            command=lambda: self._notify("<<next_button_click>>")
        )
        next_button.pack(**self.button_pack_args)

        # button to go to the last page
        last_button = tkinter.Button(
            button_frame,
            text="Last",
            underline=0,
            command=lambda: self._notify("<<last_button_click>>")
        )
        last_button.pack(**self.button_pack_args)


if __name__ == "__main__":
    MainWindow().mainloop()
