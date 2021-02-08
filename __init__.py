from mycroft import MycroftSkill, intent_file_handler


class PokerHands(MycroftSkill):
    def __init__(self):
        self.STATE_REPRESENTATION = [None, None] # length should correspond to # of possible states (first card, second, third...) -> needs to be dynamic
                                                 # first slot for first card, second slot for second card
        self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):
        #### first idea
        # hand_combination = message.data.get('combination')
        # if hand_combination == 'pair':
        #     result = "two cards of the same rank"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == 'two pair':
        #     result = "two different pairs"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == ('three of a kind' or "trips" or "set"):
        #     result = "three cards of the same rank"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == "straight":
        #     result = "five cards in a sequence, but not of the same suit"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == 'flush':
        #     result = "any five cards of the same suit, but not in a sequence"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == ('full house' or "boat"):
        #     result = "three of a kind with a pair"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == ('four of a kind' or "quads"):
        #     result = "all four cards of the same rank"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == 'straight flush':
        #     result = "five cards in a sequence, all in the same suit"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # elif hand_combination == ('royal flush' or "royal"):
        #     result = "ace, king, queen, jack, ten, all the same suit"
        #     self.speak_dialog('hands.poker', data={"result": result})
        # else:
        #     self.speak_dialog('hands.poker.all.wrong')

        #### second idea
        #STATE_REPRESENTATION = [None, None]
        #cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
        first_card = message.data.get('first_card')
        second_card = message.data.get('second_card')
        
        if (first_card not in self.cards) and (second_card not in self.cards): # both card were misunderstood
            self.speak_dialog('hands.poker.all.wrong')
        
        elif (first_card not in self.cards) and (second_card in self.cards): # first card was misunderstood
            self.STATE_REPRESENTATION = [None, second_card]
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (first_card in self.cards) and (second_card not in self.cards): # second card was misunderstood
            self.STATE_REPRESENTATION = [first_card, None]
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.STATE_REPRESENTATION = [first_card, second_card]
            if first_card == second_card:
                result = f"it is a pair of {first_card}"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})
            else:
                result = f"{first_card} and {second_card} is not a pair"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('first.card.hands.poker.intent')
    def handle_first_card_hands_poker(self, message):    
        first_card = message.data.get('first_card')
        if first_card not in self.cards:
           self.speak_dialog('still.no.hands.poker') 
        else:
            self.STATE_REPRESENTATION[0] = first_card
            if first_card == self.STATE_REPRESENTATION[1]:
                result = f"it is a pair of {first_card}"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})
            else:
                result = f"{first_card} and {self.STATE_REPRESENTATION[1]} is not a pair"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('second.card.hands.poker.intent')
    def handle_second_card_hands_poker(self, message):    
        second_card = message.data.get('second_card')
        if second_card not in self.cards:
           self.speak_dialog('still.no.hands.poker') 
        else:
            self.STATE_REPRESENTATION[1] = second_card
            if self.STATE_REPRESENTATION[0] == second_card:
                result = f"it is a pair of {self.STATE_REPRESENTATION[0]}"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})
            else:
                result = f"{self.STATE_REPRESENTATION[0]} and {second_card} is not a pair"
                self.STATE_REPRESENTATION = [None, None]
                self.speak_dialog('hands.poker', data={"result": result})

def create_skill():
    return PokerHands()

