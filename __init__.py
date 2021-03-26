from mycroft import MycroftSkill, intent_file_handler
import sys
sys.path.append('/opt/mycroft/skills/poker-hands-skill')
#from StateRepresenation import StateRepresentation
from StateRepres import Slot, Value, State
import datetime


class PokerHands(MycroftSkill):
    def __init__(self):
        self.skill_name = type(self).__name__
        
        self.STATE_REPRESENTATION = State()
        self.STATE_REPRESENTATION.first_card = Slot()
        self.STATE_REPRESENTATION.second_card = Slot()
        self.STATE_REPRESENTATION.task_state = Slot()
        # STATE_REPRESENTATION should be connection of user's intention + agent's state + task being "worked on"
        # states of task - ["in_progress" - in progress (the task is being worked on), "pair" - it's a pair, "no_pair" - it's not a pair]
        # states of slots - first value - card (if None, not understood or not answered yet), second value = [None - empty, "not_confirmed" - not confirmed, "confirmed" - confirmed, "inconsistent" - more than one value for slot]
                                                                        
        
        MycroftSkill.__init__(self)

    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):

        first_card = message.data.get('first_card')
        second_card = message.data.get('second_card')
        
        if (not self.STATE_REPRESENTATION.first_card.is_valid(first_card)) and (not self.STATE_REPRESENTATION.second_card.is_valid(second_card)): # both card were misunderstood
            self.speak_dialog('hands.poker.all.wrong')
        
        elif (not self.STATE_REPRESENTATION.first_card.is_valid(first_card)) and (self.STATE_REPRESENTATION.second_card.is_valid(second_card)): # first card was misunderstood
            self.STATE_REPRESENTATION.second_card.value = Value(value=second_card)
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (self.STATE_REPRESENTATION.first_card.is_valid(first_card)) and (not self.STATE_REPRESENTATION.second_card.is_valid(second_card)): # second card was misunderstood
            self.STATE_REPRESENTATION.first_card.value = Value(value=first_card)
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.STATE_REPRESENTATION.first_card.value = Value(value=first_card)
            self.STATE_REPRESENTATION.second_card.value = Value(value=second_card)
            self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':second_card})
            
    @intent_file_handler('first.card.hands.poker.intent')
    def handle_first_card_hands_poker(self, message):
        first_card = message.data.get('first_card')
        if self.STATE_REPRESENTATION.first_card.first_value is not None:
            result = f"I already know the first card. It is {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}. Please, what is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.first_card.is_valid(first_card):    
            self.STATE_REPRESENTATION.first_card.value = Value(value=first_card)
            result = f"The first card is {first_card}. What is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})   
        else:
            if not self.STATE_REPRESENTATION.first_card.is_valid(first_card):
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "first card"}) 
            else:
                self.STATE_REPRESENTATION.first_card.value = Value(value=first_card)
                self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']})

    @intent_file_handler('second.card.hands.poker.intent')
    def handle_second_card_hands_poker(self, message):
        second_card = message.data.get('second_card')
        if self.STATE_REPRESENTATION.second_card.first_value is not None:
            result = f"I already know the second card. It is {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']}. Please, what is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.second_card.is_valid(second_card):
            self.STATE_REPRESENTATION.second_card.value = Value(value=second_card)
            result = f"The second card is {second_card}. What is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        else:    
            if not self.STATE_REPRESENTATION.second_card.is_valid(second_card):
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "second card"}) 
            else:
                self.STATE_REPRESENTATION.second_card.value = Value(value=second_card)
                
                self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'], 'second_card':second_card})


    @intent_file_handler('confirm.both.cards.intent')
    def handle_confirm_both_cards_intent(self, message):
        self.STATE_REPRESENTATION.first_card.state = 'confirmed'
        self.STATE_REPRESENTATION.second_card.state = 'confirmed'
        time = datetime.datetime.now()

        if  self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] ==  self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}s"
            self.STATE_REPRESENTATION.task_state.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation() #TODO
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} and {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} is not a pair"
            self.STATE_REPRESENTATION.task_state.state = Value(state='no_pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.first.card.intent')
    def handle_confirm_first_card_intent(self, message):
        self.STATE_REPRESENTATION.first_card.state = 'confirmed'
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION.second_card.value = Value(value=second_card)
        self.STATE_REPRESENTATION.second_card.state = 'confirmed'
        time = datetime.datetime.now()

        if self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] ==  self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}s"
            self.STATE_REPRESENTATION.task_state.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} and {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} is not a pair"
            self.STATE_REPRESENTATION.task_state.state = Value(state='no_pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('confirm.second.card.intent')
    def handle_confirm_second_card_intent(self, message):
        self.STATE_REPRESENTATION.second_card.state = 'confirmed'
        first_card = message.data.get('first_card')
        self.STATE_REPRESENTATION.first_card.value = Value(value=first_card)
        self.STATE_REPRESENTATION.first_card.state = 'confirmed'
        time = datetime.datetime.now()

        if self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] ==  self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']:
            result = f"it is a pair of {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}s"
            self.STATE_REPRESENTATION.task_state.state = Value(state='pair')
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} and {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} is not a pair"
            self.STATE_REPRESENTATION.set_task_state("no_pair")
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']} + {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']} = {self.STATE_REPRESENTATION.task_state.state.state} \n")
            self.STATE_REPRESENTATION.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.no.cards.intent')
    def handle_confirm_no_cards_intent(self, message):
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result":""})
    
    @intent_file_handler('kill.intent')
    def handle_kill(self, message):
        if (self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is None):
            result = f"Wait a second, your highness. I looked really hard but my state representation seems to be empty already. Please, don't kill me"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is not None:
            result = f"The first card was empty, the second card was {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']}"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is not None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is None:    
            result = f"The first card was {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}, the second card was empty"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is not None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is not None:    
            result = f"The first card was {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}, the second card was {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']}"
        self.STATE_REPRESENTATION.delete_state_representation()

        self.speak_dialog('kill', data={"result": result})

    @intent_file_handler('show.intent')
    def handle_show(self, message):
        if (self.self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is None):
            result = f"The state representation is empty, my lord"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is not None:
            result = f"The first card is empty, the second card is {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']}"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is not None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is None:    
            result = f"The first card is {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}, the second card is empty"
        elif self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value'] is not None and self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value'] is not None:    
            result = f"The first card is {self.STATE_REPRESENTATION.first_card.value[0].value_confidence['value']}, the second card is {self.STATE_REPRESENTATION.second_card.value[0].value_confidence['value']}"

        self.speak_dialog('show', data={"result": result})

def create_skill():
    return PokerHands()
