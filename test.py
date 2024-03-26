from lib.conflictUtils import giveNumberOfConflict

test= [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0]
]
print(giveNumberOfConflict(test, 0)) 