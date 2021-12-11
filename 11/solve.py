#!/bin/python3

import sys

if len(sys.argv)	 < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

lines = []

with open(filename) as file:
    for line in file:
        line = line.strip()
        if line == '':
            continue
        lines.append([int(c) for c in line])
        
length = len(lines[0])
for l in lines:
    if len(l) != length:
        print('Not the same lengths')
        exit(0)



def count_flashes(steps, initial):
    state = [l.copy() for l in initial]
    height = len(state)
    width = len(state[0])
    flashes = 0
    turn = 0
    has_flashed = [[False for _ in range(len(state[0]))] for _ in range(len(state))]
    
    above_nine = []

    
    while steps < 0 or turn < steps:
        turn += 1
        flashes_this_turn = 0
        for j in range(height):
            for i in range(width):
                state[j][i] += 1
                if state[j][i] > 9:
                    has_flashed[j][i] = True
                    above_nine.append((j, i))

        #print('Incremented')
        #print('\n'.join(''.join(f'{i:01x}' for i in l) for l in state))

        while len(above_nine) > 0:
            flashes += 1
            flashes_this_turn += 1
            j, i = above_nine.pop(0)
            has_flashed[j][i] = True
            #state[j][i] = 0
            for jj in range(j - 1, j + 2):
                for ii in range(i - 1, i + 2):
                    if jj < 0 or jj >= height or ii < 0 or ii >= width:
                        continue
                    if has_flashed[jj][ii]:
                        continue
                    state[jj][ii] += 1
                    if state[jj][ii] > 9:
                        has_flashed[jj][ii] = True
                        above_nine.append((jj, ii))
            
        if flashes_this_turn >= width * height:
            print('Everyone flashed at turn: ', turn)
            if steps < 0:
                return turn
        elif turn % 100000 == 0:
            print('At turn', turn)

        #print('Flashed', len(state), len(state[0]), max(state[0]))
        #print('\n'.join(''.join(str(i) for i in l) for l in state))
        
        for j in range(height):
            for i in range(width):
                if has_flashed[j][i]:
                    state[j][i] = 0
                elif state[j][i] > 9:
                    print('What??')
                    
                has_flashed[j][i] = False

    return flashes
    

    
    
print('Part I flashes after 100 steps: ', count_flashes(100, lines))
print('Part I flashes after 100 steps: ', count_flashes(-1, lines))
