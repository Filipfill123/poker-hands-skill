import unittest
import datetime
from pyrsistent import pvector, v, pmap, m
from dataclasses import dataclass, field

"""
Code
"""
class Slot:
    
    def __init__(self):
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
        if value.valid:
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

    def solve_inconsistency(self, chosen_value): # assign - pokud chtena valu recena, pokracuj dal; jinak udelej klasickej push
        for i in range(len(self.__value)):
            if self.__value[i].value != chosen_value:
                self.__value.pop(i)
        self.__state = 'unconfirmed'


class State:

    def __init__(self):

        self.__History = v()
        # self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)
        self.__StateRepresentation = {"history": self.__History}
        

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)
        
    def __setattr__(self, name, value_in):
        # if self.__History is not None:
        #     self.__History = self.__History.append(self.__StateRepresentation)
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
        # self.__History = self.__History.append(self.__StateRepresentation)
        del self.__dict__[name]
                
        #self.__StateRepresentation = self.__agent TODO


    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        # self.__History = self.__History.append(self.__StateRepresentation)
        self.__user = Slot()
        self.__user.value = Value(state=value)
        #self.__StateRepresentation = self.__StateRepresentation.set('user', self.__user) TODO

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, value):
        # self.__History = self.__History.append(self.__StateRepresentation)
        self.__task = Slot()
        self.__task.value = Value(state=value)
        #self.__StateRepresentation = self.__StateRepresentation.set('task', self.__task)

    @property
    def state_representation(self):
        return self.__StateRepresentation

    @property
    def history(self):
        return self.__History

    
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


    # def delete_state_representation(self):
        # self.__History = self.__History.append(self.__StateRepresentation)

        # self.__StateRepresentation = m(user=self.__user, agent=self.__agent, task=self.__task, history=self.__History)
    def new_slots(self, **kwargs):
        for slot_name, value_class in kwargs.items():
            self.__dict__[slot_name + '_value_class'] = value_class


    def push(self, **kwargs):
        for key, value_in in kwargs.items():

            slot = Slot()

            if isinstance(value_in, (list, tuple)):
                if len(value_in) > 1:
                    for value_in_in in value_in:
                        if isinstance(value_in_in, Value):
                            slot.value = value_in_in
                        else:
                            slot.value = self.__dict__[key + '_value_class'](value_in_in)
                else:
                    if isinstance(value_in[0], Value):
                        slot.value = value_in[0]
                    else:
                        slot.value = self.__dict__[key + '_value_class'](value_in[0])
            else:
                if isinstance(value_in, Value):
                    slot.value = value_in
                else:
                    slot.value = self.__dict__[key + '_value_class'](value_in)

            self.__dict__[key] = slot

    def expect(self, idx, **kwargs):
        if idx == "DISAMBIG":
            self.disambig(kwargs)
        elif idx == "PRESENT":
            self.present(kwargs)

    def disambig(self, slots): ### pro vyreseni problemu + dobre na tracking stavu dialogu (uvidim prubeh)
        for key, value in slots.items():
            print(value, '=>', key)

    def present(self, slots):
        for key, value in slots.items():
            print(key, '=>', value)


@dataclass
class Value:
    value: str = None
    confidence: float = 1.0
    value_confidence: float = field(init=False)

    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)

@dataclass
class Cards(Value):
    valid: bool = None

    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)
        cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
        if self.value in cards: 
            self.valid = True
        else:
            self.valid = False
            # raise(ValueError)
@dataclass
class TimeValue(Value):
    valid: bool = None
    
    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)
        hours, minutes, *seconds = self.value.split(":")
        if seconds:
            seconds = seconds[0]
        else:
            seconds = "00"
        self.valid = True
        try:
            datetime.time(hour=int(hours), minute=int(minutes), second=int(seconds))
        except ValueError:
            self.valid = False

@dataclass
class Station(Value):
    valid: bool = None

    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)
        stations = ('praha_hlavni_nadrazi','plzen_hlavni_nadrazi','brno_hlavni_nadrazi','praha_smichov','ostrava_hlavni_nadrazi','ceske_budejovice_hlavni_nadrazi')
        if self.value in stations: 
            self.valid = True
        else:
            self.valid = False

@dataclass
class TraintypeEnum(Value):
    valid: bool = None
    def __post_init__(self):
        self.value_confidence = m(value=self.value, confidence=self.confidence)
        train_types = ('R','O','any')
        if self.value in train_types: 
            self.valid = True
        else:
            self.valid = False


if __name__ == "__main__":
    
    #first_card = Slot()
    #print(test_state.first_card.value)
    
    state = State()

    state.new_slots(to_station=Station, from_station=Station, time=TimeValue, train_type=TraintypeEnum)
    state.push(to_station=('prdelakov'))
    print(state.to_station.value)
    # state.act("DISAMBIG", slot_1=('ace','king'), slot_2=Value('two'))
    # test_state.push(slot_1=Value("ace", confidence=0.9), slot_2=Value("king", confidence=0.05))
    # state.push(slot="king", confidence=0.05)
    # state.push(slot_1="ace", slot_2="king", confidence=0.05)
    # state.push(slot_1=["ace", "king"])