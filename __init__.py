from mycroft import MycroftSkill, intent_file_handler
import sys
sys.path.append('/opt/mycroft/skills/poker-hands-skill')
#from StateRepresenation import StateRepresentation
from sample import Slot, Value, State, Cards
import datetime


class PokerHands(MycroftSkill):
    def __init__(self):
        self.skill_name = type(self).__name__
        
        self.STATE_REPRESENTATION = State()
        self.STATE_REPRESENTATION.new_slots(first_card=Cards, second_card=Cards, task_state=Value)

        
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):

        first_card = message.data.get('first_card')
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION.push(first_card=first_card, second_card=second_card)

        if (not self.STATE_REPRESENTATION.first_card.first_value) and (not self.STATE_REPRESENTATION.second_card.first_value): # both card were misunderstood
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
            self.speak_dialog('hands.poker.all.wrong')
        
        elif (not self.STATE_REPRESENTATION.first_card.first_value) and (self.STATE_REPRESENTATION.second_card.first_value): # first card was misunderstood
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.first_card)
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (self.STATE_REPRESENTATION.first_card.first_value) and (not self.STATE_REPRESENTATION.second_card.first_value): # second card was misunderstood
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.second_card)
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.confirm_unconfirmed, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
            self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':second_card})
            
    @intent_file_handler('first.card.hands.poker.intent')
    def handle_first_card_hands_poker(self, message):
        first_card = message.data.get('first_card')
        self.STATE_REPRESENTATION.push(first_card=first_card)
        if len(self.STATE_REPRESENTATION.first_card.all_values) > 1:
            result = f"You said {first_card} but you already said the first card. It was {self.STATE_REPRESENTATION.first_card.first_value}. From the cards {self.STATE_REPRESENTATION.first_card.all_values} which do you want to choose?"
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.disambig, self.STATE_REPRESENTATION.first_card)
            self.speak_dialog('hands.poker', data={"result": result})
        elif (not self.STATE_REPRESENTATION.second_card.first_value) and (self.STATE_REPRESENTATION.first_card.first_value): 
            result = f"The first card is {first_card}. What is the second card?"
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.second_card)
            self.speak_dialog('hands.poker', data={"result": result})   
        else:
            if not self.STATE_REPRESENTATION.first_card.first_value:
                self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "first card"}) 
            else:
                self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.confirm_unconfirmed, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
                self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':self.STATE_REPRESENTATION.second_card.first_value})

    @intent_file_handler('second.card.hands.poker.intent')
    def handle_second_card_hands_poker(self, message):
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION.push(second_card=second_card)
        if len(self.STATE_REPRESENTATION.second_card.all_values) > 1:
            result = f"You said {second_card} but you already said the second card. It was {self.STATE_REPRESENTATION.second_card.first_value}. From the cards {self.STATE_REPRESENTATION.second_card.all_values} which one do you want to choose?"
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.disambig, self.STATE_REPRESENTATION.second_card)
            self.speak_dialog('hands.poker', data={"result": result})
        elif (not self.STATE_REPRESENTATION.first_card.first_value) and (self.STATE_REPRESENTATION.second_card.first_value):
            self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.first_card)
            result = f"The second card is {second_card}. What is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        else:    
            if not self.STATE_REPRESENTATION.second_card.first_value:
                self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.complete_empty, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "second card"}) 
            else:
                self.STATE_REPRESENTATION.expect(self.STATE_REPRESENTATION.confirm_unconfirmed, self.STATE_REPRESENTATION.first_card, self.STATE_REPRESENTATION.second_card)
                self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION.first_card.first_value, 'second_card':second_card})


    @intent_file_handler('confirm.both.cards.intent')
    def handle_confirm_both_cards_intent(self, message):
        # TODO confirming
        time = datetime.datetime.now()

        if  self.STATE_REPRESENTATION.first_card.first_value ==  self.STATE_REPRESENTATION.second_card.first_value:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.first_value}s"
            # self.STATE_REPRESENTATION.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation() #TODO
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.first_value} and {self.STATE_REPRESENTATION.second_card.first_value} is not a pair"
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'no_pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.first.card.intent')
    def handle_confirm_first_card_intent(self, message):
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION.assign(second_card=second_card)
        time = datetime.datetime.now()
        if not self.STATE_REPRESENTATION.second_card.first_value:
            result = f"{second_card} is not a valid card. Please, say the second card again"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.first_card.first_value ==  self.STATE_REPRESENTATION.second_card.first_value:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.first_value}s"
            # self.STATE_REPRESENTATION.task_state.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.first_value} and {self.STATE_REPRESENTATION.second_card.first_value} is not a pair"
            self.STATE_REPRESENTATION.task_state.state = Value(state='no_pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'no_pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('confirm.second.card.intent')
    def handle_confirm_second_card_intent(self, message):
        first_card = message.data.get('first_card')
        self.STATE_REPRESENTATION.assign(first_card=first_card)
        time = datetime.datetime.now()
        if not self.STATE_REPRESENTATION.first_card.first_value:
            result = f"{first_card} is not a valid card. Please, say the first card again"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.first_card.first_value ==  self.STATE_REPRESENTATION.second_card.first_value:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.first_value}s"
            # self.STATE_REPRESENTATION.task_state.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.value_confidence} and {self.STATE_REPRESENTATION.second_card.first_value} is not a pair"
            self.STATE_REPRESENTATION.set_task_state("no_pair")
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.first_value} + {self.STATE_REPRESENTATION.second_card.first_value} = 'no_pair' \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.no.cards.intent')
    def handle_confirm_no_cards_intent(self, message):
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result":""})

    @intent_file_handler('choose.second.card.intent')
    def handle_choose_second_card_intent(self, message):
        card_value = message.data.get('card_value')
        self.STATE_REPRESENTATION.push(second_card=[card_value])
        if not self.STATE_REPRESENTATION.first_card.first_value:
            result = f"You chose {card_value} for the second card but the first card is empty. What is the first card?"
            self.speak_dialog('hands.poker', data={"result":result})
        elif len(self.STATE_REPRESENTATION.first_card.all_values) > 1:
            result = f"You chose {card_value} for the second card but you need to specify the first card. From the cards {self.STATE_REPRESENTATION.first_card.all_values} which do you want to choose?"
            self.speak_dialog('hands.poker', data={"result":result})
        else:
            self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION.first_card.first_value, 'second_card':self.STATE_REPRESENTATION.second_card.first_value})

    @intent_file_handler('choose.first.card.intent')
    def handle_choose_first_card_intent(self, message):
        card_value = message.data.get('card_value')
        self.STATE_REPRESENTATION.push(first_card=[card_value])
        if not self.STATE_REPRESENTATION.second_card.first_value:
            result = f"You chose {card_value} for the first card but the second card is empty. What is the second card?"
            self.speak_dialog('hands.poker', data={"result":result})
        elif len(self.STATE_REPRESENTATION.second_card.all_values) > 1:
            result = f"You chose {card_value} for the first card but you need to specify the second card. From the cards {self.STATE_REPRESENTATION.second_card.all_values} which do you want to choose?"
            self.speak_dialog('hands.poker', data={"result":result})
        else:
            self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION.first_card.first_value, 'second_card':self.STATE_REPRESENTATION.second_card.first_value})

    @intent_file_handler('kill.intent')
    def handle_kill(self, message):
        if (not self.STATE_REPRESENTATION.first_card.first_value) and (not self.STATE_REPRESENTATION.second_card.first_value):
            result = f"Wait a second, your highness. I looked really hard but my state representation seems to be empty already. Please, don't kill me"
        elif not self.STATE_REPRESENTATION.first_card.first_value and self.STATE_REPRESENTATION.second_card.first_value:
            result = f"The first card was empty, the second card was {self.STATE_REPRESENTATION.second_card.first_value}"
        elif self.STATE_REPRESENTATION.first_card.first_value and not self.STATE_REPRESENTATION.second_card.first_value:    
            result = f"The first card was {self.STATE_REPRESENTATION.first_card.first_value}, the second card was empty"
        elif self.STATE_REPRESENTATION.first_card.first_value and self.STATE_REPRESENTATION.second_card.first_value:    
            result = f"The first card was {self.STATE_REPRESENTATION.first_card.first_value}, the second card was {self.STATE_REPRESENTATION.second_card.first_value}"
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result": result})

    @intent_file_handler('show.intent')
    def handle_show(self, message):
        if (not self.STATE_REPRESENTATION.first_card.first_value) and (not self.STATE_REPRESENTATION.second_card.first_value):
            result = f"The state representation is empty, my lord"
        elif not self.STATE_REPRESENTATION.first_card.first_value and self.STATE_REPRESENTATION.second_card.first_value:
            result = f"The first card is empty, the second card is {self.STATE_REPRESENTATION.second_card.first_value}"
        elif self.STATE_REPRESENTATION.first_card.first_value and not self.STATE_REPRESENTATION.second_card.first_value:    
            result = f"The first card is {self.STATE_REPRESENTATION.first_card.first_value}, the second card is empty"
        elif self.STATE_REPRESENTATION.first_card.first_value and self.STATE_REPRESENTATION.second_card.first_value:    
            result = f"The first card is {self.STATE_REPRESENTATION.first_card.first_value}, the second card is {self.STATE_REPRESENTATION.second_card.first_value}"

        self.speak_dialog('show', data={"result": result})

def create_skill():
    return PokerHands()
