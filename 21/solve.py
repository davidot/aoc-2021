#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)
    
filename = sys.argv[1]

start_positions = []

with open(filename) as file:
    for l in file:
        l = l.strip()
        if l == '':
            continue
        parts = l.split(':')
        if len(parts) != 2:
            print("Wrong input?", l)
            exit(-1)
        
        start_positions.append(int(parts[1].strip()))



if len(start_positions) != 2:
    print("Only support two starting positions")
    exit(-3)
    

start1 = start_positions[0] - 1
start2 = start_positions[1] - 1

def play_game(dieroll, max_score=1000, winner_only=False):

    score1 = 0
    score2 = 0
    
    pos1 = start1
    pos2 = start2
    
    while score2 < max_score:
        
        pos1 = (pos1 + dieroll() + dieroll() + dieroll()) % 10
        score1 += pos1 + 1
        if score1 >= max_score:
            break
            
        pos2 = (pos2 + dieroll() + dieroll() + dieroll()) % 10
        score2 += pos2 + 1
            
            
    if (score1 < max_score and score2 < max_score) or score1 == score2:
        print("Done before any win? or equal", score1, score2)
        exit(-2)
        
    if winner_only:
        return score1 > score2
        
    return dieroll(True), max(score1, score2), min(score1, score2)
        
        
def get_deterdice(top_v=1000):
    class DeterDice:
        val = 1
        top = top_v
        rolls = 0
        
    def roll(get_rolls=False):
        if get_rolls:
            return DeterDice.rolls

        v = DeterDice.val
        DeterDice.val += 1
        DeterDice.rolls += 1
        if DeterDice.val > DeterDice.top:
            DeterDice.val = 1
            
        return v
            
    return roll
    
rolled, win_score, lose_score = play_game(get_deterdice())
print('Part 1 results: ', rolled, win_score, lose_score)
print('#Part 1: ', rolled * lose_score)


# With the dirac dice you roll between 3 and 9, it doesn't actually matter what the exact dice rolls are

possible_rolls = {i: 0 for i in range(3, 10)}

for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            possible_rolls[i+j+k] += 1
            
#print(possible_rolls)

dirac_score = 21

dirac_cache = {}

def dirac_win(pos1, score1, pos2, score2, turn1, depth = 0):
    global dirac_cache
    if score1 >= dirac_score:
        return 1, 0
    if score2 >= dirac_score:
        return 0, 1
        
    c = dirac_cache.get((pos1, score1, pos2, score2, turn1), None)
    if c is not None:
        return c
        
    if depth > 10:
        print("Depth: ", depth)

    p1_wins = 0
    p2_wins = 0
    
    pos1_init = pos1 + 0
    score1_init = score1 + 0
    pos2_init = pos2 + 0
    score2_init = score2 + 0
    

    for roll, times in possible_rolls.items():
        if turn1:
            pos1 = (pos1_init + roll) % 10
            score1 = score1_init + pos1 + 1
        else:
            pos2 = (pos2_init + roll) % 10
            score2 = score2_init + pos2 + 1
            
        w1, w2 = dirac_win(pos1, score1, pos2, score2, not turn1)
        p1_wins += w1 * times
        p2_wins += w2 * times
    

    dirac_cache[(pos1_init, score1_init, pos2_init, score2_init, turn1)] = (p1_wins, p2_wins)
    
    return p1_wins, p2_wins

p1_wins, p2_wins = dirac_win(start1, 0, start2, 0, True)

print('Part 2: ', p1_wins, p2_wins, 'best score', max(p1_wins, p2_wins))

