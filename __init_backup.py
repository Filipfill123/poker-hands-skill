from mycroft import MycroftSkill, intent_file_handler


class PokerHands(MycroftSkill):
    def __init__(self):
        self.skill_name = "poker_hands"
        self.STATE_REPRESENTATION = {'user': self.skill_name,'agent': {"first_card":[None,None],"second_card":[None,None]},'task': "in_progress"}
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

            self.STATE_REPRESENTATION['agent']['second_card'] = [second_card,"not_confirmed"] # the first card stays None
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (first_card in self.cards) and (second_card not in self.cards): # second card was misunderstood

            self.STATE_REPRESENTATION['agent']['first_card'] = [first_card, "not_confirmed"] # the second card stays None
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.STATE_REPRESENTATION['agent']['first_card'] = [first_card, "not_confirmed"]
            self.STATE_REPRESENTATION['agent']['second_card'] = [second_card,"not_confirmed"]
            self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':second_card})
            
    @intent_file_handler('first.card.hands.poker.intent')
    def handle_first_card_hands_poker(self, message):
        first_card = message.data.get('first_card')
        if self.STATE_REPRESENTATION['agent']['first_card'][0] is not None:
            result = f"I already know the first card. It is {self.STATE_REPRESENTATION['agent']['first_card'][0]}. Please, what is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})    
        elif self.STATE_REPRESENTATION['agent']['second_card'][0] is None and first_card in self.cards:
            self.STATE_REPRESENTATION['agent']['first_card'] = [first_card, "not_confirmed"]
            result = f"The first card is {first_card}. What is the second card?"
            self.speak_dialog('hands.poker', data={"result": result})   
        else:
            if first_card not in self.cards:
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "first card"}) 
            else:
                self.STATE_REPRESENTATION['agent']['first_card'] = [first_card, "not_confirmed"]
                self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':self.STATE_REPRESENTATION['agent']['second_card'][0]})

    @intent_file_handler('second.card.hands.poker.intent')
    def handle_second_card_hands_poker(self, message):
        second_card = message.data.get('second_card')
        if self.STATE_REPRESENTATION['agent']['second_card'][0] is not None:
            result = f"I already know the second card. It is {self.STATE_REPRESENTATION['agent']['second_card'][0]}. Please, what is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        elif self.STATE_REPRESENTATION['agent']['first_card'][0] is None and second_card in self.cards:
            self.STATE_REPRESENTATION['agent']['second_card'] = [second_card, "not_confirmed"]
            result = f"The second card is {second_card}. What is the first card?"
            self.speak_dialog('hands.poker', data={"result": result})
        else:    
            if second_card not in self.cards:
                self.speak_dialog('notunderstood.hands.poker',data={'which_card': "second card"}) 
            else:
                self.STATE_REPRESENTATION['agent']['second_card'] = [second_card, "not_confirmed"]
                self.speak_dialog('confirm.cards',data={'first_card':self.STATE_REPRESENTATION['agent']['first_card'][0], 'second_card':second_card})


    @intent_file_handler('confirm.both.cards.intent')
    def handle_confirm_both_cards_intent(self, message):
        self.STATE_REPRESENTATION['agent']['first_card'][1] = "confirmed"
        self.STATE_REPRESENTATION['agent']['second_card'][1] = "confirmed"
        if self.STATE_REPRESENTATION['agent']['first_card'][0] == self.STATE_REPRESENTATION['agent']['second_card'][0]:
            result = f"it is a pair of {self.STATE_REPRESENTATION['agent']['first_card'][0]}s"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION['agent']['first_card'][0]} and {self.STATE_REPRESENTATION['agent']['second_card'][0]} is not a pair"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'no_pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.first.card.intent')
    def handle_confirm_first_card_intent(self, message):
        self.STATE_REPRESENTATION['agent']['first_card'][1] = "confirmed"
        second_card = message.data.get('second_card')
        self.STATE_REPRESENTATION['agent']['second_card'] = [second_card,"confirmed"]

        if self.STATE_REPRESENTATION['agent']['first_card'][0] == self.STATE_REPRESENTATION['agent']['second_card'][0]:
            result = f"it is a pair of {self.STATE_REPRESENTATION['agent']['first_card'][0]}s"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION['agent']['first_card'][0]} and {self.STATE_REPRESENTATION['agent']['second_card'][0]} is not a pair"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'no_pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})

    @intent_file_handler('confirm.second.card.intent')
    def handle_confirm_second_card_intent(self, message):
        self.STATE_REPRESENTATION['agent']['second_card'][1] = "confirmed"
        first_card = message.data.get('first_card')
        self.STATE_REPRESENTATION['agent']['first_card'] = [first_card,"confirmed"]

        if self.STATE_REPRESENTATION['agent']['first_card'][0] == self.STATE_REPRESENTATION['agent']['second_card'][0]:
            result = f"it is a pair of {self.STATE_REPRESENTATION['agent']['first_card'][0]}s"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.STATE_REPRESENTATION['agent']['first_card'][0]} and {self.STATE_REPRESENTATION['agent']['second_card'][0]} is not a pair"
            self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
            self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]
            self.STATE_REPRESENTATION['task'] = 'no_pair'
            #### TODO logging
            self.speak_dialog('hands.poker', data={"result": result})
    
    @intent_file_handler('confirm.no.cards.intent')
    def handle_confirm_no_cards_intent(self, message):
        self.STATE_REPRESENTATION['agent']['first_card'] = [None, None]
        self.STATE_REPRESENTATION['agent']['second_card'] = [None, None]
        self.speak_dialog('kill', data={"result":""})
    
    @intent_file_handler('kill.intent')
    def handle_kill(self, message):

        if self.STATE_REPRESENTATION["agent"]["first_card"][0] is None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is None:
            result = f"Wait a second, your highness. I looked really hard but my state representation seems to be empty already. Please, don't kill me"
        elif self.STATE_REPRESENTATION["agent"]["first_card"][0] is None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is not None:
            result = f"The first card was empty, the second card was {self.STATE_REPRESENTATION['agent']['second_card'][0]}"
        elif self.STATE_REPRESENTATION["agent"]["first_card"][0] is not None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is None:
            result = f"The first card was {self.STATE_REPRESENTATION['agent']['first_card'][0]}, the second card was empty"
        self.STATE_REPRESENTATION["agent"]["first_card"] = [None, None]
        self.STATE_REPRESENTATION["agent"]["second_card"] = [None, None]

        self.speak_dialog('kill', data={"result": result})

    @intent_file_handler('show.intent')
    def handle_show(self, message):

        if self.STATE_REPRESENTATION["agent"]["first_card"][0] is None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is None:
            result = f"The state representation is empty, my lord"
        elif self.STATE_REPRESENTATION["agent"]["first_card"][0] is None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is not None:
            result = f"The first card is empty, the second card is {self.STATE_REPRESENTATION['agent']['second_card'][0]}"
        elif self.STATE_REPRESENTATION["agent"]["first_card"][0] is not None and self.STATE_REPRESENTATION["agent"]["second_card"][0] is None:
            result = f"The first card is {self.STATE_REPRESENTATION['agent']['first_card'][0]}, the second card is empty"

        self.speak_dialog('show', data={"result": result})

def create_skill():
    return PokerHands()

