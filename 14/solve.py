#!/bin/python3

import sys
from collections import Counter
from operator import itemgetter

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

template = ""
replacement_rules = {}
pairs = {}

with open(filename) as file:
    is_template = True
    
    for l in file:
        l = l.strip()
        if l == '':
            continue
            
        if is_template:
            template = l
            is_template = False
            continue
            
        parts = l.split(' -> ')
        if len(parts) != 2:
            print('Unknown input', l)
            exit(-1)
        
        replacement_rules[parts[0]] = parts[1]
        pairs[parts[0]] = 0
        
state = template + ""

for i in range(len(state) - 1):
    pairs[state[i:i+2]] += 1

#print(pairs)

def step(state):
    after = {p: 0 for p in replacement_rules.keys()}

    for pair, count in state.items():
        new_char = replacement_rules[pair]
        first = pair[0]
        second = pair[1]
        after[first + new_char] += count
        after[new_char + second] += count

    return after
    
    
#print('Template      ', state)
for i in range(40):
    pairs = step(pairs)
#    print('Did step', i, pairs)
    #if i < 4:
    #    print('After step', i, ':', state)

counts = {c: 0 for p in replacement_rules.keys() for c in p}

counts[template[0]] = 1
if len(template) > 1:
    counts[template[-1]] = 1

for pair, count in pairs.items():
    counts[pair[0]] += count
    counts[pair[1]] += count
    
min_c, min_count = min(counts.items(), key=itemgetter(1))
max_c, max_count = max(counts.items(), key=itemgetter(1))

if max_count % 2 != 0 or min_count % 2 != 0:
    print('Oh oh', min_count, max_count)
    exit(-3)

min_count //= 2
max_count //= 2

print('Diff: ', max_count - min_count, '(which is', min_c ,'-', max_c, ')')

