from mycroft import MycroftSkill, intent_file_handler


class PokerHands(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):
        self.speak_dialog('hands.poker')


def create_skill():
    return PokerHands()

