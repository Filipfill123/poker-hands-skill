from mycroft import MycroftSkill, intent_file_handler


class PokerHands(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):
        hand_combination = message.data.get('combination')
        if hand_combination == 'pair':
            result = "two cards of the same rank"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == 'two pair':
            result = "two different pairs"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == ('three of a kind' or "trips" or "set"):
            result = "three cards of the same rank"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == "straight":
            result = "five cards in a sequence, but not of the same suit"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == 'flush':
            result = "any five cards of the same suit, but not in a sequence"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == ('full house' or "boat"):
            result = "three of a kind with a pair"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == ('four of a kind' or "quads"):
            result = "all four cards of the same rank"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == 'straight flush':
            result = "five cards in a sequence, all in the same suit"
            self.speak_dialog('hands.poker', data={"result": result})
        elif hand_combination == ('royal flush' or "royal"):
            result = "ace, king, queen, jack, ten, all the same suit"
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            self.speak_dialog('hands.poker.wrong')
        


def create_skill():
    return PokerHands()

