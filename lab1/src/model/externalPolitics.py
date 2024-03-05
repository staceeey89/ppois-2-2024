from src.model.externalRelation import ExternalRelation
import src.model.state as state

class ExternalPolitics:
    def __init__(self):
        self._external_relations = []

    @property
    def relations(self):
        return self._external_relations

    def add_external_relation(self, external_relation: ExternalRelation):
        self._external_relations.append(external_relation)

    def get_external_relation(self, state_: state.State):
        try:
            return filter(lambda x: x.other_state == state_, self._external_relations)[0]
        except IndexError:
            raise ValueError()

    def remove_external_relation(self, external_relation: ExternalRelation):
        self._external_relations.remove(external_relation)
