from src.model.citizen import Citizen


class Government:
    def __init__(self, head: Citizen):
        self._head: Citizen = head

    @property
    def head(self) -> Citizen:
        return self._head

    def change_head(self, head: Citizen):
        self._head = head

    def provide_security(self, citizen: Citizen):
        return f"Security of {citizen.name} is provided thanks to {self.head.name}!"

    def provided_social_support(self, citizen: Citizen):
        return f"Social support of {citizen.name} is provided thanks to {self.head.name}!"
