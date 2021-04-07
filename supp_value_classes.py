from StateRepres import Value
from dataclasses import dataclass, field
import datetime
# do budoucna - prevest na semantickou reprezentaci reci

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
class Time(Value):
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

    value_card = Cards('ace')
    print(value_card.value)