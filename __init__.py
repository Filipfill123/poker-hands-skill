from mycroft import MycroftSkill, intent_file_handler
from StateRepresenation_test import StateRepresentation
import datetime


class PokerHands(MycroftSkill):
    def __init__(self):
        self.skill_name = "poker_hands"
        self.no_of_slates = 2 # 2 cards
        self.compulsory_slates = 2 # both cards need to be known
        self.possible_outcomes = = ["no_pair", "in_progress", "pair"]
        self.STATE_REPRESENTATION = StateRepresentation(self.skill_name, self.no_of_slates, self.compulsory_slates, self.possible_outcomes)
        # STATE_REPRESENTATION should be connection of user's intention + agent's state + task being "worked on"
        # states of task - ["in_progress" - in progress (the task is being worked on), "pair" - it's a pair, "no_pair" - it's not a pair]
        # states of slots - first value - card (if None, not understood or not answered yet), second value = [None - empty, "not_confirmed" - not confirmed, "confirmed" - confirmed, "inconsistent" - more than one value for slot]
                                                                        
        self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):

        first_card = message.data.get('first_card')
        second_card = message.data.get('second_card')
        
        if (first_card not in self.cards) and (second_card not in self.cards): # both card were misunderstood
            self.speak_dialog('hands.poker.all.wrong')
        
        elif (first_card not in self.cards) and (second_card in self.cards): # first card was misunderstood
            self.STATE_REPRESENTATION.set_card_not_cofirmed(second_card,2)
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (first_card in self.cards) and (second_card not in self.cards): # second card was misunderstood
            self.STATE_REPRESENTATION.set_card_not_cofirmed(first_card,1)
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.STATE_REPRESENTATION['agent']['first_card'] = [first_card, "not_confirmed"]
            self.STATE_REPRESENTATION['agent']['second_card'] = [second_card,"not_confirmed"]
            self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':second_card})
            
    @intent_file_handler('first.card.hands.poker.intent')
    def handle_first_card_hands_poker(self, message):
        first_card = message.data.get('first_card')
        if self.STATE_REPRESENTATION.get_card(1) is not None:
            result = f"I already know the first card. It is {self.STATE_REPRESENTATION.get_card(1)}. Please, what is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.get_card(2) is None and first_card in self.cards:    
            self.STATE_REPRESENTATION.set_card_not_cofirmed(first_card, 1)
            result = f"The first card is {first_card}. What is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})   
        else:
            if first_card not in self.cards:
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "first card"}) 
            else:
                self.STATE_REPRESENTATION.set_card_not_cofirmed(first_card, 1)
                self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':self.STATE_REPRESENTATION.get_card(2)})

    @intent_file_handler('second.card.hands.poker.intent')
    def handle_second_card_hands_poker(self, message):
        second_card = message.data.get('second_card')
        if self.STATE_REPRESENTATION.get_card(2) is not None:
            result = f"I already know the second card. It is {self.STATE_REPRESENTATION.get_card(2)}. Please, what is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.get_card(1) and second_card in self.cards:
            self.STATE_REPRESENTATION.set_card_not_cofirmed(second_card, 2)
            result = f"The second card is {second_card}. What is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        else:    
            if second_card not in self.cards:
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "second card"}) 
            else:
                self.STATE_REPRESENTATION.set_card_not_cofirmed(second_card, 2)
                
                self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION.get_card(1), 'second_card':second_card})


    @intent_file_handler('confirm.both.cards.intent')
    def handle_confirm_both_cards_intent(self, message):
        self.STATE_REPRESENTATION.set_card_cofirmed(1)
        self.STATE_REPRESENTATION.set_card_cofirmed(2)

    
        if self.STATE_REPRESENTATION.get_card(1) == self.STATE_REPRESENTATION.get_card(2):
            result = f"it is a pair of {self.STATE_REPRESENTATION.get_card(1)}s"
            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_pair()
            time = datetime.datetime.now()
            with open("logs/log.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = pair"
            
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.get_card(1)} and {self.STATE_REPRESENTATION.get_card(2)} is not a pair"

            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_no_pair()
            with open("logs/log.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = no_pair"

            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.first.card.intent')
    def handle_confirm_first_card_intent(self, message):
        self.STATE_REPRESENTATION.set_card_cofirmed(1)
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION.set_card_value_confirmed(second_card, 2)

        if self.STATE_REPRESENTATION.get_card(1) == self.STATE_REPRESENTATION.get_card(2):
            result = f"it is a pair of {self.STATE_REPRESENTATION.get_card(1)}s"

            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_pair()
            with open("logs/log.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = pair")

            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.get_card(1)} and {self.STATE_REPRESENTATION.get_card(2)} is not a pair"

            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_no_pair()
            with open("logs/log.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = no_pair")
            self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('confirm.second.card.intent')
    def handle_confirm_second_card_intent(self, message):
        self.STATE_REPRESENTATION.set_card_cofirmed(2)
        first_card = message.data.get('first_card')
        self.STATE_REPRESENTATION.set_card_value_confirmed(first_card, 1)

        if self.STATE_REPRESENTATION.get_card(1) == self.STATE_REPRESENTATION.get_card(2):
            result = f"it is a pair of {self.STATE_REPRESENTATION.get_card(1)}s"

            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_pair()
            with open("logs/log.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = pair")
            
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.get_card(1)} and {self.STATE_REPRESENTATION.get_card(2)} is not a pair"

            self.STATE_REPRESENTATION.delete_state_representation()
            self.STATE_REPRESENTATION.set_outcome_no_pair()
            with open("logs/logg.txt", "w") as logging:
                write.logging(f"{time}: {self.STATE_REPRESENTATION.get_card(1)} + {self.STATE_REPRESENTATION.get_card(2)} = no_pair")
            
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.no.cards.intent')
    def handle_confirm_no_cards_intent(self, message):
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result":""})
    
    @intent_file_handler('kill.intent')
    def handle_kill(self, message):
        if self.STATE_REPRESENTATION.get_card(1) is None and self.STATE_REPRESENTATION.get_card(2) is None:
            result = f"Wait a second, your highness. I looked really hard but my state representation seems to be empty already. Please, don't kill me"
        elif self.STATE_REPRESENTATION.get_card(1) is None and self.STATE_REPRESENTATION.get_card(2) is not None:
            result = f"The first card was empty, the second card was {self.STATE_REPRESENTATION.get_card(2)}"
        elif self.STATE_REPRESENTATION.get_card(1) is not None and self.STATE_REPRESENTATION.get_card(2) is None:    
            result = f"The first card was {self.STATE_REPRESENTATION.get_card(1)}, the second card was empty"
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result": result})

    @intent_file_handler('show.intent')
    def handle_show(self, message):
        if self.STATE_REPRESENTATION.get_card(1) is None and self.STATE_REPRESENTATION.get_card(2) is None:
            result = f"The state representation is empty, my lord"
        elif self.STATE_REPRESENTATION.get_card(1) is None and self.STATE_REPRESENTATION.get_card(2) is not None:
            result = f"The first card is empty, the second card is {self.STATE_REPRESENTATION.get_card(2)}"
        elif self.STATE_REPRESENTATION.get_card(1) is not None and self.STATE_REPRESENTATION.get_card(2) is None:    
            result = f"The first card is {self.STATE_REPRESENTATION.get_card(1)}, the second card is empty"

        self.speak_dialog('show', data={"result": result})

def create_skill():
    return PokerHands()
