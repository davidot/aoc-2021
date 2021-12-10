#!/bin/python3


filename = "input.txt"

lines = []


with open(filename) as file:
    lines = [l.rstrip('\n') for l in file if l.strip() != '']
    

error_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

closing = ")]}>"

def opend(c):
    if c == ")":
        return "("
    elif c == "]":
        return "["
    elif c == "}":
        return "{"
    elif c == ">":
        return "<"
    else:
        raise Exception("What??")



def check_corrupted1(line):
    stack = []
    
    for c in line:
        if c in closing:
            if len(stack) == 0 or stack[-1] != opend(c):
                return error_score[c], []
            stack.pop()
        else:
            stack.append(c)
            
    if len(stack) > 0:
        return 0, stack

    return 0, []
    


score1 = 0

incompletes = []

for line in lines:
    sc, incomplete = check_corrupted1(line)
    score1 += sc
    if len(incomplete) > 0:
        incompletes.append(incomplete)

print(f'#Part I: total score: {score1}')


autocomplete_score = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

scores = []

for stack in incompletes:
    score = 0
    stack.reverse()
    while len(stack) > 0:
        score *= 5
        v = stack.pop(0)
        score += autocomplete_score[v]
        
        
    scores.append(score)

if len(scores) % 2 != 1:
    print("Not odd scores???")
    raise Exception()
    
scores.sort()

print(f'#Part II: middle score: {scores[len(scores) // 2]}')

