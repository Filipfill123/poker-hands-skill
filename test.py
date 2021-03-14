from pyrsistent import pvector, v

class Slot():
    
    #def __init__(self):
       # self.Value = Value()
       # self.State = None
  
    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def is_valid(self, value):
        if value == "ace":
            return True
        else:
            return False

class Value():

    def __init__(self, *args, **kwargs):
        self.value = None
        self.confidence = 1.0
        self.state = None
        if len(args) != 0:
            self.value = args[0]
        if len(kwargs) != 0:
            #print(kwargs)
            self.confidence = kwargs['confidence']
        

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value


class State():

    def __init__(self):
        self.Agent = Slot()
        self.User = Slot()
        self.Task = Slot()
        self.History = History()

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)


class History():

    def __init__(self):
        self.history = v()


if __name__ == "__main__":

    # test = State()
    # Value = Value("ace", confidence=0.8, confirmed=False)
    # if Value.value == "ace" and Value.confidence == 0.8:
    #     print("lol")

    test_slot = Slot()
    test_slot.first_card = Value("ace", confidence=0.8, confirmed=False)
    test_slot.second_card = Value("ace", confidence=0.9, confirmed=False)

    if test_slot.first_card.value == test_slot.second_card.value:
        print("jop")
    #test.User.Value = Value(2)
    #print(test.User.Value.value)
    #test.value.value = "ace"
    #print(test.value.confidence)