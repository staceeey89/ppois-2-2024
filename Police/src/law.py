class Law:
    def __init__(self, title, jurisdiction, description, penalty):
        self.name = title
        self.jurisdiction = jurisdiction
        self.description = description
        self.penalty = penalty

    def __str__(self):
        return f"{self.name} - {self.penalty}"
