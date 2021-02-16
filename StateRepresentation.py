#### we need state representation initialization:
#### 1) we need states for user intention, 2) task progress
#### 3) we need to know which slates of agent's state are compulsory etc. and the numbers of slates


#### functions:
#### 1) fill slate with either the first UNCONFIRMED card or the second UNCONFIRMED
#### 2) fill slate with both UNCONFIRMED cards (1) and 2) SET FUNCTIONS)
#### 3) GET FUNCTIONS for both cards
#### 4) SET FUNCTIONS for CONFIRMED (alternatively change card/s and CONFIRM it/them)

def initialize_state_representation(skill_name, no_of_slates, compulsory_slates, possible_outcomes = ["no_pair", "in_progress", "pair"]):
    task_state = possible_outcomes[1]
    state_representation = {'user': skill_name,'agent': {},'task': task_state}
    for i in range(no_of_slates):
        state_representation["agent"][f"card_{i+1}"] = [None,None,"compulsory"]

    return state_representation


lol = initialize_state_representation('prdel',2,2)

print(lol['agent']['card_2'])
