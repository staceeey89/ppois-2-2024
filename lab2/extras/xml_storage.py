import xml.dom.minidom
from typing import List
from xml.sax import ContentHandler

from extras.empty_list_storage import EmptyListStorage
from extras.tournament import Tournament


class TournamentHandler(ContentHandler):
    def __init__(self):
        self.current_tag = ""
        self.current_tournament = None
        self.tournaments = []

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "tournament":
            self.current_tournament = {'id': attributes['id']}

    def endElement(self, tag):
        if tag == "tournament":
            self.tournaments.append(self.current_tournament)
            self.current_tournament = None
        self.current_tag = ""

    def characters(self, content):
        if self.current_tournament is not None:
            self.current_tournament[self.current_tag] = content


class XmlStorage(EmptyListStorage):
    def __init__(self):
        super().__init__()
        self.file: str = 'data/tournaments.xml'
        self._tournaments: List[Tournament] = self.__load_tournaments_from_xml()

    def __load_tournaments_from_xml(self):
        handler = TournamentHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.file)

        tournament_list = []
        for tournament_data in handler.tournaments:
            tournament = Tournament(tournament_data['id'],
                                    tournament_data['trn_name'],
                                    tournament_data['trn_date'],
                                    tournament_data['trn_sport'],
                                    tournament_data['win_name'],
                                    int(tournament_data['trn_prize']),
                                    int(tournament_data['win_prize']))
            tournament_list.append(tournament)

        return tournament_list

    def __save_tournaments_to_xml(self):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("tournaments")
        doc.appendChild(root)
        for tournament in self._tournaments:
            tournament_element = doc.createElement("tournament")
            for key, value in tournament.__dict__.items():
                if key != 'id':
                    element = doc.createElement(key)
                    element.appendChild(doc.createTextNode(str(value)))
                    tournament_element.appendChild(element)
            tournament_element.setAttribute("id", str(tournament.__dict__['id']))
            root.appendChild(tournament_element)
        with open(self.file, "w") as f:
            f.write(doc.toprettyxml(indent="  "))

    def save(self):
        self.__save_tournaments_to_xml()
