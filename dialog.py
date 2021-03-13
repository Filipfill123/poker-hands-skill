Value("value") == "value"

Value("value", confidence=0.9)
Value("value", confirmed=True)
Value("value1", "value2")

Value(confirmed=True) == VALUE_CONFIRMED

class foo:
    @intent_file_handler('hands.poker.intent')
    def handle_hands_poker(self, message):

        first_card = message.data.get('first_card')
        second_card = message.data.get('second_card')
        
        if (not self.state.first_card.is_valid(first_card)
        and not self.state.second_card.is_valid(second_card)):
            # both card were misunderstood
            self.speak_dialog('hands.poker.all.wrong')
        
        elif (first_card not in self.cards) and (second_card in self.cards): # first card was misunderstood
            self.state.second_card = second_card
            self.speak_dialog('hands.poker.first.wrong', data={"second_card": second_card})
        
        elif (first_card in self.cards) and (second_card not in self.cards): # second card was misunderstood
            self.state.first_card = Value(first_card, confidence=1.0)
            self.speak_dialog('hands.poker.second.wrong', data={"first_card": first_card})
        
        else:
            self.state.first_card = first_card
            self.state.second_card = second_card
            self.speak_dialog('confirm.cards',data={'first_card':first_card, 'second_card':second_card})

    @intent_file_handler('confirm.both.cards.intent')
    def handle_confirm_both_cards_intent(self, message):
        self.state.first_card = Value(confirmed=True)
        self.state.second_card = Value(confirmed=True)
        time = datetime.datetime.now()

        if self.state.first_card == self.state.second_card:
            result = f"it is a pair of {self.state.first_card}s"
            self.state.set_task_state("pair")
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.state.first_card} + {self.state.second_card} = {self.state.get_task_state()} \n")
            self.state.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
        else:
            result = f"{self.state.first_card} and {self.state.second_card} is not a pair"
            self.state.set_task_state("no_pair")
            with open("/home/polakf/DP/mycroft-core/skills/poker-hands-skill/logs/log.txt", "w+") as logging:
                logging.write(f"{time}: {self.state.first_card} + {self.state.second_card} = {self.state.get_task_state()} \n")
            self.state.delete_state_representation()
            self.speak_dialog('hands.poker', data={"result": result})
