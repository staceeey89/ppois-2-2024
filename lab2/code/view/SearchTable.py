import tkinter as tk
from tkinter import ttk


class SearchResultsWindow:
    def __init__(self, parent, results):
        self.parent = parent
        self.results = results

        self.window = tk.Toplevel(parent)
        self.window.title("Результаты поиска")

        columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
        self.treeview = ttk.Treeview(self.window, columns=columns, show="headings")

        for col in columns:
            self.treeview.heading(col, text=col)

        for col in columns:
            self.treeview.column(col, anchor="center")

        for player in results:
            self.treeview.insert("", "end", values=(
                player.id, player.full_name, player.birth_date, player.football_team, player.home_city,
                player.team_size, player.position))

        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
