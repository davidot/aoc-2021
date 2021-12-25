#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]


with open(filename) as file:
    lines = [l.strip() for l in file.readlines() if l.strip() != '']



state = lines
width = len(lines[0])
height = len(lines)


def move(state):
    any_moved = False
    
    new_state = [['.' for _ in range(width)] for _ in range(height)]
    
    non_dot = 0
    
    for y in range(height):
        for x in range(width):
            if state[y][x] == '>':
                target_x = (x + 1) % width
                if state[y][target_x] == '.':
                    assert new_state[y][target_x] == '.'
                    new_state[y][target_x] = '>'
                    any_moved = True
                else:
                    assert new_state[y][x] == '.'
                    new_state[y][x] = '>'
    
    for y in range(height):
        for x in range(width):
            if state[y][x] == 'v':
                target_y = (y + 1) % height
                if new_state[target_y][x] == '.' and state[target_y][x] != 'v':
                    assert new_state[target_y][x] == '.'
                    new_state[target_y][x] = 'v'
                    any_moved = True
                else:
                    assert new_state[y][x] == '.'
                    new_state[y][x] = 'v'

    
    return new_state, any_moved


steps = 0
any_moved = True

while any_moved and steps < 1000:
    state, any_moved = move(state)
    steps += 1
    
    #if steps >= 58:
    #    print('After step', steps)
    #    print('\n'.join(''.join(c for c in l) for l in state))
    #    break
    
print('Took', steps, any_moved)