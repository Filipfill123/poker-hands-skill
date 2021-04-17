from dataclasses import dataclass, field
from pyrsistent import pvector, v, pmap, m


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
class Slot:
    
    def __init__(self):
       self.__value = None
       self.__state = None
       self.__first_value = None

    @property
    def value(self):
        # if self.__value is not None:
        #     return self.__value[0].value_confidence['value']
        # else:
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
            self.__last_value = self.__value[-1].value_confidence['value']
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
    def first_value(self):
        return self.__first_value

    @property
    def last_value(self):
        return self.__last_value

    def value_at_index(self, index):
        all_values = self.all_values
        
        return all_values[index]

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    
class State:
    def __init__(self):
        self.expectations = v()  
        self.slot_names = v()
        self.History = v()

    def push(self, **kwargs):
        
        expectations, self.expectations = self.expectations, v()  # TODO: Move into self.history()
        if len(expectations) != 0:
            self.History = self.History.append(expectations)
        for cb, slot_names in expectations:
            cbkwargs = {key: kwargs.get(key) for key in slot_names}

            # Call the expectation callback and pass myself as first argument
            handled = cb(self, **cbkwargs)
            if handled:
                # The arguments were handled by the callback
                for key in slot_names:
                    del kwargs[key]

        if kwargs:
            # Only change state if there is something to push
            self.extend(**kwargs)

    def extend(self, **kwargs):
        for key, value_in in kwargs.items():

            slot_name = key

            if isinstance(value_in, (list, tuple)):
                if len(value_in) > 1:
                    for value_in_in in value_in:
                        if isinstance(value_in_in, Value):
                            self.__dict__[slot_name].value = value_in_in
                            print("extended values_1:", key, '=',value_in_in)
                        else:
                            self.__dict__[slot_name].value = self.__dict__[key + '_value_class'](value_in_in)
                            print("extended values_2:", key, '=',value_in_in)
                else:
                    if isinstance(value_in[0], Value):
                        self.__dict__[slot_name].value = value_in[0]
                        print("extended values_3:", key, '=',value_in[0])
                    else:
                        self.__dict__[slot_name].value = self.__dict__[key + '_value_class'](value_in[0])
                        print("extended values_4:", key, '=',value_in[0])
            else:
                if isinstance(value_in, Value):
                    self.__dict__[slot_name].value = value_in
                    print("extended values_5:", key, '=',value_in)
                else:
                    self.__dict__[slot_name].value = self.__dict__[key + '_value_class'](value_in)
                    print("extended values_6:", key, '=',value_in)


    def assign(self, **kwargs):

        for key, value in kwargs.items():
            for i in range(len(self.__dict__[key].value)):
                self.__dict__[key].value.pop()
            if isinstance(value[0], Value):
                self.__dict__[key].value = value[0]
            else:
                self.__dict__[key].value = self.__dict__[key + '_value_class'](value[0])
            print("assigned values:", key, '=', value[0])

    def confirm_slots(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key].state = 'confirmed'

    def expect(self, cb, *args):
        slot_names = v()
        for slot_name in self.slot_names:  # iterate over slots
            for slot in args:
                if getattr(self, slot_name) is slot:
                    slot_names = slot_names.append(slot_name)
        self.expectations = self.expectations.append((cb, slot_names))

    @staticmethod
    def complete_empty(self, **kwargs):
        for slot_name in kwargs:
            print(f'Slot {slot_name} must be filled')
            #self.extend(**kwargs)
            

    @staticmethod
    def confirm_unconfirmed(self, **kwargs):
        for slot_name in kwargs:
            print(f'Slot {slot_name} must be confirmed')
            self.confirm_slots(**kwargs)

    @staticmethod
    def disambig(self, **kwargs):
        for key, value in kwargs.items():
            if value[0] not in self.__dict__[key].all_values:
                print(f'New value {value} was not accepted, it was not in proposed values {self.__dict__[key].all_values} of slot {key}')
                return False # the values were not assigned -> the slots were not handled
            else:
                print(f'New value {value} was accepted in slot {key}')
                self.assign(**kwargs)
                return True  # the slots were handled

    @staticmethod
    def present(self, **kwargs):
        for slot_name in kwargs:
            print("Value was presented", getattr(self, slot_name).first_value)

    

    @property
    def empty_slots(self):
        empty_slots = list()
        for attribute, value in self.__dict__.items():
            if isinstance(value, Slot):
                if self.__dict__[attribute].state is None:
                    empty_slots.append(value)
        empty_slots = tuple(empty_slots)
        return empty_slots

    @property
    def confirmed_slots(self):
        confirmed_slots = list()
        for attribute, value in self.__dict__.items():
            if isinstance(value, Slot):
                if self.__dict__[attribute].state == 'confirmed':
                    confirmed_slots.append(value)
        
        return confirmed_slots

    @property
    def unconfirmed_slots(self):
        unconfirmed_slots = list()
        for attribute, value in self.__dict__.items():
            if isinstance(value, Slot):
                if self.__dict__[attribute].state == 'unconfirmed':
                    unconfirmed_slots.append(value)
        return unconfirmed_slots

    @property
    def inconsistent_slots(self):
        inconsistent_slots = list()
        for attribute, value in self.__dict__.items():
            if isinstance(value, Slot):
                if self.__dict__[attribute].state == 'inconsistent':
                    inconsistent_slots.append(value)
        return inconsistent_slots
    
    def new_slots(self, **kwargs):
        for slot_name, value_class in kwargs.items():
            
            self.__dict__[slot_name + '_value_class'] = value_class
            self.__dict__[slot_name] = Slot()
            self.slot_names = self.slot_names.append(slot_name)
            print("new slot added: ", slot_name)
        self.History = self.History.append(self.slot_names)

    def delete_state_representation(self):
        for slot_name in self.slot_names:
            self.__dict__[slot_name] = Slot()

