from dataclasses import dataclass


@dataclass
class Input:
    command_name: str
    args: list
