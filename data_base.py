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

class DataBase:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://GGCristo:764319@cluster0.kndqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        self.db = self.client['users']

    def add(self, user, question: str, answer: str) -> bool:
        if self.db[str(user)].find_one( {'question': question} ) == None:
            self.db[str(user)].insert_one({
                                            'question': question,
                                            'answer': answer,
                                            'repetitions': REPETITIONS_DEFAULT,
                                            'easiness': EASINESS_DEFAULT,
                                            'interval': INTERVAL_DEFAULT
                                    })
            return True
        return False

    def get(self, user: int):
        self.db[str(user)].update_one({
                                          'type': 'information'
                                      },
                                      {
                                          '$inc': {'cards_received': 1}
                                      }, upsert=True)
        return self.db[str(user)].find_one({
                                               'question': {'$exists':True},
                                               'answer': {'$exists':True},
                                               'interval': {'$exists':True},
                                           },
                                           sort=[("interval", 1)])

    def get_all(self, user: int):
        return self.db[str(user)].find({
                                           'question': {'$exists': True}
                                       })

    def delete(self, user: int, questions: list[str]):
        for question in questions:
            self.db[str(user)].delete_one( {'question': question} )

    def update_quality(self, user: int, card, quality: int):
        new_easiness, new_interval, new_repetitions = update_quality(card['interval'], card['easiness'], card['repetitions'], quality)
        self.db[str(user)].update_one({
                                          '_id': card['_id']
                                      },
                                      {
                                          '$set': {
                                              'easiness': new_easiness,
                                              'interval': new_interval,
                                              'repetitions': new_repetitions,
                                          }
                                      })

    def reset(self, user: int):
        self.db[str(user)].update_many({
                                           'question': {'$exists':True},
                                           'answer': {'$exists':True}
                                       },
                                       {
                                           '$set': {
                                               "interval": INTERVAL_DEFAULT,
                                               "easiness": EASINESS_DEFAULT,
                                               "repetitions": REPETITIONS_DEFAULT
                                           }
                                       })
        self.db[str(user)].update_one({
                                          'type': 'information'
                                      },
                                      {
                                          '$set': {
                                              'cards_received':0
                                          }
                                      })
    def info(self, user: int):
        cards_received = self.db[str(user)].find_one({
                                                         'type': 'information'
                                                     },
                                                     {
                                                         '_id': False,
                                                         'cards_received':True
                                                     })["cards_received"] 


        return {
            'number_cards': self.db[str(user)].count_documents({
                                                                   'question': {'$exists':True},
                                                                   'answer': {'$exists':True}
                                                               },
                                                               ),
            'cards_received': cards_received if cards_received != None else 0
        }


    def isEmpty(self, user: int) -> bool:
        return self.db[str(user)].find_one() == None

def update_quality(interval, easiness, repetitions, quality):
    assert quality >= 0 and quality <= 5

    easiness = max(1.3, easiness + 0.1 - (5.0 - quality) * (0.08 + (5.0 - quality) * 0.02))

    if quality < 3: repetitions = 0
    else: repetitions += 1

    if repetitions == 1: interval = 2
    elif repetitions == 2: interval = 6
    else: interval = round(interval * easiness)
    return [easiness, interval, repetitions]

data_base = DataBase()
