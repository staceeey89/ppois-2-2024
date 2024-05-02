from dataclasses import dataclass


@dataclass
class ConfigPaths:
    """Class to store default configuration file paths."""
    enemies: str
    weapons: str
    waves: str
    animations: str