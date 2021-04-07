
class State:
    def __init__(self):
        self.expectations = []  # TODO: change to v()

        self.slot_1 = []
        self.slot_2 = []

    def push(self, **kwargs):
        expectations, self.expectations = self.expectations, []  # TODO: Move into self.history()
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

    def extend(self, slot_1=[], slot_2=[]): # = stary push()
        print("extended values:", slot_1, slot_2)
        self.slot_1.extend(slot_1)
        self.slot_2.extend(slot_2)
        
    def assign(self, slot_1=[], slot_2=[]): # stary solve_inconsistency()
        print("assigned values:", slot_1, slot_2)
        self.slot_1[:] = slot_1
        self.slot_2[:] = slot_2

    def expect(self, cb, *args):
        # TODO: Hack - code necessary to convert slot instances to slot_names,
        # real State class should property to get the names of slots
        slot_names = []  
        for slot_name in dir(self):  # iterate over slots
            for slot in args:
                if getattr(self, slot_name) is slot:
                    slot_names.append(slot_name)

        slot_names = tuple(slot_names)
        # TODO: represent slot_names as v() to include it into the history
        self.expectations.append((cb, slot_names))

    @staticmethod
    def disambig(self, **kwargs):
        self.assign(**kwargs)
        return True  # the slots were handled

    @staticmethod
    def present(self, **kwargs):
        for slot_name in kwargs:
            print("value vas presented", getattr(self, slot_name))


print("""

Example 1

""")

s = State()

# Turn 1

s.push(slot_1=["king", "ace"])
s.expect(s.disambig, s.slot_1)

# Turn 2

s.push(slot_1=["king"], slot_2=["new"])
s.expect(s.present, s.slot_1, s.slot_2)

# Turn 3
s.push()   # handle expectations even if there wasn't any input


print("""

Example 2

""")

s = State()

# Turn 1

def my_disambig(state, slot_1):
    if set(slot_1).issubset(state.slot_1):
        # Accept the disambiguation, it was in the proposed values
        print("Accepted! old value", state.slot_1, "new value", slot_1)
        state.assign(slot_1=slot_1)
        return True
    else:
        # Reject the disambiguation
        print("Rejected! old value", state.slot_1, "new value", slot_1)
        return False

s.push(slot_1=["king", "ace"])
s.expect(my_disambig, s.slot_1)

# Turn 2

s.push(slot_1=["queen"])
s.expect(my_disambig, s.slot_1)

# Turn 3
s.push(slot_1=["queen"])   # handle expectations even if there wasn't any input
s.expect(s.present, s.slot_1)

# Turn 4
s.push()



print("""

Example 3

""")

s = State()

def say_king(state, slot_1):
    if "king" in slot_1:
        print("Good, you said king")
        state.assign(slot_1=slot_1)
        return True
    else:
        print("You have to say king, not", slot_1)
        state.expect(say_king, state.slot_1)
        return True

# Initialization

s.expect(say_king, s.slot_1)

# Turn 1

s.push(slot_1=["ace"])

# Turn 2

s.push(slot_1=["queen"])

# Turn 3

s.push(slot_1=["king"])
