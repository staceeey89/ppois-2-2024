import xml.dom.minidom
from typing import List
from xml.sax import ContentHandler

from model.entity.Player import Player
from model.EmptyListStorage import EmptyListStorage


class PlayerHandler(ContentHandler):
    def __init__(self):
        self.current_tag = ""
        self.current_player = None
        self.players = []

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "player":
            self.current_player = {'id': attributes['id']}

    def endElement(self, tag):
        if tag == "player":
            self.players.append(self.current_player)
            self.current_player = None
        self.current_tag = ""

    def characters(self, content):
        if self.current_player is not None:
            self.current_player[self.current_tag] = content


class XmlPlayerController(EmptyListStorage):
    def __init__(self, file):
        super().__init__()
        self.file: str = file
        self._players: List[Player] = self.__load_players_from_xml()

    def __load_players_from_xml(self):
        handler = PlayerHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.file)

        player_list = []
        for player_data in handler.players:
            player = Player(player_data['id'], player_data['full_name'], player_data['birth_date'],
                            player_data['football_team'], player_data['home_city'], int(player_data['team_size']),
                            player_data['position'])
            player_list.append(player)

        return player_list

    def __save_players_to_xml(self):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("players")
        doc.appendChild(root)
        for player in self._players:
            player_element = doc.createElement("player")
            for key, value in player.__dict__.items():
                if key != 'id':
                    element = doc.createElement(key)
                    element.appendChild(doc.createTextNode(str(value)))
                    player_element.appendChild(element)
            player_element.setAttribute("id", str(player.__dict__['id']))
            root.appendChild(player_element)
        with open(self.file, "w") as f:
            f.write(doc.toprettyxml(indent="  "))

    def save(self):
        self.__save_players_to_xml()