print("""

Example 10

""")
state = State()
state.new_slots(first_card=Cards, second_card=Cards)
state.push(first_card='ace')
state.expect(state.complete_empty, state.second_card)
state.push(first_card='king')
state.expect(state.disambig, state.first_card)

state.push(first_card=['king'])
# print("""

# Example 1

# """)

# s = State()
# s.new_slots(slot_1=Cards, slot_2=Cards, slot_3=Cards)

# # Turn 1
# #s.expect(s.complete_empty, s.slot_1, s.slot_2, s.slot_3)
# s.push(slot_1=["king", "ace"], slot_2=["two"])
# s.expect(s.complete_empty, s.slot_3)



# # Turn 2

# s.push(slot_3=["ace"])
# s.expect(s.disambig, s.slot_1)
# s.push(slot_1=["king"])
# s.expect(s.confirm_unconfirmed, s.slot_1, s.slot_2, s.slot_3)

# s.expect(s.present, s.slot_1, s.slot_2, s.slot_3)

# # Turn 3
# s.push()   # handle expectations even if there wasn't any input
# s.assign(slot_1=["seven"])
# print(s.slot_1.all_values)

# print(s.slot_names)
# print(s.slot_1.all_values, s.slot_2.all_values)

# print("""

# Example 2

# """)

# s = State()
# s.new_slots(slot_1=Cards)
# # Turn 1

# def my_disambig(state, slot_1):
#     if set(slot_1).issubset(state.slot_1):
#         # Accept the disambiguation, it was in the proposed values
#         print("Accepted! old value", state.slot_1, "new value", slot_1)
#         state.assign(slot_1=slot_1)
#         return True
#     else:
#         # Reject the disambiguation
#         print("Rejected! old value", state.slot_1, "new value", slot_1)
#         return False

# s.push(slot_1=["king", "ace"])
# s.expect(my_disambig, s.slot_1)

# # Turn 2

# s.push(slot_1=["queen"])
# s.expect(my_disambig, s.slot_1)

# # Turn 3
# s.push(slot_1=["queen"])   # handle expectations even if there wasn't any input
# s.expect(s.present, s.slot_1)

# # Turn 4
# s.push()



# print("""

# Example 3

# """)

# s = State()
# s.new_slots(slot_1=Cards)

# def say_king(state, slot_1):
#     if "king" in slot_1:
#         print("Good, you said king")
#         state.assign(slot_1=slot_1)
#         return True
#     else:
#         print("You have to say king, not", slot_1)
#         state.expect(say_king, state.slot_1)
#         return True

# # Initialization

# s.expect(say_king, s.slot_1)

# # Turn 1

# s.push(slot_1=["ace"])

# # Turn 2

# s.push(slot_1=["queen"])

# # Turn 3

# s.push(slot_1=["king"])