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
    def __init__(self, skill_name, no_of_slates, is_confidence_score):
        """
        Initialization of STATE REPRESENTATION

        Args: user's intent, number of slates (probably should be dynamic somehow), true if using confidence score/false if no confidence score
        """
        state_representation = {'user': skill_name,'agent': {},'task': "in_progress"}
        if is_confidence_score:
            for i in range(no_of_slates):
                state_representation["agent"][f"slot_{i+1}"] = [[None, None],None] # [[ace,0.9], "not_confirmed"]
        else:
            for i in range(no_of_slates):
                state_representation["agent"][f"slot_{i+1}"] = [None,None] # [ace, "not_confirmed"]
        
        self.no_of_slates = no_of_slates
        self.STATE_REPRESENTATION = state_representation # INITIALIZATION


    """
    Part 1) no confidence score
    """
    def get_slot_value(self, which_slot):
        """
        For getting value of a specific slot = to be used if there are no unconsistencies, thus no confidence score

        Args: number of slot to get
        
        Returns: value of a specific slot
        """
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0]
        return slot_value
    

    def get_all_slots_value(self): 
        """
        For getting value of all slots = to be used if there are no unconsistencies, thus no confidence score
        
        Returns: array of values for all slots ([ace, king]) 
        """
        slots_value = list()
        for i in range(self.no_of_slates):
            slots_value.append(self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0])
        return slots_value


    def set_slot_value_not_cofirmed(self, slot_value, which_slot):
        """
        For setting an unconfirmed value to a slot = to be used if there are no unconsistencies, thus no confidence score

        Args: value to set, number of slot
        
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"] = [slot_value,"not_confirmed"]


    def set_slot_cofirmed(self, which_slot):
        """
        For "switching"/setting a slot to a confirmed state  = to be used if there are no unconsistencies, thus no confidence score

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] = "confirmed"
    
    def delete_state_representation(self):
        """
        Deletes all of agent's memory - primarely for debugging purposes
        """
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"] = [None, None]


    """
    Part 2) with confidence score
    """

    def get_slot_value_with_confidence(self, which_slot):
        """
        For getting value of a specific slot and its confidence score = to be used if there are unconsistencies, thus with confidence score

        Args: number of slot to get
        
        Returns: value of a specific slot and its confidence
        """
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0]
        return slot_value

    def get_all_slot_values(self, which_slot):
        """
        For getting all values of one slot and their confidence scores = to be used if there are unconsistencies, thus with confidence score

        Args: number of slot to get

        Returns: array of arrays [[ace,0.9],[king,0.3],[two,0.05]] = [[value_1, confidence_score_1],[value_2, confidence_score_2],...]

        """
        slot_values = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0])):
            slot_values.append(self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0][i])
        return slot_values

    def set_slot_value_not_cofirmed_with_confidence(self, slot_value, confidence_score, which_slot):
        """
        For setting an unconfirmed value and its confidence to a slot = to be used if there are unconsistencies, thus with confidence score

        Args: value, confidence score, number of slot  
        
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"] = [[slot_value,confidence_score],"not_confirmed"]


    def set_slot_cofirmed_with_confidence(self, which_slot): # function without confidence could also be used
        """
        For "switching"/setting a slot to a confirmed state  = to be used if there are unconsistencies, thus with confidence score

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] = "confirmed"
    
    def delete_state_representation_with_confidence(self):
        """
        Deletes all of agent's memory - primarely for debugging purposes
        """
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"] = [[None, None], None]


    """
    Part 3) confidence score does not matter
    """
    def get_task_state(self):
        """
        For getting state of task

        Returns: state of task
        """
        task_state = self.STATE_REPRESENTATION["task"]

        return task_state

    def get_user_state(self):
        """
        For getting state of user

        Returns: state of user
        """
        user_state = self.STATE_REPRESENTATION["user"]
        
        return user_state

    def set_user_state(self, user_state):
        """
        For setting a user state

        Args: the user state to be set
        """
        self.STATE_REPRESENTATION["user"] = user_state

    def set_task_state(self, task_state):
        """
        For setting a task state

        Args: the task state to be set
        """
        self.STATE_REPRESENTATION["task"] = task_state

    

    



    


