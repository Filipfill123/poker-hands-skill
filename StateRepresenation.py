
class StateRepresentation:
    def __init__(self, skill_name, no_of_slates, is_confidence_score):
        """
        Initialization of STATE REPRESENTATION

        Args: user's intent, number of slates (probably should be dynamic somehow), true if using confidence score/false if no confidence score
        """
        state_representation = {'user': skill_name,'agent': {},'task': "in_progress"}
        if is_confidence_score:
            for i in range(no_of_slates):
                state_representation["agent"][f"slot_{i+1}"] = [[[None, None]],None] # [[[ace,0.9],[king,0.2],...], "not_confirmed"]
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
        For getting value of a specific slot = to be used if there are no inconsistencies, thus no confidence score

        Args: number of slot to get
        
        Returns: value of a specific slot
        """
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0]
        return slot_value
    

    def get_all_slots_value(self): 
        """
        For getting value of all slots = to be used if there are no inconsistencies, thus no confidence score
        
        Returns: array of values for all slots ([ace, king,...]) for slot_1 and slot_2,...
        """
        slots_value = list()
        for i in range(self.no_of_slates):
            slots_value.append(self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0])
        return slots_value


    def get_all_not_confirmed_slots(self):
        """
        For getting all uncofirmed slots = to be used if there are no inconsistencies, thus no confidence score

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_not_confirmed, slot_value],...] 
        """
        uncofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][1] == "not_confirmed":
                uncofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0]])
        return uncofirmed_slots

    def get_all_confirmed_slots(self):
        """
        For getting all cofirmed slots = to be used if there are no inconsistencies, thus no confidence score

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_confirmed, slot_value],...] 
        """
        cofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][1] == "confirmed":
                cofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0]])
        return cofirmed_slots


    def get_all_empty_slots(self):
        """
        For getting all empty slots = to be used if there are no inconsistencies, thus no confidence score

        Returns: array of number of empty slots [1, 4, 7,...]
        """
        empty_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0] is None:
                empty_slots.append(i+1)
        return empty_slots


    def set_slot_value_not_cofirmed(self, slot_value, which_slot):
        """
        For setting an unconfirmed value to a slot = to be used if there are no inconsistencies, thus no confidence score

        Args: value to set, number of slot
        
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"] = [slot_value,"not_confirmed"]


    def set_slot_cofirmed(self, which_slot):
        """
        For "switching"/setting a slot to a confirmed state  = to be used if there are no inconsistencies, thus no confidence score

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] = "confirmed"
    

    def delete_state_representation(self):
        """
        Deletes the whole state representation - primarely for debugging purposes
        """
        self.STATE_REPRESENTATION["user"] = None
        self.STATE_REPRESENTATION["task"] = None
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"] = [None, None]


    def delete_agent_representation(self):
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
        For getting value of a specific slot and its confidence score = to be used if there are inconsistencies, thus with confidence score

        Args: number of slot to get
        
        Returns: value of a specific slot
        """
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0][0][0]
        return slot_value


    def get_all_slot_values(self, which_slot):
        """
        For getting all values of one slot and their confidence scores = to be used if there are inconsistencies, thus with confidence score

        Args: number of slot to get

        Returns: array of arrays [[ace,0.9],[king,0.3],[two,0.05]] = [[value_1, confidence_score_1],[value_2, confidence_score_2],...]

        """
        slot_values = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0]
        return slot_values


    def get_all_not_confirmed_slots_with_confidence(self):
        """
        For getting all uncofirmed slots = to be used if there are inconsistencies, thus with confidence score

        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_not_confirmed, [slot_value, confidence_score]],...] 
        """
        uncofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][1] == "not_confirmed":
                uncofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0][0]])
        return uncofirmed_slots

    def get_all_confirmed_slots_with_confidence(self):
        """
        For getting all cofirmed slots = to be used if there are inconsistencies, thus with confidence score

        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_confirmed, [slot_value, confidence_score]],...] 
        """
        cofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][1] == "confirmed":
                cofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0][0]])
        return cofirmed_slots

    def get_all_inconsistent_slots_with_confidence(self):
        """
        For getting all inconsistent slots = to be used if there are inconsistencies, thus with confidence score

        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_inconsistent, [[slot_value_1, confidence_score_1], [slot_value_2, confidence_score_2]]],...] 
        """
        inconsistent_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][1] == "inconsistent":
                inconsistent_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0]])
        return inconsistent_slots


    def get_all_empty_slots_with_confidence(self):
        """
        For getting all empty slots = to be used if there are inconsistencies, thus with confidence score

        Returns: array of number of empty slots [1, 5, 7,...]
        """
        empty_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"][0][0][0] is None:
                empty_slots.append(i+1)
        return empty_slots

    def set_slot_value_not_cofirmed_with_confidence(self, slot_value, confidence_score, which_slot):
        """
        For setting an unconfirmed value and its confidence to a slot = to be used if there are inconsistencies, thus with confidence score
        Also appends a new value and its confidence to a slot, sorts the whole slot from most confident to least and sets slot as "inconsistent"

        Args: value, confidence score, number of slot  
        
        """
        if self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0][0][0] is None and self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] is None:
            self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"] = [[[slot_value,confidence_score]],"not_confirmed"]

        else:
            self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0].append([slot_value, confidence_score])
            self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][0].sort(key=lambda x: x[1], reverse=True)
            self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] = "inconsistent"


    def set_slot_cofirmed_with_confidence(self, which_slot): # function without confidence could also be used
        """
        For "switching"/setting a slot to a confirmed state  = to be used if there are inconsistencies, thus with confidence score

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"][1] = "confirmed"
    

    def delete_agent_representation_with_confidence(self):
        """
        Deletes all of agent's memory - primarely for debugging purposes
        """
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"] = [[[None, None]], None]

    def delete_state_representation_with_confidence(self):
        """
        Deletes the whole state representation - primarely for debugging purposes
        """
        self.STATE_REPRESENTATION["user"] = None
        self.STATE_REPRESENTATION["task"] = None
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"] = [[[None, None]], None]


    """
    Part 3) confidence score does not matter
    """
    def get_task_state(self):
        """
        For getting state of task

        Returns: (str) state of task
        """
        task_state = self.STATE_REPRESENTATION["task"]

        return task_state


    def get_user_state(self):
        """
        For getting state of user

        Returns: (str) state of user
        """
        user_state = self.STATE_REPRESENTATION["user"]
        
        return user_state


    def set_task_state(self, task_state):
        """
        For setting a task state

        Args: the task state to be set
        """
        self.STATE_REPRESENTATION["task"] = task_state


    def set_user_state(self, user_state):
        """
        For setting a user state

        Args: the user state to be set
        """
        self.STATE_REPRESENTATION["user"] = user_state


if __name__ == "__main__":
    state_repres = StateRepresentation("test", 3, True)
    state_repres.set_slot_value_not_cofirmed_with_confidence("karta",0.8, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("prdel",0.2, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("kundibad",20, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("karta",0.8, 3)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("prdel",0.2, 3)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("kundibad",20, 3)
    print(state_repres.get_all_not_confirmed_slots_with_confidence())

    

    



    


