from model.group import Group


class SearchCriteria:
    def __init__(self, group: Group | None = None, name: str | None = None,
                 criteria: dict | None = None, page_number: int = 1, page_size: int = 10):
        self.group = group
        self.name = name
        self.criteria = criteria
        self.page_number: int = page_number
        self.page_size: int = page_size
