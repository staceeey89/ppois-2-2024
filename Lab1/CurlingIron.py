from instrument import Instrument


class CurlingIron(Instrument):
    def use(self, type):
        if type == "тонкие":
            return "\nДля тонких волос используется плойка с температурой 80 градусов"
        elif type == "плотные":
            return "\nДля плотных волос используется плойка с температурой 150 градусов"
