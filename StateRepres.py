import unittest
from pyrsistent import pvector, v, pmap, m
from dataclasses import dataclass, field

"""
Code
"""
class Slot:
    
    def __init__(self, name):
       self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
       self.__value = None
       self.__state = None
       self.__name = name
       self.first_value = None

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
            self.first_value = self.__value[0].value_confidence['value']
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
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def value_at_index(self, index):
        all_values = self.all_values
        
        return all_values[index]

    def is_valid(self, value):
        if value in self.cards:
            return True
        else:
            return False

class Value:

    def __init__(self, value='placeholder_value', confidence=1.0, state='placeholder_state'):
        self.value_confidence = m(value=value, confidence=confidence)
        self.state = state

class State:

    def __init__(self):
        self.__user = None
        self.__task = None
        # self.__agent = v()
        self.__agent = list()
        self.__History = History()
        # self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)
        self.__StateRepresentation = {"user":self.__user, "agent":self.__agent, "task":self.__task, "history": self.__History}
        

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
            slot = Slot(name)
            slot.value = value_in
            self.__dict__[name] = slot
            self.__agent = self.__agent.append(slot)
        
        #if self.__StateRepresentation is not None:
            #self.__StateRepresentation = self.__StateRepresentation.append(name)  
       
    def __delattr__(self, name):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        del self.__dict__[name]
        for slot in self.__agent:
            if slot.name == name:
                self.__agent = self.__agent.delete(self.__agent.index(slot))

        self.__StateRepresentation['agent'] = self.__agent


    @property
    def user(self):
        return self.User

    @user.setter
    def user(self, value):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        self.__user = Slot('user')
        self.__user.value = Value(state=value)
        self.__StateRepresentation = self.__StateRepresentation.set('user', self.__user)

    @property
    def task(self):
        return self.Task

    @task.setter
    def task(self, value):
        self.__History.history = self.__History.history.append(self.__StateRepresentation)
        self.__task = Slot('task')
        self.__task.value = Value(state=value)
        self.__StateRepresentation = self.__StateRepresentation.set('task', self.__task)

    @property
    def state_representation(self):
        return self.__StateRepresentation

    @property
    def agent(self):
        return self.__agent

    @property
    def history(self):
        return self.__History.history

    
    @property
    def all_unconfirmed_slots(self):
        all_unconfirmed_slots = list()
        for slot in self.__agent:
            if slot.state == 'unconfirmed':
                all_unconfirmed_slots.append(slot.name)
        return all_unconfirmed_slots

    @property
    def all_confirmed_slots(self):
        all_confirmed_slots = list()
        for slot in self.__agent:
            if slot.state == 'confirmed':
                all_confirmed_slots.append(slot.name)
        return all_confirmed_slots


    @property
    def all_inconsistent_slots(self):
        all_inconsistent_slots = list()
        for slot in self.__agent:
            if slot.state == 'inconsistent':
                all_inconsistent_slots.append(slot.name)
        return all_inconsistent_slots


    
    def delete_state_representation(self):
        self.__History = self.__History.history.append(self.__StateRepresentation)

        self.__user = None
        self.__task = None
        self.__agent = v()
        self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)
         
class History:

    def __init__(self):
        self.history = v()

@dataclass
class ValueTest:
    value: str
    confidence: float = 1.0
    value_confidence: float = field(init=False)

    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)

if __name__ == "__main__":
    
    test_state = State()
    test_state.first_card = Value('ace')
    print(test_state.history[1]['agent'][0].first_value)
    
    

    
