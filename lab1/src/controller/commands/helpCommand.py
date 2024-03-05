from src.controller.commands.command import Command
from src.controller.input import Input
from src.DAO.repository import Repository


class HelpCommand(Command):
    name = "help"

    def execute(self):
        return ("list\n"
                "list [name_of_state] [government|economy|external_politics|legislation|population]\n"
                "add state [name_of_state] [name_of_head_of_government]\n"
                "add citizen [name_of_citizen] [income_of_citizen] [name_of_state]\n"
                "remove state [name_of_state]\n"
                "remove citizen [name_of_citizen] [name_of_state]\n"
                "publish_law [title] [text]\n"
                "provide_security [name_of_state] [name_of_citizen]\n"
                "provide_social_support [name_of_state] [name_of_citizen]\n"
                "collect_taxes [name_of_state]\n"
                "enhance_infrastructure [name_of_state]")

    def can_execute(self, *args: str) -> bool:
        return len(self.args) == 0