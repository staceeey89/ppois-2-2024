import wx


class FindRemoveDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(FindRemoveDialog, self).__init__(parent, title=title, size=(300, 600))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.input_ctrls = []
        self.choice_ctrls = []
        self.radio_list = []
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        radio1 = wx.RadioButton(self.panel, label="Full name: ", style=wx.RB_GROUP)
        hbox1.Add(radio1, 0, wx.ALL, 5)
        self.radio_list.append(radio1)
        self.add_choice_field(hbox1)
        vbox.Add(hbox1)
        self.add_name_field(vbox)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        radio2 = wx.RadioButton(self.panel, label="Father full name: ")
        hbox2.Add(radio2, 0, wx.ALL, 5)
        self.radio_list.append(radio2)
        self.add_choice_field(hbox2)
        vbox.Add(hbox2)
        self.add_name_field(vbox)

        radio3 = wx.RadioButton(self.panel, label="Father salary: ")
        vbox.Add(radio3, 0, wx.ALL, 5)
        self.radio_list.append(radio3)
        self.add_salary_field(vbox, "Maximum: ")
        self.add_salary_field(vbox, "Minimum: ")

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        radio4 = wx.RadioButton(self.panel, label="Mother full name: ")
        hbox3.Add(radio4, 0, wx.ALL, 5)
        self.radio_list.append(radio4)
        self.add_choice_field(hbox3)
        vbox.Add(hbox3)
        self.add_name_field(vbox)

        radio5 = wx.RadioButton(self.panel, label="Mother salary: ")
        vbox.Add(radio5, 0, wx.ALL, 5)
        self.radio_list.append(radio5)
        self.add_salary_field(vbox, "Maximum: ")
        self.add_salary_field(vbox, "Minimum: ")

        radio6 = wx.RadioButton(self.panel, label="Brothers: ")
        vbox.Add(radio6, 0, wx.ALL, 5)
        self.radio_list.append(radio6)
        self.add_siblings_field(vbox)

        radio7 = wx.RadioButton(self.panel, label="Sisters: ")
        vbox.Add(radio7, 0, wx.ALL, 5)
        self.radio_list.append(radio7)
        self.add_siblings_field(vbox)

        self.set_ok_cancel_buttons(vbox)

        self.panel.SetSizer(vbox)

    def add_choice_field(self, vbox):
        choice = wx.Choice(
            self.panel, choices=["First name", "Middle name", "Last name"]
        )
        choice.SetSelection(0)
        self.choice_ctrls.append(choice)
        vbox.Add(choice, 0, wx.ALL, 5)

    def add_name_field(self, vbox):
        text_ctrl = wx.TextCtrl(self.panel, size=(130, 20))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(text_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)
        text_ctrl.GetLabelText

        self.input_ctrls.append(text_ctrl)

    def add_salary_field(self, vbox, string):
        label = wx.StaticText(self.panel, label=string, size=(70, 20))
        text_ctrl = wx.TextCtrl(self.panel, size=(100, 20))
        text_ctrl.Bind(wx.EVT_CHAR, self.accept_only_numerical)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.ALL, border=5)
        hbox.Add(text_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)

        self.input_ctrls.append(text_ctrl)

    def add_siblings_field(self, vbox):
        spin_ctrl = wx.SpinCtrlDouble(
            self.panel,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS,
            0,
            50,
            0,
        )

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(spin_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)

        self.input_ctrls.append(spin_ctrl)

    def accept_only_numerical(self, event):
        text_ctrl = event.GetEventObject()
        text_length = len(text_ctrl.GetValue())

        keycode = event.GetKeyCode()
        if keycode < wx.WXK_SPACE or keycode == wx.WXK_DELETE or keycode > 255:
            event.Skip()
            return

        if text_length == 0 and chr(keycode) == "0":
            return

        if chr(keycode).isdigit():
            event.Skip()
            return

    def set_ok_cancel_buttons(self, vbox):
        button_ok = wx.Button(self.panel, label="OK")
        button_cancel = wx.Button(self.panel, label="Cancel")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(button_ok, flag=wx.LEFT | wx.RIGHT, border=5)
        hbox.Add(button_cancel, flag=wx.LEFT | wx.RIGHT, border=5)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

        button_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        button_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, event):
        self.name_out = None
        self.salary_out = None
        self.brothers = None
        self.sisters = None
        index = 0
        for ind, radio in enumerate(self.radio_list, 1):
            if radio.GetValue() is True:
                index = ind
                break

        if index == 1 or index == 2 or index == 4:
            if index == 4:
                text: str = self.input_ctrls[4].GetValue()
            else:
                text: str = self.input_ctrls[index - 1].GetValue()

            if len(text.split()) != 1:
                wx.MessageBox(
                    "The name field is incorrect!", "Error", wx.OK | wx.ICON_ERROR
                )
                return

            text = text.replace(" ", "")

            if index == 4:
                self.name_out = [self.choice_ctrls[2].GetCurrentSelection(), 2, text]
            else:
                self.name_out = [
                    self.choice_ctrls[index - 1].GetCurrentSelection(),
                    index - 1,
                    text,
                ]
            self.EndModal(wx.ID_OK)

        if index == 3 or index == 5:
            if index == 3:
                text_max = self.input_ctrls[index - 1].GetValue()
                text_min = self.input_ctrls[index].GetValue()
            else:
                text_max = self.input_ctrls[index].GetValue()
                text_min = self.input_ctrls[index + 1].GetValue()

            if text_max == "" and text_min == "":
                wx.MessageBox(
                    "The salary field is empty!", "Error", wx.OK | wx.ICON_ERROR
                )
                return

            if text_max != "" and text_min != "":
                if int(text_max) < int(text_min):
                    wx.MessageBox(
                        "The min value is bigger than max!",
                        "Error",
                        wx.OK | wx.ICON_ERROR,
                    )
                    return

            if index == 3:
                self.salary_out = [0, (text_max, text_min)]
            else:
                self.salary_out = [1, (text_max, text_min)]

            self.EndModal(wx.ID_OK)

        if index == 6:
            self.brothers = int(self.input_ctrls[index + 1].GetValue())
            self.EndModal(wx.ID_OK)

        if index == 7:
            self.sisters = int(self.input_ctrls[index + 1].GetValue())
            self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)


class InputDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(InputDialog, self).__init__(parent, title=title, size=(500, 327))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.full_names_list = []
        self.salary_list = []
        self.siblings_list = []
        self.add_name_field(vbox, "Full name: ")
        self.add_name_field(vbox, "Father full name: ")
        self.add_salary_field(vbox, "Father salary: ")
        self.add_name_field(vbox, "Mother full name: ")
        self.add_salary_field(vbox, "Mother salary: ")
        self.add_siblings_field(vbox, "Brothers amount: ")
        self.add_siblings_field(vbox, "Sisters amount: ")

        self.set_ok_cancel_buttons(vbox)

        self.panel.SetSizer(vbox)

    def add_name_field(self, vbox, string):
        label = wx.StaticText(self.panel, label=string, size=(100, 20))
        text_ctrl = wx.TextCtrl(self.panel, size=(230, 20))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.ALL, border=5)
        hbox.Add(text_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)
        text_ctrl.GetLabelText

        self.full_names_list.append(text_ctrl)

    def add_salary_field(self, vbox, string):
        label = wx.StaticText(self.panel, label=string, size=(100, 20))
        text_ctrl = wx.TextCtrl(self.panel, size=(100, 20))
        text_ctrl.Bind(wx.EVT_CHAR, self.accept_only_numerical)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.ALL, border=5)
        hbox.Add(text_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)

        self.salary_list.append(text_ctrl)

    def add_siblings_field(self, vbox, string):
        label = wx.StaticText(self.panel, label=string, size=(100, 20))
        spin_ctrl = wx.SpinCtrlDouble(
            self.panel,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS,
            0,
            50,
            0,
        )

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(label, flag=wx.ALL, border=5)
        hbox.Add(spin_ctrl, proportion=1, flag=wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.LEFT | wx.TOP, border=5)

        self.siblings_list.append(spin_ctrl)

    def accept_only_numerical(self, event):
        text_ctrl = event.GetEventObject()
        text_length = len(text_ctrl.GetValue())

        keycode = event.GetKeyCode()
        if keycode < wx.WXK_SPACE or keycode == wx.WXK_DELETE or keycode > 255:
            event.Skip()
            return

        if text_length == 0 and chr(keycode) == "0":
            return

        if chr(keycode).isdigit():
            event.Skip()
            return

    def set_ok_cancel_buttons(self, vbox):
        button_ok = wx.Button(self.panel, label="OK")
        button_cancel = wx.Button(self.panel, label="Cancel")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(button_ok, flag=wx.LEFT | wx.RIGHT, border=5)
        hbox.Add(button_cancel, flag=wx.LEFT | wx.RIGHT, border=5)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

        button_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        button_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, event):
        self.value = []
        for ind, full_name in enumerate(self.full_names_list, 1):
            text = full_name.GetValue()
            if len(text.split()) != 3:
                if text != "":
                    error_message = f"The full name field {ind} is incorrect {full_name.GetValue()}!"
                else:
                    error_message = f"The full name field {ind} is incorrect!"
                wx.MessageBox(error_message, "Error", wx.OK | wx.ICON_ERROR)
                return

        for ind, salary_field in enumerate(self.salary_list, 1):
            text = salary_field.GetValue()
            if text == "":
                wx.MessageBox(
                    f"The salary field {ind} is empty!", "Error", wx.OK | wx.ICON_ERROR
                )
                return
        words = self.full_names_list[0].GetValue().split()
        text = " ".join(words)
        self.value.append(text)
        words = self.full_names_list[1].GetValue().split()
        text = " ".join(words)
        self.value.append(text)
        self.value.append(int(self.salary_list[0].GetValue()))
        words = self.full_names_list[2].GetValue().split()
        text = " ".join(words)
        self.value.append(text)
        self.value.append(int(self.salary_list[1].GetValue()))
        self.value.append(int(self.siblings_list[0].GetValue()))
        self.value.append(int(self.siblings_list[1].GetValue()))

        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)


class InfoDialog(wx.Dialog):
    def __init__(self, parent, title, message, size=(400, 300)):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        text = wx.TextCtrl(panel, value=message, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        btn_ok = wx.Button(panel, label="OK")
        btn_ok.Bind(wx.EVT_BUTTON, self.OnOK)
        vbox.Add(btn_ok, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        self.Centre()
        self.ShowModal()

    def OnOK(self, event):
        self.Destroy()
