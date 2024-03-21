import wx
from pubsub import pub
from dialogs import FindRemoveDialog, InputDialog
from typing import List
from model import Record
from dataclasses import astuple


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(
            parent,
            title=title,
            size=(900, 500),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
        )

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("gray")

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(7)
        self.add_control_box(vbox)

        self.add_menubar()
        vbox.AddStretchSpacer(1)
        self.add_table(vbox)
        self.add_navigation_box(vbox)
        vbox.AddStretchSpacer(2)
        self.panel.SetSizer(vbox)
        self.panel.Fit()
        self.Centre()

    def add_control_box(self, vbox: wx.BoxSizer):
        control_box = wx.BoxSizer(wx.HORIZONTAL)
        add_button = wx.Button(self.panel, label="Add entry", size=(80, 40))
        add_button.Bind(wx.EVT_BUTTON, self.on_add_entry)
        find_button = wx.Button(self.panel, label="Find entries", size=(90, 40))
        find_button.Bind(wx.EVT_BUTTON, self.on_find)
        remove_button = wx.Button(self.panel, label="Remove entries", size=(90, 40))
        remove_button.Bind(wx.EVT_BUTTON, self.on_remove)
        control_box.AddSpacer(25)
        control_box.Add(add_button, border=5)
        control_box.Add(find_button, border=5)
        control_box.Add(remove_button, border=5)
        control_box.AddSpacer(17)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.amount_text = wx.StaticText(
            self.panel, id=1, label="No data", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        self.on_page_amount_text = wx.StaticText(
            self.panel, id=1, label="No info", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        vertical_box.AddSpacer(3)
        vertical_box.Add(self.amount_text)
        vertical_box.Add(self.on_page_amount_text)
        control_box.Add(vertical_box)

        on_page_box = wx.BoxSizer(wx.VERTICAL)
        on_page_control_text = wx.StaticText(
            self.panel, id=1, label="Per page:", style=wx.ALIGN_LEFT, size=(120, 17)
        )
        on_page_minus = wx.Button(self.panel, label="-", size=((22, 22)))
        on_page_minus.Bind(wx.EVT_BUTTON, self.on_minus)
        self.on_page_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.on_page_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_page_enter)
        on_page_plus = wx.Button(self.panel, label="+", size=((22, 22)))
        on_page_plus.Bind(wx.EVT_BUTTON, self.on_plus)

        on_page_box.Add(on_page_control_text)

        on_page_hor_box = wx.BoxSizer(wx.HORIZONTAL)
        on_page_hor_box.Add(on_page_minus)
        on_page_hor_box.Add(self.on_page_ctrl)
        on_page_hor_box.Add(on_page_plus)

        on_page_box.Add(on_page_hor_box)
        control_box.Add(on_page_box)

        vbox.Add(control_box, flag=wx.LEFT, border=30)

    def add_navigation_box(self, vbox: wx.BoxSizer):
        navigation_box = wx.BoxSizer(wx.HORIZONTAL)
        first_button = wx.Button(self.panel, label="<<", size=(20, 17))
        first_button.Bind(wx.EVT_BUTTON, self.on_first)
        prev_button = wx.Button(self.panel, label="<", size=(20, 17))
        prev_button.Bind(wx.EVT_BUTTON, self.on_prev_nav)

        next_button = wx.Button(self.panel, label=">", size=(20, 17))
        next_button.Bind(wx.EVT_BUTTON, self.on_next_nav)
        last_button = wx.Button(self.panel, label=">>", size=(20, 17))
        last_button.Bind(wx.EVT_BUTTON, self.on_last)

        self.page_text = wx.StaticText(
            self.panel, id=1, label="0/0", style=wx.ALIGN_CENTER, size=(50, 20)
        )

        navigation_box.Add(first_button)
        navigation_box.Add(prev_button)
        navigation_box.Add(self.page_text)
        navigation_box.Add(next_button)
        navigation_box.Add(last_button)

        vbox.Add(navigation_box, flag=wx.LEFT | wx.CENTER, border=20)

    def on_add_entry(self, event):
        pub.sendMessage("press add entry")

    def on_minus(self, event):
        pub.sendMessage("press minus", evt_object=self)

    def on_plus(self, event):
        pub.sendMessage("press plus", evt_object=self)

    def on_page_enter(self, event):
        pub.sendMessage(
            "press page enter",
            evt_object=self,
            enter_input=self.on_page_ctrl.GetValue(),
        )

    def on_first(self, event):
        pub.sendMessage("press first", evt_object=self)

    def on_last(self, event):
        pub.sendMessage("press last", evt_object=self)

    def on_prev_nav(self, event):
        pub.sendMessage("press prev", evt_object=self)

    def on_next_nav(self, event):
        pub.sendMessage("press next", evt_object=self)

    def on_find(self, event):
        pub.sendMessage("open find dialog")

    def on_remove(self, event):
        pub.sendMessage("open remove dialog")

    def add_menubar(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        editMenu = wx.Menu()
        fileItemOpenSQL = fileMenu.Append(
            wx.ID_OPEN, "Open a db file", "Select a database to work with"
        )
        fileItemOpenXML = fileMenu.Append(
            wx.NewId(), "Open an XML file", "Select an xml file"
        )
        fileItemSave = fileMenu.Append(wx.NewId(), "Save file", "Save the changes")
        fileItemQuit = fileMenu.Append(wx.NewId(), "Quit", "Quit application")

        viewTree = viewMenu.Append(wx.NewId(), "Tree", "View in the tree form")
        viewFind = viewMenu.Append(wx.NewId(), "Find", "Find all entries")

        editAdd = editMenu.Append(wx.NewId(), "Add", "Add a new entry")
        editRemove = editMenu.Append(wx.NewId(), "Remove", "Find all entries to remove")

        menubar.Append(fileMenu, "&File")
        menubar.Append(viewMenu, "&View")
        menubar.Append(editMenu, "&Edit")

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItemQuit)
        self.Bind(wx.EVT_MENU, self.OnSave, fileItemSave)
        self.Bind(wx.EVT_MENU, self.OnOpenSQL, fileItemOpenSQL)
        self.Bind(wx.EVT_MENU, self.OnOpenXML, fileItemOpenXML)
        self.Bind(wx.EVT_MENU, self.OnTree, viewTree)
        self.Bind(wx.EVT_MENU, self.OnViewFind, viewFind)
        self.Bind(wx.EVT_MENU, self.OnEditRemove, editRemove)
        self.Bind(wx.EVT_MENU, self.OnEditAdd, editAdd)

    def OnTree(self, event):
        pub.sendMessage("open tree view", evt_object=self)

    def OnViewFind(self, event):
        pub.sendMessage("open find dialog")

    def OnEditRemove(self, event):
        pub.sendMessage("open remove dialog")

    def OnEditAdd(self, event):
        pub.sendMessage("press add entry")

    def OnSave(self, event):
        pub.sendMessage("save changes")

    def OnOpenXML(self, event):
        pub.sendMessage("open file open dialog XML")

    def OnOpenSQL(self, event):
        pub.sendMessage("open file open dialog SQL")

    def add_table(self, vbox: wx.BoxSizer):
        list_box = wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListCtrl(
            self.panel,
            style=wx.LC_REPORT | wx.LC_HRULES,
            size=wx.Size(832, 350),
        )
        column_names = (
            "Full name",
            "Father full name",
            "Father salary",
            "Mother full name",
            "Mother salary",
            "Brothers amount",
            "Sisters amount",
        )
        self.list.InsertColumn(0, column_names[0], width=135)
        for i in range(1, 7):
            self.list.InsertColumn(i, column_names[i], width=8 * len(column_names[i]))

        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.prevent_selection_event)

        list_box.Add(self.list)
        vbox.Add(
            list_box,
            proportion=1,
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.CENTER,
            border=5,
        )

    def prevent_selection_event(self, event):
        item_index = event.GetIndex()
        self.list.Select(item_index, on=False)

    def setup_table(self, table_data: List[Record]):
        for record in table_data:
            self.add_table_item(record)

    def add_table_item(self, record: Record):
        index = self.list.GetItemCount()
        record_tuple = astuple(record)
        self.list.InsertItem(index, record_tuple[0])
        for col, text in enumerate(record_tuple[1:], 1):
            if type(text) is int:
                text = str(text)
            self.list.SetItem(index, col, text)

    def set_page_text(self, current_page, total_pages):
        page_text_str = f"{current_page}/{total_pages}"
        self.page_text.SetLabel(page_text_str)

    def set_amount_text(self, amount: int):
        self.amount_text.SetLabel(f"Entries: {amount}")

    def set_on_page_text(self, on_page: int):
        self.on_page_amount_text.SetLabel(f"On page: {on_page}")

    def set_per_page_text(self, per_page: int):
        self.on_page_ctrl.SetLabel(str(per_page))

    def clear_table(self):
        self.list.DeleteAllItems()

    def on_page_ctrl_input(self) -> str:
        return self.on_page_ctrl.GetLabelText()

    def OnQuit(self, event):
        self.Close()

    def call_add_entry_dialog(self):
        self.Disable()
        dialog = InputDialog(self, title="Add entry")
        if dialog.ShowModal() == wx.ID_OK:
            out = dialog.value
            pub.sendMessage("add new entry dialog", new_data=out)
        dialog.Destroy()
        self.Enable()
        self.SetFocus()

    def call_find_dialog(self):
        self.SetFocus()
        self.Disable()
        dialog = FindRemoveDialog(self, title="Find entries")
        if dialog.ShowModal() == wx.ID_OK:
            if dialog.name_out is not None:
                pub.sendMessage("open find full name window", full_name=dialog.name_out)
            elif dialog.salary_out is not None:
                pub.sendMessage("open find salary window", salary=dialog.salary_out)
            elif dialog.brothers is not None:
                pub.sendMessage("open find brothers window", brothers=dialog.brothers)
            elif dialog.sisters is not None:
                pub.sendMessage("open find sisters window", sisters=dialog.sisters)
            dialog.Destroy()
            return
        dialog.Destroy()
        self.Enable()
        self.SetFocus()

    def call_remove_dialog(self):
        self.SetFocus()
        self.Disable()
        dialog = FindRemoveDialog(self, title="Remove entries")
        if dialog.ShowModal() == wx.ID_OK:
            if dialog.name_out is not None:
                pub.sendMessage(
                    "open remove full name window", full_name=dialog.name_out
                )
            elif dialog.salary_out is not None:
                pub.sendMessage("open remove salary window", salary=dialog.salary_out)
            elif dialog.brothers is not None:
                pub.sendMessage("open remove brothers window", brothers=dialog.brothers)
            elif dialog.sisters is not None:
                pub.sendMessage("open remove sisters window", sisters=dialog.sisters)
            dialog.Destroy()
            return
        dialog.Destroy()
        self.Enable()
        self.SetFocus()


