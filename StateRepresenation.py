from pyrsistent import v, pvector
class StateRepresentation:
    
    def __init__(self):
        """
        Initialization of STATE REPRESENTATION
        TaskSlot for task's state
        UserSlot for user's state
        AgentSlots for agent's slots
        """
        
        self.TaskSlot = TaskSlot()
        self.UserSlot = UserSlot()
        self.AgentSlots = v()
        self.Memory = list()
        
    """
    Agent functions
    """
    def insert_agent_slot(self, name, slot_state, slot_value, slot_confidence):
        self.Memory.append(self.AgentSlots)
        self.AgentSlots = self.AgentSlots.append(AgentSlot(name, slot_state, slot_value, slot_confidence))

    def replace_agent_slot(self, which_slot, name, slot_state, slot_value, slot_confidence):
        self.Memory.append(self.AgentSlots)
        self.AgentSlots = self.AgentSlots.set(which_slot)

    def remove_agent_slot(self, which_slot):
        self.Memory.append(self.AgentSlots)
        self.AgentSlots = self.AgentSlots.delete(which_slot)

    def print_agent_names(self):
        names = []
        for i in range(len(self.AgentSlots)):
            names.append(self.AgentSlots[i].get_slot_name_slot())
        return names

    def get_slot_value(self, which_slot, index=0):
        """
        For getting value of a specific slot

        Args: number of slot to get
        
        Returns: value of a specific slot
        """
        slot_value = self.AgentSlots[which_slot].get_slot_value_slot(index)
        return slot_value
    
    def get_all_slot_values(self, which_slot):
        slot_values = list()
        for i in range(len(self.AgentSlots[which_slot].slot_value_confidence)):
            slot_values.append(self.AgentSlots[which_slot].get_slot_value_slot(i))
        return slot_values

    def get_all_slots_value(self): 
        """
        For getting value of all slots
        
        Returns: array of values for all slots ([ace, king,...]) for slot_1 and slot_2,...
        """
        slots_value = list()
        for i in range(len(self.AgentSlots)):
            slots_value.append(self.AgentSlots[i].get_slot_value_confidence_slot())
        return slots_value


    def get_all_not_confirmed_slots(self):
        """
        For getting all uncofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_not_confirmed, slot_value],...] 
        """
        uncofirmed_slots = list()
        for i in range(len(self.AgentSlots)):
            if self.AgentSlots[i].get_slot_state_slot() == "not_confirmed":
                uncofirmed_slots.append([i+1, self.AgentSlots[i].get_slot_value_confidence_slot()])
        return uncofirmed_slots

    def get_all_confirmed_slots(self):
        """
        For getting all cofirmed slots

        Returns: array of arrays [[1, "ace"], [4, "two"],...] = [[which_slot_is_confirmed, slot_value],...] 
        """
        cofirmed_slots = list()
        for i in range(len(self.AgentSlots)):
            if self.AgentSlots[i].get_slot_state_slot() == "confirmed":
                cofirmed_slots.append([i+1, self.AgentSlots[i].get_slot_value_cofidence_slot()])
        return cofirmed_slots

    def get_all_inconsistent_slots(self):
        """
        For getting all inconsistent slots
        Returns: array of arrays [[1, ["ace",0.9]], [4, ["two",0.87]],...] = [[which_slot_is_inconsistent, [[slot_value_1, confidence_score_1], [slot_value_2, confidence_score_2]]],...] 
        """
        inconsistent_slots = list()
        for i in range(len(self.AgentSlots)):
            if self.AgentSlots[i].get_slot_state_slot() == "inconsistent":
                inconsistent_slots.append([i+1, self.AgentSlots[i].get_slot_value_confidence_slot()])
        return inconsistent_slots


    def get_all_empty_slots(self):
        """
        For getting all empty slots

        Returns: array of number of empty slots [1, 4, 7,...]
        """
        empty_slots = list()
        for i in range(len(self.AgentSlots)):
            if self.AgentSlots[i].get_slot_value_confidence_slot()["value"] is None:
                empty_slots.append(i+1)
        return empty_slots


    def set_slot_value_confidence(self, which_slot, slot_value, slot_confidence):
        """
        For setting an unconfirmed value to a slot
        Args: value to set, number of slot
        
        """
        self.AgentSlots[which_slot].set_slot_value_confidence_slot(slot_value, slot_confidence)

    def set_slot_not_cofirmed(self, which_slot):
        """
        For setting a slot to an unconfirmed state

        Args: which slot to confirm
        """
        self.AgentSlots[which_slot].set_slot_state_slot("not_confirmed")

    def set_slot_confirmed(self, which_slot):
        """
        For setting a slot to a confirmed state

        Args: which slot to confirm
        """
        self.AgentSlots[which_slot].set_slot_state_slot("confirmed")

    def set_slot_inconsistent(self, which_slot):
        """
        For setting a slot to an inconsistent state

        Args: which slot to inconsist
        """
        self.AgentSlots[which_slot].set_slot_state_slot("inconsistent")
    
            
    """
    General functions
    """

    def get_task_state(self):
        """
        For getting state of task

        Returns: (str) state of task
        """
        task_state = self.TaskSlot.get_task_state_slot()

        return task_state


    def get_user_state(self):
        """
        For getting state of user

        Returns: (str) state of user
        """
        user_state = self.UserSlot.get_user_state_slot()
        
        return user_state


    def set_task_state(self, task_state):
        """
        For setting a task state

        Args: the task state to be set
        """
        self.TaskSlot.set_task_state_slot(task_state)


    def set_user_state(self, user_state):
        """
        For setting a user state

        Args: the user state to be set
        """
        self.UserSlot.set_user_state_slot(user_state)

    
    def delete_state_representation(self):
        """
        Deletes the whole state representation - primarely for debugging purposes
        """
        self.UserSlot.set_user_state_slot(None)
        self.TaskSlot.set_task_state_slot(None)
        self.AgentSlots = v()
            


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
    def __init__(self, name, slot_state, slot_value, slot_confidence):
        self.name = name
        self.slot_state = slot_state
        self.slot_value_confidence = [{"value": slot_value, "confidence_score": slot_confidence}]

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

    def get_slot_value_slot(self, index):
        return self.slot_value_confidence[index]["value"]

    def get_slot_value_confidence_slot(self):
        return self.slot_value_confidence

    def get_slot_state_slot(self):
        return self.slot_state

            

if __name__ == "__main__":

    STATE_REPRESENTATION = StateRepresentation()


    STATE_REPRESENTATION.insert_agent_slot("kundibad", "not_confirmed", "test", 0.0)
    STATE_REPRESENTATION.insert_agent_slot("dement", "not_confirmed", "test_2", 0.9)
    print(STATE_REPRESENTATION.AgentSlots)
    print(STATE_REPRESENTATION.Memory)
    STATE_REPRESENTATION.remove_agent_slot(0)
    print(STATE_REPRESENTATION.AgentSlots)
    print(STATE_REPRESENTATION.Memory)
    
    # seznam = list()
    # vector = v(1,2,3)
    # v1 = vector.delete(0)
    # print(v1)
    # seznam.append(vector)
    # seznam.append(v1)
    # print(seznam)