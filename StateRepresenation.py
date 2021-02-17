#### we need state representation initialization:
#### 1) we need states for user intention, 2) task progress
#### 3) we need to know which slates of agent's state are compulsory etc. and the numbers of slates


#### functions:
#### 1) fill slate with either the first UNCONFIRMED card or the second UNCONFIRMED
#### 2) fill slate with both UNCONFIRMED cards ( 1) and 2) SET FUNCTIONS)
#### 3) GET FUNCTIONS for both cards
#### 4) SET FUNCTIONS for CONFIRMED (alternatively change card/s and CONFIRM it/them)
#### 5) DELETE state representation

class StateRepresentation:
    def __init__(self, skill_name, no_of_slates, compulsory_slates, possible_outcomes):
        # possible_outcomes = ["no_pair", "in_progress", "pair"]
        task_state = possible_outcomes[1] # -> only three outcomes - no_pair, in_progress, pair (for simplicity as -1 0 1, hence 0 1 2)
        state_representation = {'user': skill_name,'agent': {},'task': task_state}
        for i in range(no_of_slates):
            state_representation["agent"][f"card_{i+1}"] = [None,None,"compulsory"]
        
        self.no_of_slates = no_of_slates
        self.STATE_REPRESENTATION = state_representation

    def get_card(self, which_card):
        card = self.STATE_REPRESENTATION["agent"][f"card_{which_card}"][0]
        return card
    
    def get_all_cards(self):
        cards = list()
        for i in range(self.no_of_slates):
            cards.append(self.STATE_REPRESENTATION["agent"][f"card_{i+1}"][0])
        return cards

    def set_card_not_cofirmed(self, card_value, which_card):
        self.STATE_REPRESENTATION["agent"][f"card_{which_card}"] = [card_value,"not_confirmed", "compulsory"]

    def set_card_cofirmed(self, which_card):
        self.STATE_REPRESENTATION["agent"][f"card_{which_card}"][1] = "confirmed"

    def set_card_value_confirmed(self, card_value, which_card):
        self.STATE_REPRESENTATION["agent"][f"card_{which_card}"] = [card_value,"confirmed", "compulsory"]

    def set_outcome_pair(self):
        self.STATE_REPRESENTATION["agent"]["task"] = "pair"
    
    def set_outcome_no_pair(self):
        self.STATE_REPRESENTATION["agent"]["task"] = "no_pair"
    
    def delete_state_representation(self):
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"card_{i+1}"] = [None, None, "compulsory"]
    # def set_both_cards_not_confirmed(self, card_values): -> probably unnecessary

    



    


