from pymongo import MongoClient

# This is the number of times a user sees a flashcard.
# 0 means they haven't studied it yet, 1 means it is their first time, and so on.
# It is also referred to as n in some of the documentation.
REPETITIONS_DEFAULT: int = 0
# This is also referred to as the easiness factor or EFactor or EF.
# It is multiplier used to increase the "space" in spaced repetition.
# The range is from 1.3 to 2.5
EASINESS_DEFAULT: float = 2.5
# This is the length of time (in days) between repetitions.
# It is the "space" of spaced repetition
INTERVAL_DEFAULT: int = 1

class data_base_:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['users']
    def add(self, person, question: str, answer: str) -> None:
        self.db[str(person)].insert_one({ # TODO: Asegurarse que no esta repe la pregunta
                                            "question": question,
                                            "answer": answer,
                                            "repetitions": REPETITIONS_DEFAULT,
                                            "easiness": EASINESS_DEFAULT,
                                            "interval": INTERVAL_DEFAULT
                                  })
    def get(self, person):
        return self.db[str(person)].find_one(sort=[("interval", 1)])
    def get_all(self, person):
        return self.db[str(person)].find()
    def delete(self, person, questions: list[str]):
        for question in questions:
            self.db[str(person)].delete_one( {"question": question} )
    def update_quality(self, person, card, quality):
        new_easiness, new_interval, new_repetitions = update_quality(card['interval'], card['easiness'], card['repetitions'], quality)
        self.db[str(person)].update_one({
                                            '_id': card['_id']
                                        },
                                        {
                                            '$set': {
                                                'easiness': new_easiness,
                                                'interval': new_interval,
                                                'repetitions': new_repetitions,
                                            }
                                        }, upsert=False)

    def isEmpty(self, person):
        return self.db[str(person)].find_one() == None

def update_quality(interval, easiness, repetitions, quality):
    assert quality >= 0 and quality <= 5

    easiness = max(1.3, easiness + 0.1 - (5.0 - quality) * (0.08 + (5.0 - quality) * 0.02))

    if quality < 3: repetitions = 0
    else: repetitions += 1

    if repetitions == 1: interval = 2
    elif repetitions == 2: interval = 6
    else: interval = round(interval * easiness)
    return [easiness, interval, repetitions]

data_base = data_base_()
