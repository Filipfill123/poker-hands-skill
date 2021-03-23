from pyrsistent import pvector, v, pmap, m

class Slot():
    
    def __init__(self):
       self.cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
  
    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        #print(value)
        if name == 'value':
            if self.is_valid(value.value):
                if self.value is None:
                    self.__dict__[name] = [value]
                    self.__dict__['state'] = 'unconfirmed'
                else:
                    self.__dict__[name].append(value)
                    self.__dict__[name].sort(key=lambda x: x.confidence, reverse=True)
                    self.__dict__['state'] = 'inconsistent'
                self.__dict__['first_value'] = self.__dict__[name][0].value
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

class Value():

    def __init__(self, *args, **kwargs):
        self.value = None
        self.confidence = 1.0
        if len(args) != 0:
            self.value = args[0]
        if len(kwargs) != 0:
            if 'confidence' in kwargs:
                self.confidence = kwargs['confidence']

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
            
    def __delattr__(self, name):
         del self.__dict__[name]

class State():

    def __init__(self):
    #     self.Agent = Slot()
    #     self.User = Slot()
    #     self.Task = Slot()
        self.History = History()

    def __getattribute__(self, name):
        return super().__getattribute__(name)

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

class History():

    def __init__(self):
        self.history = v()

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

            
    def __delattr__(self, name):
         del self.__dict__[name]

if __name__ == "__main__":

    
    test_state = State()
    History = History()
    #print(History.history)
    #user = Slot()
    #task = Slot()
    first_card = Slot()
    #second_card = Slot()
    first_card.value = Value("king", confidence=0.1)
    first_card.value = Value("ace", confidence=0.9)
    print(first_card.first_value)
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
    