class FindFrame(MainFrame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(
            parent,
            title=title,
            size=(900, 500),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
        )
        self.parent = parent
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("gray")

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(7)
        self.add_control_box(vbox)
        vbox.AddStretchSpacer(1)
        self.add_table(vbox)
        self.add_navigation_box(vbox)
        vbox.AddStretchSpacer(2)
        self.panel.SetSizer(vbox)
        self.panel.Fit()
        self.Centre()
        self.Show()

    def on_close(self, event):
        self.parent.Enable()
        self.parent.SetFocus()
        event.Skip()

    def add_control_box(self, vbox: wx.BoxSizer):
        control_box = wx.BoxSizer(wx.HORIZONTAL)
        control_box.AddSpacer(320)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.amount_text = wx.StaticText(
            self.panel, id=1, label="No data", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        self.on_page_amount_text = wx.StaticText(
            self.panel, id=1, label="No info", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        vertical_box.AddSpacer(3)
        vertical_box.Add(self.amount_text)
        vertical_box.Add(self.on_page_amount_text)
        control_box.Add(vertical_box)

        on_page_box = wx.BoxSizer(wx.VERTICAL)
        on_page_control_text = wx.StaticText(
            self.panel, id=1, label="Per page:", style=wx.ALIGN_LEFT, size=(120, 17)
        )
        on_page_minus = wx.Button(self.panel, label="-", size=((22, 22)))
        on_page_minus.Bind(wx.EVT_BUTTON, self.on_minus)
        self.on_page_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.on_page_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_page_enter)
        on_page_plus = wx.Button(self.panel, label="+", size=((22, 22)))
        on_page_plus.Bind(wx.EVT_BUTTON, self.on_plus)

        on_page_box.Add(on_page_control_text)

        on_page_hor_box = wx.BoxSizer(wx.HORIZONTAL)
        on_page_hor_box.Add(on_page_minus)
        on_page_hor_box.Add(self.on_page_ctrl)
        on_page_hor_box.Add(on_page_plus)

        on_page_box.Add(on_page_hor_box)
        control_box.Add(on_page_box)

        vbox.Add(control_box, flag=wx.LEFT, border=30)


class RemoveFrame(MainFrame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(
            parent,
            title=title,
            size=(900, 500),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
        )
        self.parent = parent
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("gray")

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(7)
        self.add_control_box(vbox)
        vbox.AddStretchSpacer(1)
        self.add_table(vbox)
        self.add_navigation_box(vbox)
        vbox.AddStretchSpacer(2)
        self.panel.SetSizer(vbox)
        self.panel.Fit()
        self.Centre()
        self.Show()

    def on_close(self, event):
        self.parent.Enable()
        self.parent.SetFocus()
        event.Skip()

    def add_control_box(self, vbox: wx.BoxSizer):
        control_box = wx.BoxSizer(wx.HORIZONTAL)
        add_button = wx.Button(self.panel, label="Remove entries", size=(120, 40))
        add_button.Bind(wx.EVT_BUTTON, self.on_remove_entries)
        control_box.AddSpacer(25)
        control_box.Add(add_button, border=5)
        control_box.AddSpacer(295)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.amount_text = wx.StaticText(
            self.panel, id=1, label="No data", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        self.on_page_amount_text = wx.StaticText(
            self.panel, id=1, label="No info", style=wx.ALIGN_LEFT, size=(170, 17)
        )
        vertical_box.AddSpacer(3)
        vertical_box.Add(self.amount_text)
        vertical_box.Add(self.on_page_amount_text)
        control_box.Add(vertical_box)

        on_page_box = wx.BoxSizer(wx.VERTICAL)
        on_page_control_text = wx.StaticText(
            self.panel, id=1, label="Per page:", style=wx.ALIGN_LEFT, size=(120, 17)
        )
        on_page_minus = wx.Button(self.panel, label="-", size=((22, 22)))
        on_page_minus.Bind(wx.EVT_BUTTON, self.on_minus)
        self.on_page_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.on_page_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_page_enter)
        on_page_plus = wx.Button(self.panel, label="+", size=((22, 22)))
        on_page_plus.Bind(wx.EVT_BUTTON, self.on_plus)

        on_page_box.Add(on_page_control_text)

        on_page_hor_box = wx.BoxSizer(wx.HORIZONTAL)
        on_page_hor_box.Add(on_page_minus)
        on_page_hor_box.Add(self.on_page_ctrl)
        on_page_hor_box.Add(on_page_plus)

        on_page_box.Add(on_page_hor_box)
        control_box.Add(on_page_box)

        vbox.Add(control_box, flag=wx.LEFT, border=30)

    def on_remove_entries(self, event):
        pub.sendMessage("remove entries")
        self.Close()
        self.parent.Enable()
        self.parent.SetFocus()
