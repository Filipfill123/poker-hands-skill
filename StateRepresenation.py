
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
        slot_value = self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].get_slot_value_confidence_slot()[0]["value"]
        return slot_value
    

    def get_all_slots_value(self): 
        """
        For getting value of all slots
        
        Returns: array of values for all slots ([ace, king,...]) for slot_1 and slot_2,...
        """
        slots_value = list()
        for i in range(self.no_of_slates):
            slots_value.append(self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_confidence_slot())
        return slots_value


    def get_all_not_confirmed_slots(self):
        """
        For getting all uncofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_not_confirmed, slot_value],...] 
        """
        uncofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "not_confirmed":
                uncofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_confidence_slot()])
        return uncofirmed_slots

    def get_all_confirmed_slots(self):
        """
        For getting all cofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_confirmed, slot_value],...] 
        """
        cofirmed_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "confirmed":
                cofirmed_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_cofidence_slot()])
        return cofirmed_slots

    def get_all_inconsistent_slots(self):
        """
        For getting all inconsistent slots
        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_inconsistent, [[slot_value_1, confidence_score_1], [slot_value_2, confidence_score_2]]],...] 
        """
        inconsistent_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_state_slot() == "inconsistent":
                inconsistent_slots.append([i+1, self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_confidence_slot()])
        return inconsistent_slots


    def get_all_empty_slots(self):
        """
        For getting all empty slots

        Returns: array of number of empty slots [1, 4, 7,...]
        """
        empty_slots = list()
        for i in range(len(self.STATE_REPRESENTATION["agent"])):
            if self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].get_slot_value_confidence_slot()["value"] is None:
                empty_slots.append(i+1)
        return empty_slots


    def set_slot_value_confidence(self, slot_value, slot_confidence, which_slot):
        """
        For setting an unconfirmed value to a slot
        Args: value to set, number of slot
        
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_value_confidence_slot(slot_value, slot_confidence)

    def set_slot_not_cofirmed(self, which_slot):
        """
        For setting a slot to an unconfirmed state

        Args: which slot to confirm
        """
        self.STATE_REPRESENTATION["agent"][f"slot_{which_slot}"].set_slot_state_slot("not_confirmed")

    def set_slot_confirmed(self, which_slot):
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
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].set_slot_value_confidence_slot(None, None)
            self.STATE_REPRESENTATION["agent"][f"slot_{i+1}"].set_slot_state_slot(None)


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
        self.slot_state = None
        self.slot_value_confidence = []

    def set_slot_value_confidence_slot(self, slot_value, slot_confidence):
        if slot_value is None:
            pass
        else:
            if not self.get_slot_value_confidence_slot():
                self.slot_value_confidence = [{"value": slot_value, "confidence_score": slot_confidence}]
                self.slot_state = "not_confirmed"
            else:
                self.slot_value_confidence.append({"value": slot_value, "confidence_score": slot_confidence})
                self.slot_value_confidence.sort(key=lambda x: x["confidence_score"], reverse=True)
                self.slot_state = "inconsistent"

    def set_slot_state_slot(self, slot_state):
        self.slot_state = slot_state

    def get_all_slot_values(self):
        return {"slot_name": self.name, "slot_value_confidence": self.slot_value_confidence, "slot_state": self.slot_state}

    def get_slot_name_slot(self):
        return self.name

    def get_slot_value_confidence_slot(self):
        return self.slot_value_confidence

    def get_slot_state_slot(self):
        return self.slot_state

            

if __name__ == "__main__":

    skill_name = "poker_hands"
    no_of_slates = 2 # 2 cards
    STATE_REPRESENTATION = StateRepresentation(skill_name, no_of_slates)

    STATE_REPRESENTATION.set_slot_value_confidence("test_2", 0.6, 1)
    print(STATE_REPRESENTATION.get_slot_value(1))
    print(STATE_REPRESENTATION.get_all_not_confirmed_slots())
    STATE_REPRESENTATION.set_slot_value_confidence("test", 1, 1)
    print(STATE_REPRESENTATION.get_all_inconsistent_slots())
    print(STATE_REPRESENTATION.get_all_slots_value())
    STATE_REPRESENTATION.delete_state_representation()
    print(STATE_REPRESENTATION.get_all_slots_value())


