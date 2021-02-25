
class StateRepresentation:
    def __init__(self, skill_name, no_of_slates):
        """
        Initialization of STATE REPRESENTATION

        Args: user's intent, number of slates (probably should be dynamic somehow)
        """
        state_representation = {'user': UserSlot(),'agent': {},'task': TaskSlot()}
        for i in range(no_of_slates):
            state_representation["agent"][f"slot_{i+1}"] = AgentSlot(f"slot_{i+1}")
        
        self.no_of_slates = no_of_slates
        self.STATE_REPRESENTATION = state_representation # INITIALIZATION


    def get_slot_value(self, which_slot):
        """
        For getting value of a specific slot

        Args: number of slot to get
        
        Returns: value of a specific slot
        """
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].get_slot_value_slot()
        return slot_value
    

    def get_all_slots_value(self): 
        """
        For getting value of all slots
        
        Returns: array of values for all slots ([ace, king,...]) for slot_1 and slot_2,...
        """
        slots_value = list()
        for i in range(self.no_of_slates):
            slots_value.append(self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_slot())
        return slots_value


    def get_all_not_confirmed_slots(self):
        """
        For getting all uncofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_not_confirmed, slot_value],...] 
        """
        uncofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "not_confirmed":
                uncofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_slot()])
        return uncofirmed_slots

    def get_all_confirmed_slots(self):
        """
        For getting all cofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_confirmed, slot_value],...] 
        """
        cofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "confirmed":
                cofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_slot()])
        return cofirmed_slots

    def get_all_inconsistent_slots(self):
        """
        For getting all inconsistent slots
        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_inconsistent, [[slot_value_1, confidence_score_1], [slot_value_2, confidence_score_2]]],...] 
        """
        inconsistent_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "inconsistent":
                inconsistent_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_slot()])
        return inconsistent_slots


    def get_all_empty_slots(self):
        """
        For getting all empty slots

        Returns: array of number of empty slots [1, 4, 7,...]
        """
        empty_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_slot() is None:
                empty_slots.append(i+1)
        return empty_slots


    def set_slot_value(self, slot_value, which_slot):
        """
        For setting an unconfirmed value to a slot
        Args: value to set, number of slot
        
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_value_slot(slot_value)
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_state_slot("not_confirmed")

    def set_slot_not_cofirmed(self, which_slot):
        """
        For setting a slot to an unconfirmed state

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_state_slot("not_confirmed")

    def set_slot_cofirmed(self, which_slot):
        """
        For setting a slot to a confirmed state

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_state_slot("confirmed")

    def set_slot_inconsistent(self, which_slot):
        """
        For setting a slot to an inconsistent state

        Args: which slot to inconsist
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_state_slot("inconsistent")
    

    def delete_state_representation(self):
        """
        Deletes the whole state representation - primarely for debugging purposes
        """
        self.STATE_REPRESENTATION["user"].set_user_state_slot(None)
        self.STATE_REPRESENTATION["task"].set_task_state_slot(None)
        for i in range(self.no_of_slates):
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].set_all_slot_values_slot(None, None, None)


    def get_task_state(self):
        """
        For getting state of task

        Returns: (str) state of task
        """
        task_state = self.STATE_REPRESENTATION["task"].get_task_state_slot()

        return task_state


    def get_user_state(self):
        """
        For getting state of user

        Returns: (str) state of user
        """
        user_state = self.STATE_REPRESENTATION["user"].get_user_state_slot()
        
        return user_state


    def set_task_state(self, task_state):
        """
        For setting a task state

        Args: the task state to be set
        """
        self.STATE_REPRESENTATION["task"].set_task_state_slot(task_state)


    def set_user_state(self, user_state):
        """
        For setting a user state

        Args: the user state to be set
        """
        self.STATE_REPRESENTATION["user"].set_user_state_slot(user_state)


class TaskSlot:
    def __init__(self):
        self.task_state = None

    def set_task_state_slot(self, task_state):
        self.task_state = task_state

    def get_task_state_slot(self):
        return self.task_state

class UserSlot:
    def __init__(self):
        self.user_state = None
    
    def set_user_state_slot(self, user_state):
        self.user_state = user_state

    def get_user_state_slot(self):
        return self.user_state

class AgentSlot:
    def __init__(self, name):
        self.name = name
        self.slot_value = None
        self.slot_confidence = None
        self.slot_state = None

    def set_all_slot_values_slot(self, slot_value, slot_confidence, slot_state):
        self.slot_value = slot_value
        self.slot_confidence = slot_confidence
        self.slot_state = slot_state

    def set_slot_value_slot(self, slot_value):
        self.slot_value = slot_value

    def set_slot_confidence_slot(self, slot_confidence):
        self.slot_confidence = slot_confidence

    def set_slot_state_slot(self, slot_state):
        self.slot_state = slot_state

    def get_all_slot_values(self):
        return {"slot_name": self.name, "slot_value": self.slot_value, "slot_confidence": self.slot_confidence, "slot_state": self.slot_state}

    def get_slot_value_slot(self):
        return self.slot_value

    def get_slot_confidence_slot(self):
        return self.slot_confidence

    def get_slot_state_slot(self):
        return self.slot_state

            

if __name__ == "__main__":
    state_repres = StateRepresentation("test", 3)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("karta",0.8, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("prdel",0.2, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("kundibad",20, 1)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("karta",0.8, 3)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("prdel",0.2, 3)
    #state_repres.set_slot_value_not_cofirmed_with_confidence("kundibad",20, 3)
    print(state_repres.get_task_state())
    # TaskSlot = TaskSlot()
    # print(TaskSlot.get_task_state_slot())

    

    



    


