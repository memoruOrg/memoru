class Card_:
    def __init__(self, question: str, answer: str):
        self.quality: int = 0
        self.question: str = question
        self.answer: str = answer

class cardSlice_:
    def __init__(self):
        self.slice: list[Card_] = []
        self.index: int = 0
        print("Constructor")
    def add(self, question: str, answer: str) -> None:
        self.slice.append(Card_(question, answer))
        sorted(self.slice, key=lambda card: card.quality)
    def get(self) -> Card_:
        self.index += 1
        return self.slice[self.index - 1] # TODO: que no te salga la misma pregunta seguida

cardSlice = cardSlice_()
