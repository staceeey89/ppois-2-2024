from client import Client
from HairClipper import HairClipper
from CurlingIron import CurlingIron
from instrument import Instrument


class Barber:
    def __init__(self, name):
        self._available = True
        self._active_instrument = None
        self._instruments = []
        self._name = name

    def make_haircut(self, client):
        response = "\n"
        for ins in self._instruments:
            if isinstance(ins, HairClipper):
                self._active_instrument = ins
                break
        power = ""
        if isinstance(client, Client):
            if client.hair_length < 10:
                response += "Выполняется стрижка коротких волос"
                power = "low"
            else:
                response += "Выполняется стрижка длинных волос"
                power = "high"
        response += self._active_instrument.use(power)
        return response

    def make_hair_styling(self, client):
        response = "\n"
        if isinstance(client, Client):
            if client.hair_length < 10:
                response += "Выполняется укладка коротких волос"
            else:
                response += "Выполняется укладка длинных волос"
            for ins in self._instruments:
                if isinstance(ins, CurlingIron):
                    self._active_instrument = ins
                    break
            if self._active_instrument is not None:
                response += self._active_instrument.use(client.hair_type)
        return response

    def make_consultation(self, client):
        response = "\n"
        if isinstance(client, Client):
            if client.hair_length < 10:
                if client.hair_type == "тонкие":
                    response += "Выполнена консультация по уходу за короткими тонкими волосами"
                else:
                    response += "Выполнена консультация по уходу за короткими плотными волосами"
            else:
                if client.hair_type == "тонкие":
                    response += "Выполнена консультация по уходу за длинными тонкими волосами"
                else:
                    response += "Выполнена консультация по уходу за длинными плотными волосами"
        return response

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def instruments(self):
        return self._instruments

    def add_instrument(self, value):
        if isinstance(value, Instrument):
            self._instruments.append(value)

    @property
    def name(self):
        return self._name
