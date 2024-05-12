class Review:
    def __init__(self):
        self.text_comments = []
        self.marks = []

    def AddComm(self, text, mark):
        self.text_comments.insert(len(self.text_comments)+1, text)
        self.marks.insert(len(self.marks)+1,mark)

    def PrintComms(self):
        i = 0
        if len(self.text_comments) == 0:
            print("У этого продукта нету комментариев.")
        while i < len(self.text_comments):
            print(f'Комментарий №{i+1} : {self.text_comments[i]} | Оценка: {self.marks[i]}')
            i += 1
