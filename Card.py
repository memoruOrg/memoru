class Card_:
    def __init__(self, question: str, answer: str):
        # Also known as quality of assessment.
        # This is how difficult (as defined by the user) a flashcard is.
        # The scale is from 0 to 5
        self.quality: int = 0
        # This is the number of times a user sees a flashcard.
        # 0 means they haven't studied it yet, 1 means it is their first time, and so on.
        # It is also referred to as n in some of the documentation.
        self.repetitions: int = 0
        # This is also referred to as the easiness factor or EFactor or EF.
        # It is multiplier used to increase the "space" in spaced repetition.
        # The range is from 1.3 to 2.5
        self.easiness: float = 2.5
        # This is the length of time (in days) between repetitions.
        # It is the "space" of spaced repetition
        self.interval: int = 1
        self.question: str = question
        self.answer: str = answer
    def updateQuality(self, quality: int):
        assert quality >= 0 and quality <= 5

        self.easiness = max(1.3, self.easiness + 0.1 - (5.0 - quality) * (0.08 + (5.0 - quality) * 0.02))

        if quality < 3: self.repetitions = 0
        else: self.repetitions += 1

        if self.repetitions == 1: self.interval = 2
        elif self.repetitions == 2: self.interval = 6
        else: self.interval = round(self.interval * self.easiness)

class cardSlice_:
    def __init__(self):
        self.slice: list[Card_] = []
        self.index: int = 0
    def add(self, question: str, answer: str) -> None:
        self.slice.append(Card_(question, answer))
    def get(self) -> Card_:
        self.slice = sorted(self.slice, key=lambda card: card.interval)
        for i, _ in enumerate(self.slice[1:]): # Hint por si hay problemas de barajear
            self.slice[i].interval -= 1
        return self.slice[0]
    def updateQuality(self, quality: int):
        self.slice[0].updateQuality(quality)

cardSlice = cardSlice_()
