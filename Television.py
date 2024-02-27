from Screen import *
from Sound_system import *
from Technical_characteristics import *
class Television:
    connected: bool = False
    device: str = 'No devices connected!'
    operation_system: str = ''
    software_version: str = ''
    tv_channel: str = ''

    def device_connected(self, device: str, connected: bool) -> bool:
        self.connected = connected
        if self.connected is False and device != '' or self.connected is True:
            self.device = device
            return True
        else:
            self.device = 'No devices connected!'
            return False

    def __init__(self, model: str, price: str, color: str):
        self.model = model
        self.price = price
        self.color = color
        self.is_on = False
        self.screen = Screen()
        self.sound = Sound_system()

    def set_software(self, operation_system: str, software_version: str):
        self.operation_system = operation_system
        self.software_version = software_version

    def update_software(self, operation_system: str, software_version: str) -> bool:
        if self.operation_system == operation_system:
            if float(self.software_version) < float(software_version):
                self.software_version = software_version
                print('You software updated succesfully!')
                return True
            else:
                print('You software already updated to latest version!')
        else:
            print('Incorrect software!')
            return False

    def turn_on(self) -> bool:
        self.is_on: bool = True
        print('TV is turned on!')
        return self.is_on

    def turn_off(self) -> bool:
        self.is_on: bool = False
        print('TV is turned off!')
        return self.is_on

    def check_channel(self) -> bool:
        if self.tv_channel == '':
            print('You are not watching a channel!')
            return False
        else:
            print('You are watching a', self.tv_channel, 'channel!')
            return True

    def choose_channel(self, tv_channel: str):
        self.check_channel()
        if self.is_on == True:
            if tv_channel == 'Childrens' or tv_channel == 'Entertainment' or tv_channel == 'Sport' or tv_channel == 'Culinary' or tv_channel == 'Music':
                self.tv_channel = tv_channel
                print('Now you are watching a', self.tv_channel, 'channel!')
            else:
                print('Incorrect channel entered!')
        else:
            print('TV is off! You cant choose the channel!')

    def add_britness(self, level: int):
        self.screen.add_britness(level)
        return level

    def add_contrast(self, level: int):
        self.screen.add_contrast(level)
        return level

    def add_saturation(self, level: int):
        self.screen.add_saturation(level)
        return level

    def change_sound_level(self, level: int) -> bool:
        if self.is_on == True:
            self.sound.change_sound_level(level)
            return True
        else:
            print('TV is off! Cant change sound level')
            return False

    def print_data(self):
        print('Television info')
        print('_' * 66)
        print('|Model:', self.model, '|Color:', self.color, '|Price:', self.price, '|Device connected:', self.device)
        print('_' * 66)
        print('|Type of software:', self.operation_system, '|Version:', self.software_version)
        print('_' * 66)
        print('|Screen Brightness:', self.screen.britness, '|Contrast:', self.screen.contrast, '|Saturation:',
              self.screen.saturation)
        print('_' * 66)
        print('|Sound level:', self.sound.sound_level)
        print('_' * 66)