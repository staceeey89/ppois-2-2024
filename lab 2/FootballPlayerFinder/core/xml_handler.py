import xml.sax
import xml.dom.minidom
from xml.dom.minidom import Document
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl
from core.db_interface import DBInterface
from core.player import Player

class XMLHandler(DBInterface):
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def add_player(self, player):
        doc = xml.dom.minidom.parse(self.xml_file)
        root = doc.documentElement

        player_element = doc.createElement("player")

        full_name = doc.createElement("full_name")
        full_name.appendChild(doc.createTextNode(player.full_name))
        player_element.appendChild(full_name)

        birth_date = doc.createElement("birth_date")
        birth_date.appendChild(doc.createTextNode(player.birth_date))
        player_element.appendChild(birth_date)

        football_team = doc.createElement("football_team")
        football_team.appendChild(doc.createTextNode(player.football_team))
        player_element.appendChild(football_team)

        home_city = doc.createElement("home_city")
        home_city.appendChild(doc.createTextNode(player.home_city))
        player_element.appendChild(home_city)

        squad = doc.createElement("squad")
        squad.appendChild(doc.createTextNode(player.squad))
        player_element.appendChild(squad)

        position = doc.createElement("position")
        position.appendChild(doc.createTextNode(player.position))
        player_element.appendChild(position)

        root.appendChild(player_element)

        with open(self.xml_file, "w", encoding="utf-8") as f:
            doc.writexml(f)

    def search_players(self, criteria=None, offset=None, limit=None):
        criteria = criteria or {}  # Set criteria to an empty dictionary if it's None

        class PlayerHandler(xml.sax.ContentHandler):
            def __init__(self):
                self.players = []
                self.current_player = None
                self.current_data = ""

            def startElement(self, name, attrs):
                if name == "player":
                    self.current_player = Player("", "", "", "", "", "")

            def endElement(self, name):
                if name == "player":
                    if self.current_player.birth_date == "":
                        self.current_player.birth_date = "1900-01-01"  # Default value for birth date
                    self.players.append(self.current_player)
                    self.current_player = None
                elif name == "full_name":
                    self.current_player.full_name = self.current_data
                elif name == "birth_date":
                    self.current_player.birth_date = self.current_data
                elif name == "football_team":
                    self.current_player.football_team = self.current_data
                elif name == "home_city":
                    self.current_player.home_city = self.current_data
                elif name == "squad":
                    self.current_player.squad = self.current_data
                elif name == "position":
                    self.current_player.position = self.current_data
                self.current_data = ""

            def characters(self, content):
                self.current_data = content

        handler = PlayerHandler()
        xml.sax.parse(self.xml_file, handler)

        players = handler.players
        filtered_players = [p for p in players if all(getattr(p, key) == value for key, value in criteria.items())]

        if offset is not None:
            filtered_players = filtered_players[offset:]

        if limit is not None:
            filtered_players = filtered_players[:limit]

        return filtered_players

    def get_players_count(self, criteria=None):
        players = self.search_players(criteria)
        return len(players)

    def delete_players(self, criteria):
        players = self.search_players(criteria)
        doc = xml.dom.minidom.parse(self.xml_file)
        root = doc.documentElement

        for player in players:
            for node in root.getElementsByTagName("player"):
                if all(node.getElementsByTagName(key)[0].firstChild.data == value for key, value in criteria.items()):
                    root.removeChild(node)

        with open(self.xml_file, "w", encoding="utf-8") as f:
            doc.writexml(f)

        return len(players)
