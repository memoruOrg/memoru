class Card_:
    def __init__(self, question: str, answer: str):
        self.quality = 0
        self.question = question
        self.answer = answer

class cardSlice_:
    def __init__(self):
        self.slice = []
        print("Constructor")
    def add(self, question: str, answer: str):
        self.slice.append(Card_(question, answer))
        sorted(self.slice, key=lambda card: card.quality)

cardSlice = cardSlice_()
