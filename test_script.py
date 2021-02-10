# test .py script for trial and error bullshit -> should be the library (in the future)
STATE_REPRESENTATION_2 = {'user': "skill_name", 'task': "in_progress",'agent': {"first_card":["ace","confirmed"],"second_card":["king","not_confirmed"]}}
#STATE_REPRESENTATION_2 = { 'first' : ["prdel", "prdel"],
                            #"second": ["hovno", "hovno"]}
STATE_REPRESENTATION_2['agent']['first_card'] = ["kunda","prdel"]
print(STATE_REPRESENTATION_2['agent']['first_card'])                                                                           