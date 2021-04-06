from StateRepres import Value
from dataclasses import dataclass, field

@dataclass
class Cards(Value):
    valid: bool = None

    def __post_init__(self):
        cards = ('ace','king','queen','jack','ten','nine','eight','seven','six','five','four','three','two')
        if self.value in cards: 
            self.valid = True
        else:
            self.valid = False
            # raise(ValueError)

if __name__ == "__main__":
    card = Cards('test')
    print(card.valid)
