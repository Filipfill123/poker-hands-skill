import unittest
from pyrsistent import pvector, v, pmap, m
from dataclasses import dataclass, field

"""
Code
"""
class Slot:
    
    def __init__(self):
       self.__allowed_values = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
       self.__value = None
       self.__state = None
       self.__first_value = None

    @property
    def value(self):
        if self.__value is not None:
            return self.__value[0].value_confidence['value']
        else:
            return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value.value_confidence['value']):
            if self.__value is None:
                self.__value = [value]
                self.__state = 'unconfirmed'
            else:
                self.__value.append(value)
                self.__value.sort(key=lambda x: x.value_confidence['confidence'], reverse=True)
                self.__state = 'inconsistent'
            self.__first_value = self.__value[0].value_confidence['value']
        else:
            print("Value not valid!")

    @property
    def all_values(self):
        all_values = list()
        if self.__value is not None:
            for i in range(len(self.__value)):
                all_values.append(self.__value[i].value_confidence['value'])
        else:
            return self.__value
        return all_values

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def first_value(self):
        return self.__first_value

    def value_at_index(self, index):
        all_values = self.all_values
        
        return all_values[index]

    def solve_inconsistency(self, chosen_value):
        for i in range(len(self.__value)):
            if self.__value[i].value != chosen_value:
                self.__value.pop(i)
        self.__state = 'unconfirmed'

    def is_valid(self, value):
        if value in self.__allowed_values:
            return True
        else:
            return False


class State:

    def __init__(self):

        self.__History = History()
        # self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)
        self.__StateRepresentation = {"history": self.__History}
        

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)
        
    def __setattr__(self, name, value_in):
        if self.__History is not None:
            self.__History.history = self.__History.history.append(self.__StateRepresentation)
        if name.startswith('_State'):
            self.__dict__[name] = value_in
        else:
            try:
                self.__dict__[name]
                self.__dict__[name].value = value_in
            except KeyError:
                slot = Slot()
                slot.value = value_in
                self.__dict__[name] = slot
        
        #if self.__StateRepresentation is not None:
            #self.__StateRepresentation = self.__StateRepresentation.append(name)  
       
    def __delattr__(self, name):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        del self.__dict__[name]
                
        #self.__StateRepresentation = self.__agent TODO


    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        self.__user = Slot()
        self.__user.value = Value(state=value)
        #self.__StateRepresentation = self.__StateRepresentation.set('user', self.__user) TODO

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, value):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        self.__task = Slot()
        self.__task.value = Value(state=value)
        #self.__StateRepresentation = self.__StateRepresentation.set('task', self.__task)

    @property
    def state_representation(self):
        return self.__StateRepresentation

    @property
    def history(self):
        return self.__History.history

    
    @property
    def confirmed_slots(self):
        confirmed_slots = dict()
        for attribute, value in self.__dict__.items():
            if not attribute.startswith('_State'):
                if self.__dict__[attribute].state == 'confirmed' :
                    confirmed_slots[attribute] = value
        return confirmed_slots

    @property
    def unconfirmed_slots(self):
        unconfirmed_slots = dict()
        for attribute, value in self.__dict__.items():
            if not attribute.startswith('_State'):
                if self.__dict__[attribute].state == 'unconfirmed' :
                    unconfirmed_slots[attribute] = value
        return unconfirmed_slots

    @property
    def inconsistent_slots(self):
        inconsistent_slots = dict()
        for attribute, value in self.__dict__.items():
            if not attribute.startswith('_State'):
                if self.__dict__[attribute].state == 'inconsistent' :
                    inconsistent_slots[attribute] = value
        return inconsistent_slots


    def delete_state_representation(self):
        self.__History = self.__History.history.append(self.__StateRepresentation)

        # self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)

    def push(self, **kwargs):
        for key, value_in in kwargs.items():

            slot = Slot()

            if isinstance(value_in, (list, tuple)):
                if len(value_in) > 1:
                    for value_in_in in value_in:
                        if isinstance(value_in_in, Value):
                            slot.value = value_in_in
                        else:
                            slot.value = Value(value_in_in)
                else:
                    if isinstance(value_in[0], Value):
                        slot.value = value_in[0]
                    else:
                        slot.value = Value(value_in[0])
            else:
                if isinstance(value_in, Value):
                    slot.value = value_in
                else:
                    slot.value = Value(value_in)

            self.__dict__[key] = slot

class History:

    def __init__(self):
        self.history = v()

@dataclass
class Value:
    value: str
    confidence: float = 1.0
    value_confidence: float = field(init=False)

    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)

if __name__ == "__main__":
    
    test_state = State()
    #first_card = Slot()
    #print(test_state.first_card.value)
    
    test_state.push(slot_1=("ace", "king", ""))
    print(test_state.slot_1.all_values)
    # test_state.push(slot_1=Value("ace", confidence=0.9), slot_2=Value("king", confidence=0.05))
    # state.push(slot="king", confidence=0.05)
    # state.push(slot_1="ace", slot_2="king", confidence=0.05)
    # state.push(slot_1=["ace", "king"])
    

    
