from pyrsistent import pvector, v, pmap, m

class Slot:
    
    def __init__(self):
       self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
  
    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        
        if name == 'value':
            if self.is_valid(value.value_confidence['value']):
                if self.value is None:
                    self.__dict__[name] = [value]
                    self.__dict__['state'] = 'unconfirmed'
                else:
                    self.__dict__[name].append(value)
                    self.__dict__[name].sort(key=lambda x: x.value_confidence['confidence'], reverse=True)
                    self.__dict__['state'] = 'inconsistent'
                self.__dict__['first_value'] = self.__dict__[name][0].value_confidence['value']
            else:
                print("value not valid")
        else:
            self.__dict__[name] = value

    def __delattr__(self, name):
         del self.__dict__[name]

    def is_valid(self, value):
        if value in self.cards:
            return True
        else:
            return False

class Value:

    def __init__(self, **kwargs):
        if 'value' in kwargs and 'confidence' in kwargs:
            self.value_confidence = m(value=kwargs['value'], confidence=kwargs['confidence'])
        elif 'value' in kwargs:
            self.value_confidence = m(value=kwargs['value'], confidence=1.0)
        else:
            #self.state = m(value=kwargs['state'])
            self.state = kwargs['state']

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
            
    def __delattr__(self, name):
         del self.__dict__[name]

class State:

    def __init__(self):
    #     self.Agent = Slot()
    #     self.User = Slot()
    #     self.Task = Slot()
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
            self.History.history = self.History.history.append(self.__dict__[name])
            self.__dict__[name] = value
                 
    def __delattr__(self, name):
        self.History.history = self.History.history.append(self.__dict__[name])
        del self.__dict__[name]

    def delete_state_representation(self):
        for attribute in self.__dict__.items():
            
            self.__dict__[attribute] = None
            
        #self.History.history = self.History.history.append(self.__dict__[name])
         
class History:

    def __init__(self):
        self.history = v()

    # def __getattribute__(self, name):
    #     return super().__getattribute__(name)

    # def __getattr__(self, name):
    #     return super().__setattr__(name, None)
            
    # def __delattr__(self, name):
    #      del self.__dict__[name]

# if __name__ == "__main__":
    
#     test_state = State()
#     #user = Slot()
#     #task = Slot()
#     test_state.first_card = Slot()
#     test_state.task_state = Slot()
#     test_state.task_state.state = Value(state='pair')
#     test_state.first_card.value = Value(value="ace")
#     print(test_state.first_card.state)
#     test_state.first_card.state = 'confirmed'

#     print(test_state.delete_state_representation())
    #second_card = Slot()
    #
    #print(test_state.first_card.value[0].value_confidence['value'])
    #print(test_state.History.history)
    #print(test_state.prdel)
    #print(test_state.prdel)
    # print(test_state.prdel)
    # test_state.prdel = "test_1"
    # print(test_state.History.history)
    # test_state.prdel = "test_2"
    # print(test_state.History.history)
    # test_state.prdel = "test_3"
    # print(test_state.History.history)
    # test_state.prdel = "test_4"
    # print(test_state.History.history)
    # test_state.prdel = "test_5"
    # print(test_state.History.history)
    # test_state.prdel = "test_6"
    # print(test_state.History.history)
    # test_state.prdel = "test_7"
    # print(test_state.History.history)
    # test_state.prdel = "test_8"
    # print(test_state.History.history)    
    #print(test_state.prdel)
    #test_state.second_card = second_card
    #print(test_state.first_card.value[0].value)
    
