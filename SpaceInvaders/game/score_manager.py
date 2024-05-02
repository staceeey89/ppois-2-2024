import json


class ScoreManager:
    def __init__(self, filename):
        self.filename = filename

    def save_scores(self, scores):
        with open(self.filename, 'w') as file:
            json.dump(scores, file)

    def load_scores(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def add_score(self, name, score):
        scores = self.load_scores()
        scores[name] = score
        self.save_scores(scores)

    def get_max_score(self):
        scores = self.load_scores()
        if scores:
            max_score = max(scores.values())
            print(list(scores.values()))
            return max_score
        else:
            return None
