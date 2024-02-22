import screen_brightness_control as sbc


class BrightnessController:
    @staticmethod
    def get_brightness() -> int:
        return sbc.get_brightness(display=0).pop()

    @staticmethod
    def set_brightness(brightness_level: int):
        sbc.set_brightness(brightness_level)

    @staticmethod
    def increase_brightness():
        BrightnessController.set_brightness(BrightnessController.get_brightness() + 5)

    @staticmethod
    def decrease_brightness():
        BrightnessController.set_brightness(BrightnessController.get_brightness() - 5)
