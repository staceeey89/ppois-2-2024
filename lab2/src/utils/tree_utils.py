import tkinter
import tkinter.ttk

from src.model.user import User


def add_user_to_tree(tree,  user: User):
    tree.insert(
        "",
        tkinter.END,
        iid=f"{user.name} {user.surname} {user.patronymic}",
        text=f"{user.name} {user.surname} {user.patronymic}",
        values=(
            user.name,
            user.surname,
            user.patronymic,
            user.account,
            user.address,
            user.mobile_number,
            user.landline_number,
        ),
    )
    for field, value in user:
        tree.insert(
            f"{user.name} {user.surname} {user.patronymic}",
            tkinter.END,
            text=value,
        )


def clear_tree(tree):
    for child in tree.get_children(""):
        tree.delete(child)


def build_tree(columns: dict[str, str], frame, pack_args, users: list[User] | None = None) -> tkinter.ttk.Treeview:
    tree = tkinter.ttk.Treeview(
        frame,
        columns=list(columns),
        show="headings"
    )
    tree.column("#0", width=500)
    for column, head in columns.items():
        tree.heading(column, text=head)
    tree.pack(**pack_args)
    if users:
        for user in users:
            add_user_to_tree(tree, user)
    return tree
