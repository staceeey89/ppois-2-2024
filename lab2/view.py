import wx
from typing import List, Optional
from model import Record
from pubsub import pub
from frames import MainFrame, FindFrame, RemoveFrame
from dialogs import FindRemoveDialog, InputDialog, InfoDialog


class View:
    def __init__(self):
        self.app = wx.App()
        self.mainFrame = MainFrame(None, "Database view")
        self.mainFrame.Show()

    def main_loop(self):
        self.app.MainLoop()

    def get_mainFrame(self):
        return self.mainFrame

    def update_table(self, evt_object, new_data: List[Record]):
        evt_object.clear_table()
        evt_object.setup_table(new_data)

    def set_page_text(self, evt_object, current_page, total_pages):
        if total_pages == 0:
            evt_object.set_page_text(0, 0)
            return
        evt_object.set_page_text(current_page + 1, total_pages)

    def set_amount_text(self, evt_object, amount):
        evt_object.set_amount_text(amount)

    def set_on_page_text(self, evt_object, on_page: int):
        evt_object.set_on_page_text(on_page)

    def set_per_page(self, evt_object, amount):
        evt_object.set_per_page_text(amount)

    def error_message(self, message):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)

    def change_input_ctrl_text(self, evt_object, new_input):
        evt_object.on_page_ctrl.SetLabel(str(new_input))

    def reset_input_ctrl(self, evt_object):
        label = evt_object.on_page_ctrl.GetLabelText()
        self.mainFrame.on_page_ctrl.SetLabel(label)

    def call_add_entry_dialog(self):
        self.mainFrame.call_add_entry_dialog()

    def call_find_dialog(self):
        self.mainFrame.call_find_dialog()

    def call_remove_dialog(self):
        self.mainFrame.call_remove_dialog()

    def open_find_window(self):
        return FindFrame(self.mainFrame, "Found entries")

    def open_remove_window(self):
        return RemoveFrame(self.mainFrame, "Found entries to remove")

    def open_file_open_dialog_SQL(self, is_saved: bool) -> Optional[str]:
        if is_saved is False:
            if (
                wx.MessageBox(
                    "Current content has not been saved! Proceed?",
                    "Please confirm",
                    wx.ICON_QUESTION | wx.YES_NO,
                    self.mainFrame,
                )
                == wx.NO
            ):
                self.mainFrame.Enable()
                return None

        with wx.FileDialog(
            self.mainFrame,
            "Open Database file",
            wildcard="Database files (*.db)|*.db",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.mainFrame.Enable()
                return None

            pathname = fileDialog.GetPath()
            try:
                self.mainFrame.Enable()
                return pathname
            except IOError:
                self.mainFrame.Enable()
                wx.LogError("Cannot open file")

    def open_file_open_dialog_XML(self, is_saved: bool) -> Optional[str]:
        if is_saved is False:
            if (
                wx.MessageBox(
                    "Current content has not been saved! Proceed?",
                    "Please confirm",
                    wx.ICON_QUESTION | wx.YES_NO,
                    self.mainFrame,
                )
                == wx.NO
            ):
                self.mainFrame.Enable()
                return None

        with wx.FileDialog(
            self.mainFrame,
            "Open XML file",
            wildcard="XML files(*.xml)|*.xml",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.mainFrame.Enable()
                return None

            pathname = fileDialog.GetPath()
            try:
                self.mainFrame.Enable()
                return pathname
            except IOError:
                self.mainFrame.Enable()
                wx.LogError("Cannot open file")

    def open_removed_info(self, removed_entries):
        if removed_entries == 0:
            InfoDialog(None, "Remove result", "Nothing has been removed!")
        else:
            InfoDialog(None, "Remove result", f"Entries removed: {removed_entries}")

    def info_message(self, title: str, message: str) -> None:
        InfoDialog(None, title, message)

    def set_saved_status(self, evt_object, is_saved: bool):
        if evt_object == self.mainFrame and not is_saved:
            self.mainFrame.SetLabel("Database view *")
        elif is_saved:
            self.mainFrame.SetLabel("Database view")
