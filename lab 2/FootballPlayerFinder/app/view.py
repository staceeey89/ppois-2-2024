import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import TYPE_CHECKING

from anytree import Node, RenderTree
from tkcalendar import DateEntry

if TYPE_CHECKING:
    from app.controller import Controller


class View:
    def __init__(self, root, controller):
        self.switch_db_dialog = None
        self.result_tree = None
        self.search_button = None
        self.delete_frame = None
        self.position_entry = None
        self.squad_entry = None
        self.additional_date_entry = None
        self.home_city_entry = None
        self.full_name_entry = None
        self.football_team_entry = None
        self.birth_date_entry = None
        self.additional_criteria_dropdown = None
        self.additional_criteria = None
        self.additional_search_entry = None
        self.additional_search_criteria_frame = None
        self.add_criteria_button = None
        self.date_entry = None
        self.search_entry = None
        self.criteria = None
        self.delete_result_tree = None
        self.search_result_tree = None
        self.player_tree = None
        self.search_window = None
        self.root = root
        self.root.resizable(width=False, height=False)
        self.controller: Controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.player_tree = ttk.Treeview(self.root, columns=(
            "Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"), show="headings")
        self.player_tree.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        first_button = ttk.Button(self.root, text="First", command=lambda: self.controller.first_page("main"))
        first_button.grid(row=1, column=2, padx=(150, 200), pady=5, sticky="w")

        prev_button = ttk.Button(self.root, text="Previous", command=lambda: self.controller.prev_page("main"))
        prev_button.grid(row=1, column=1, padx=(0, 10), pady=5)

        next_button = ttk.Button(self.root, text="Next", command=lambda: self.controller.next_page("main"))
        next_button.grid(row=1, column=2, padx=(100, 150), pady=5)

        last_button = ttk.Button(self.root, text="Last", command=lambda: self.controller.last_page("main"))
        last_button.grid(row=1, column=1, padx=(0, 0), pady=5, sticky="e")

        headers = ["Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"]
        for header in headers:
            self.player_tree.heading(header, text=header)

        header_menu = tk.Menu(self.root)
        self.root.config(menu=header_menu)

        options_menu = tk.Menu(header_menu, tearoff=0)
        header_menu.add_cascade(label="Options", menu=options_menu)

        options_menu.add_command(label="Add Player", command=self.show_add_player_window)
        options_menu.add_command(label="Search Players", command=self.show_search_window)
        options_menu.add_command(label="Delete Players", command=self.show_delete_window)
        options_menu.add_command(label="Players Tree", command=self.show_players_tree)

        settings_menu = tk.Menu(header_menu, tearoff=0)
        header_menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Players limit",
                                  command=self.show_players_limit_dialog)
        settings_menu.add_command(label="Switch DB",
                                  command=self.show_switch_db_dialog)

    def show_players_limit_dialog(self):
        # Create a dialog window
        limit_dialog = tk.Toplevel(self.root)
        limit_dialog.title("Set Players Limit")
        limit_dialog.resizable(width=False, height=False)

        limit_dialog.grab_set()

        # Create a label and entry for user input
        limit_label = tk.Label(limit_dialog, text="Enter the number of players per page:")
        limit_label.grid(row=0, column=0, padx=10, pady=5)

        limit_entry = ttk.Entry(limit_dialog)
        limit_entry.grid(row=0, column=1, padx=10, pady=5)

        # Function to handle setting the players limit
        def set_players_limit():
            limit = limit_entry.get()
            if limit.isdigit():
                self.controller.set_players_limit(int(limit))
                limit_dialog.destroy()
            else:
                messagebox.showerror("Error", "Please enter a valid number.")

        # Create a button to confirm the limit
        confirm_button = ttk.Button(limit_dialog, text="Set Limit", command=set_players_limit)
        confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def show_switch_db_dialog(self):
        # Create a dialog window
        self.switch_db_dialog = tk.Toplevel(self.root)
        self.switch_db_dialog.title("Switch Database")
        self.switch_db_dialog.resizable(width=False, height=False)

        # Function to handle the database switch to XML
        def switch_to_xml():
            file_path = tk.filedialog.askopenfilename(title="Select XML File", filetypes=[("XML files", "*.xml")])
            if file_path:
                self.controller.switch_to_xml(file_path)

        # Create buttons for MySQL and XML options
        mysql_button = ttk.Button(self.switch_db_dialog, text="MySQL",
                                  command=self.controller.switch_to_sql)
        mysql_button.pack(pady=5)

        xml_button = ttk.Button(self.switch_db_dialog, text="XML", command=switch_to_xml)
        xml_button.pack(pady=5)

    def show_search_window(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search Players")
        self.search_window.resizable(width=False, height=False)

        search_frame = tk.Frame(self.search_window)
        search_frame.pack(padx=10, pady=10)
        search_frame.grab_set()

        search_criteria_frame = tk.Frame(search_frame)
        search_criteria_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.criteria = tk.StringVar()
        criteria_dropdown = ttk.Combobox(search_criteria_frame, textvariable=self.criteria,
                                         values=["Full Name", "Birth Date", "Position", "Squad", "Football Team",
                                                 "Home City"])
        criteria_dropdown.set("Select Criteria")
        criteria_dropdown.grid(row=0, column=1, padx=10, pady=5)

        criteria_dropdown.bind("<<ComboboxSelected>>", lambda event: self.toggle_date_entry())

        self.search_entry = ttk.Entry(search_criteria_frame, width=50)
        self.date_entry = DateEntry(search_criteria_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)

        self.toggle_date_entry()

        self.add_criteria_button = ttk.Button(search_criteria_frame, text="+", command=self.toggle_additional_criteria)
        self.add_criteria_button.grid(row=0, column=2, padx=10, pady=5)

        self.additional_search_criteria_frame = tk.Frame(search_frame)

        self.additional_search_entry = ttk.Entry(self.additional_search_criteria_frame, width=50)
        self.additional_search_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.additional_criteria = tk.StringVar()
        self.additional_criteria_dropdown = ttk.Combobox(self.additional_search_criteria_frame,
                                                         textvariable=self.additional_criteria,
                                                         values=["Full Name", "Birth Date", "Position", "Squad",
                                                                 "Football Team",
                                                                 "Home City"])
        self.additional_criteria_dropdown.grid(row=0, column=1, padx=10, pady=5,
                                               sticky="w")

        self.additional_search_criteria_frame.grid(row=1, column=1, columnspan=3, padx=10, pady=5)
        self.additional_search_criteria_frame.grid_forget()

        self.additional_criteria_dropdown.bind("<<ComboboxSelected>>",
                                               lambda event: self.toggle_additional_date_entry())

        self.additional_date_entry = DateEntry(self.additional_search_criteria_frame, width=12, background='darkblue',
                                               foreground='white', borderwidth=2)

        self.toggle_additional_date_entry()

        self.search_result_tree = ttk.Treeview(search_frame, columns=(
            "Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"), show="headings")
        self.search_result_tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        headers = ["Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"]
        for header in headers:
            self.search_result_tree.heading(header, text=header)

        search_button = ttk.Button(search_frame, text="Search",
                                   command=lambda: self.controller.search_players("search"))
        search_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        first_button = ttk.Button(search_frame, text="First", command=lambda: self.controller.first_page("search"))
        first_button.grid(row=3, column=2, padx=(150, 200), pady=5, sticky="w")

        prev_button = ttk.Button(search_frame, text="Previous",
                                 command=lambda: self.controller.prev_page("search"))
        prev_button.grid(row=3, column=1, padx=(0, 10), pady=5)

        next_button = ttk.Button(search_frame, text="Next", command=lambda: self.controller.next_page("search"))
        next_button.grid(row=3, column=2, padx=(100, 150), pady=5)

        last_button = ttk.Button(search_frame, text="Last", command=lambda: self.controller.last_page("search"))
        last_button.grid(row=3, column=1, padx=(0, 0), pady=5, sticky="e")

    def toggle_date_entry(self):
        if self.criteria.get() == "Birth Date":
            self.date_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.search_entry.grid_forget()
        else:
            self.search_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.date_entry.grid_forget()

    def toggle_additional_date_entry(self):
        if self.additional_criteria.get() == "Birth Date":
            self.additional_date_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.additional_search_entry.grid_forget()
        else:
            self.additional_search_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.additional_date_entry.grid_forget()

    def toggle_additional_criteria(self):
        if self.additional_search_criteria_frame.winfo_ismapped():
            self.add_criteria_button.config(text="+")
            self.additional_search_criteria_frame.grid_forget()
            self.additional_search_entry.delete(0, tk.END)
            self.additional_criteria.set("Select Criteria")
        else:
            if self.criteria.get() != "Select Criteria":
                current_main_criteria = self.criteria.get()
                self.additional_criteria_dropdown['values'] = [criteria for criteria in
                                                               ["Full Name", "Birth Date", "Position", "Squad",
                                                                "Football Team", "Home City"] if
                                                               criteria != current_main_criteria]
                self.add_criteria_button.config(text="-")
                self.additional_search_criteria_frame.grid(row=1, column=0, columnspan=3, padx=10,
                                                           pady=5, sticky="w")
                self.additional_search_entry.delete(0, tk.END)
                self.additional_criteria.set("Select Criteria")
            else:
                messagebox.askokcancel("Error", "Pick main criteria")

    def update_search_results(self, players):
        for item in self.search_result_tree.get_children():
            self.search_result_tree.delete(item)

        if players:
            for player in players:
                self.search_result_tree.insert("", tk.END, values=player.get_player_data())
        else:
            self.search_result_tree.insert("", tk.END, values=["No players found."])

        current_page_num = self.controller.get_page_num("search")
        self.search_window.title(f"Player List - Page {current_page_num}")

    def show_delete_window(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Players")
        delete_window.resizable(width=False, height=False)

        self.delete_frame = tk.Frame(delete_window)
        self.delete_frame.grab_set()
        self.delete_frame.pack(padx=10, pady=10)

        criteria_frame = tk.Frame(self.delete_frame)
        criteria_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.criteria = tk.StringVar()
        criteria_dropdown = ttk.Combobox(criteria_frame, textvariable=self.criteria,
                                         values=["Full Name", "Birth Date", "Position", "Squad", "Football Team",
                                                 "Home City"])
        criteria_dropdown.set("Select Criteria")
        criteria_dropdown.grid(row=0, column=1, padx=10, pady=5)

        criteria_dropdown.bind("<<ComboboxSelected>>", lambda event: self.toggle_date_entry())

        self.search_entry = ttk.Entry(criteria_frame, width=50)
        self.date_entry = DateEntry(criteria_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)

        self.toggle_date_entry()

        self.add_criteria_button = ttk.Button(criteria_frame, text="+", command=self.toggle_additional_criteria)
        self.add_criteria_button.grid(row=0, column=2, padx=10, pady=5)

        self.additional_search_criteria_frame = tk.Frame(self.delete_frame)

        self.additional_search_entry = ttk.Entry(self.additional_search_criteria_frame, width=50)
        self.additional_search_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.additional_criteria = tk.StringVar()
        self.additional_criteria_dropdown = ttk.Combobox(self.additional_search_criteria_frame,
                                                         textvariable=self.additional_criteria,
                                                         values=["Full Name", "Birth Date", "Position", "Squad",
                                                                 "Football Team",
                                                                 "Home City"])
        self.additional_criteria_dropdown.grid(row=0, column=1, padx=10, pady=5,
                                               sticky="w")

        self.additional_search_criteria_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        self.additional_search_criteria_frame.grid_forget()

        self.additional_criteria_dropdown.bind("<<ComboboxSelected>>",
                                               lambda event: self.toggle_additional_date_entry())

        self.additional_date_entry = DateEntry(self.additional_search_criteria_frame, width=12, background='darkblue',
                                               foreground='white', borderwidth=2)

        self.toggle_additional_date_entry()

        self.search_button = ttk.Button(criteria_frame, text="Search",
                                        command=lambda: self.controller.search_players("delete"))
        self.search_button.grid(row=0, column=3, padx=10, pady=5, sticky="e")

        self.result_tree = ttk.Treeview(self.delete_frame, columns=(
            "Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"), show="headings")
        self.result_tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        headers = ["Full Name", "Birth Date", "Football Team", "Home City", "Squad", "Position"]
        for header in headers:
            self.result_tree.heading(header, text=header)

        delete_button = ttk.Button(self.delete_frame, text="Delete", command=self.controller.delete_players)
        delete_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        first_button = ttk.Button(self.delete_frame, text="First", command=lambda: self.controller.first_page("delete"))
        first_button.grid(row=4, column=0, padx=(150, 200), pady=5, sticky="w")

        prev_button = ttk.Button(self.delete_frame, text="Previous",
                                 command=lambda: self.controller.prev_page("delete"))
        prev_button.grid(row=4, column=0, padx=(0, 10), pady=5)

        next_button = ttk.Button(self.delete_frame, text="Next", command=lambda: self.controller.next_page("delete"))
        next_button.grid(row=4, column=1, padx=(0, 10), pady=5)

        last_button = ttk.Button(self.delete_frame, text="Last", command=lambda: self.controller.last_page("delete"))
        last_button.grid(row=4, column=1, padx=(0, 0), pady=5, sticky="e")

    def update_delete_results(self, players):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        if players:
            for player in players:
                self.result_tree.insert("", tk.END, values=player.get_player_data())
        else:
            self.result_tree.insert("", tk.END, values=["No players found."])

    def show_add_player_window(self):
        add_player_window = tk.Toplevel(self.root)
        add_player_window.title("Add Player")
        add_player_window.resizable(width=False, height=False)

        add_frame = tk.Frame(add_player_window)
        add_frame.pack(padx=10, pady=10)
        add_frame.grab_set()

        full_name_label = tk.Label(add_frame, text="Full Name:")
        full_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.full_name_entry = ttk.Entry(add_frame, width=30)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=5)

        birth_date_label = tk.Label(add_frame, text="Birth Date:")
        birth_date_label.grid(row=1, column=0, padx=10, pady=5)
        self.birth_date_entry = DateEntry(add_frame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2)
        self.birth_date_entry.grid(row=1, column=1, padx=10, pady=5)

        football_team_label = tk.Label(add_frame, text="Football Team:")
        football_team_label.grid(row=2, column=0, padx=10, pady=5)
        self.football_team_entry = ttk.Entry(add_frame, width=30)
        self.football_team_entry.grid(row=2, column=1, padx=10, pady=5)

        home_city_label = tk.Label(add_frame, text="Home City:")
        home_city_label.grid(row=3, column=0, padx=10, pady=5)
        self.home_city_entry = ttk.Entry(add_frame, width=30)
        self.home_city_entry.grid(row=3, column=1, padx=10, pady=5)

        squad_label = tk.Label(add_frame, text="Squad:")
        squad_label.grid(row=4, column=0, padx=10, pady=5)
        self.squad_entry = ttk.Entry(add_frame, width=30)
        self.squad_entry.grid(row=4, column=1, padx=10, pady=5)

        position_label = tk.Label(add_frame, text="Position:")
        position_label.grid(row=5, column=0, padx=10, pady=5)
        self.position_entry = ttk.Entry(add_frame, width=30)
        self.position_entry.grid(row=5, column=1, padx=10, pady=5)

        add_button = ttk.Button(add_frame, text="Add Player", command=self.controller.add_player)
        add_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)  # corrected grid placement

    def show_players_tree(self):
        players = self.controller.get_all_players()
        # Create a new window to display the tree
        tree_window = tk.Toplevel(self.root)
        tree_window.title("Players Tree")

        # Create a root node for the tree
        root_node = Node("Players")

        # Assuming each player is represented by a tuple
        for player in players:
            player_node = Node(name=player.get_player_data()[0], parent=root_node)
            # Assuming the remaining elements of the tuple are player attributes
            for index, value in enumerate(player.get_player_data()[1:], start=1):
                Node(value, parent=player_node)

        # Render the tree
        tree_str = ""
        for pre, fill, node in RenderTree(root_node):
            tree_str += "%s%s\n" % (pre, node.name)

        # Display the tree in a text widget
        tree_frame = tk.Frame(tree_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree_text = tk.Text(tree_frame)
        tree_text.insert(tk.END, tree_str)
        tree_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbars if the tree is large
        scrollbar = ttk.Scrollbar(tree_frame, command=tree_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree_text.config(yscrollcommand=scrollbar.set)

    def update_main_window(self, players):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)

        if players:
            for player in players:
                self.player_tree.insert("", tk.END, values=player.get_player_data())
        else:
            self.player_tree.insert("", tk.END, values=["No players found."])

        current_page_num = self.controller.get_page_num("main")
        players_per_page = self.controller.get_players_limit()
        players_count = self.controller.players_list.get_players_count()
        self.root.title(
            f"Player List - Page: {current_page_num}\tPlayers {players_count}\tPer page: {players_per_page}")
