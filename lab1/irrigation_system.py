

class IrrigationSystem:
    def __init__(self):
        self.turned_on = False
        self.dunged = False

    def turn_on(self):
        self.turned_on = True
        print("включена система полива")

    def turn_off(self):
        self.turned_on = False
        print("система полива выключена")

    def get_status(self):
        return self.turned_on

    def start_fertilize(self):
        if self.dunged:
            print("система полива уже заправлена")
        else:
            self.dunged = True
            print("ваша система полива заправлена удобрением")

    def stop_fertilize(self):
        if not self.dunged:
            print("система полива уже без удобрения")
        else:
            self.dunged = False
            print("ваша система полива больше не заправлена удобрением")