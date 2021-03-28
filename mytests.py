import unittest
from pyrsistent import pvector, v, pmap, m
from dataclasses import dataclass, field

"""
Code
"""
class Slot:
    
    def __init__(self):
       self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
       self.__value = None
       self.__state = None
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
    #     self.Agent = Slot()
    #     self.User = Slot()
    #     self.Task = Slot()
        # self.StateRepresentation = v()
        self.History = History()


    def __getattribute__(self, name):
        #print(self.__dict__[name])
        return super().__getattribute__(name)
        
        #return self.__dict__[name].first_value

    def __getattr__(self, name):
        return super().__setattr__(name, None)
        
    def __setattr__(self, name, value):
        if (getattr(self, name, None)) is None:
            self.__dict__[name] = value
        else:
            #self.History.history = self.History.history.append(self.__dict__[name])
            self.__dict__[name] = value
                 
    def __delattr__(self, name):
       # self.History.history = self.History.history.append(self.__dict__[name])
        del self.__dict__[name]

    def delete_state_representation(self):
        for attribute in self.__dict__.items():
            
            self.__dict__[attribute] = None
    
        #self.History.history = self.History.history.append(self.__dict__[name])

    @property
    def all_unconfirmed_slots(self):
        all_unconfirmed_slots = list()
        for attribute, value in self.__dict__.items():
            if attribute != 'History':
                if self.__dict__[attribute].state == 'unconfirmed' :
                    all_unconfirmed_slots.append(attribute)
        return all_unconfirmed_slots

    @property
    def all_confirmed_slots(self):
        all_confirmed_slots = list()
        for attribute, value in self.__dict__.items():
            if attribute != 'History':
                if self.__dict__[attribute].state == 'confirmed' :
                    all_confirmed_slots.append(attribute)
        return all_confirmed_slots

    @property
    def all_inconsistent_slots(self):
        all_inconsistent_slots = list()
        for attribute, value in self.__dict__.items():
            if attribute != 'History':
                if self.__dict__[attribute].state == 'inconsistent' :
                    all_inconsistent_slots.append(attribute)
        return all_inconsistent_slots
         
class History:

    def __init__(self):
        self.history = v()

@dataclass
class ValueTest:
    value: str
    confidence: float = 1.0
    value_confidence: float = field(init=False)

    def __post_init__(self):
        if self.confidence < 0.0 or self.confidence > 1.0:
            self.confidence = 1.0
        self.value_confidence = m(value=self.value, confidence=self.confidence)
        


class Tests():

    def first_value(self):
        state = State()
        state.slot = Slot()
        state.slot.value = Value(value="king",confidence=0.05)
        state.slot.value = Value(value="ace",confidence=0.9)
        return state.slot.first_value

    def all_unconfirmed_slots(self):
        state = State()
        state.slot_1 = Slot()
        state.slot_2 = Slot()
        state.slot_3 = Slot()
        state.slot_1.value = Value('ace',0.9)
        state.slot_2.value = Value('king')
        state.slot_3.value = Value("two")
        state.slot_3.state = 'confirmed'
        return state.all_unconfirmed_slots

    def all_confirmed_slots(self):
        state = State()
        state.slot_1 = Slot()
        state.slot_2 = Slot()
        state.slot_3 = Slot()

        state.slot_1.value = Value('ace',0.9)

        state.slot_2.value = Value('king')

        state.slot_3.value = Value("two")

        state.slot_1.state = 'confirmed'
        state.slot_3.state = 'confirmed'

        return state.all_confirmed_slots

    def all_inconsistent_slots(self):
        state = State()
        state.slot_1 = Slot()
        state.slot_2 = Slot()
        state.slot_3 = Slot()

        state.slot_1.value = Value('ace',0.9)

        state.slot_2.value = Value('king',0.9)
        state.slot_2.value = Value('three',0.02)

        state.slot_3.value = Value("two", 0.8)
        state.slot_3.value = Value("seven", 0.1)

        return state.all_inconsistent_slots

class MyFirstTests(unittest.TestCase):
    """
    Tests
    """
        
    
    def test_first_value(self):
        tests = Tests()
        self.assertEqual(tests.first_value(), "ace", "Should be ace")

    def test_unconfirmed(self):
        tests = Tests()
        self.assertEqual(tests.all_unconfirmed_slots(), ['slot_1', 'slot_2'])

    def test_confirmed(self):
        tests = Tests()
        self.assertEqual(tests.all_confirmed_slots(), ['slot_1', 'slot_3'])

    def test_inconsistent(self):
        tests = Tests()
        self.assertEqual(tests.all_inconsistent_slots(), ['slot_2', 'slot_3'])


if __name__ == '__main__':
    unittest.main()
    
