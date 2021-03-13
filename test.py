from pyrsistent import pvector, v

class Slot():
    
    def __init__(self):
        self.value = Value()
        self.state = "unconfirmed"
  
    def __getattribute__(self, name):
        return super(Slot, self).__getattribute__(name)    # Gets called when the item is not found via __getattribute__

    def __getattr__(self, name):
        return super(Slot, self).__setattr__(name, 'nothing')

class Value():

    def __init__(self):
        self.value = None
        self.confidence = 1.0


class State():

    def __init__(self):
        self.Agent = Slot()
        self.User = Slot()
        self.Task = Slot()
        self.History = History()


class History():

    def __init__(self):
        self.history = v()



if __name__ == "__main__":

    test = Slot()
    print(test.prdel)
    print(test.prdel)
    #test.value.value = "ace"
    #print(test.value.confidence)