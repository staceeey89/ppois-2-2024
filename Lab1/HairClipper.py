from instrument import Instrument


class HairClipper(Instrument):
    def use(self, power):
        if power == "low":
            return "\nИспользуется машинка со слабой мощностью"
        elif power == "high":
            return "\nИспользуется машинка с сильной мощностью"
