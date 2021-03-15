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
        if self.value is None:
            self.__dict__[name] = [value]
        else:
            self.__dict__[name].append(value)
            self.__dict__[name].sort(key=lambda x: x.confidence, reverse=True)

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
            self.confidence = kwargs['confidence']
        

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
            


class State():

    # def __init__(self):
    #     self.Agent = Slot()
    #     self.User = Slot()
    #     self.Task = Slot()
    #     self.History = History()

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return super().__setattr__(name, None)
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value

class History():

    def __init__(self):
        self.history = v()


if __name__ == "__main__":

    # test = State()
    # Value = Value("ace", confidence=0.8, confirmed=False)
    # if Value.value == "ace" and Value.confidence == 0.8:
    #     print("lol")
    test_state = State()
    first_card = Slot()
    second_card = Slot()
    first_card.value = Value("ace", confidence=0.1, confirmed=False)
    first_card.value = Value("king", confidence=0.9, confirmed=False)
    second_card.value = Value("king", confidence=0.9, confirmed=False)
    test_state.first_card = first_card
    test_state.second_card = second_card
    print(first_card.value[0].confidence, first_card.value[1].confidence)
    #test.User.Value = Value(2)
    #print(test.User.Value.value)
    #test.value.value = "ace"
    #print(test.value.confidence)