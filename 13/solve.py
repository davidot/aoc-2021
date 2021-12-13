#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]


dots = []
folds = []
max_x = 0
max_y = 0

with open(filename) as file:
    in_dots = True
    
    for l in file:
        l = l.strip()
        if l == '':
            in_dots = False
            continue
        
        if in_dots:
            parts = l.split(',')
            if len(parts) != 2:
                print('Wrong input dots: _', l, '_')
                exit(-1)
            dots.append((int(parts[0]), int(parts[1])))
            if dots[-1][0] > max_x:
                max_x = dots[-1][0]

            if dots[-1][1] > max_y:
                max_y = dots[-1][1]

        else:
            parts = l.split('=')
            if len(parts) != 2:
                print('Wrong input folds: _', l, '_')
                exit(-1)
            folds.append((parts[0][-1], int(parts[1])))



field = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]

for x, y in dots:
    field[y][x] = True

print(max_x, max_y)

def fold_x(field, line):
    width = len(field[0])
    if (width - 1) / 2 != line or width % 2 != 1:
        print('Never instructed how to fold not in the middle??', width, line)
        exit(-3)
    
    field_new = [[False for _ in range(line)] for _ in range(len(field))]

    for y in range(len(field)):    
        for i in range(line):
            if field[y][i] or field[y][width - 1 - i]:
                field_new[y][i] = True
                
    return field_new
                
def fold_y(field, line):
    height = len(field)
    if (height - 1) / 2 != line or height % 2 != 1:
        print('Never instructed how to fold not in the middle??', height, line)
        exit(-3)
    
    field_new = [[False for _ in range(len(field[0]))] for _ in range(line)]

    for x in range(len(field[0])):
        for j in range(line):
            #print(j, height - j)
            if field[j][x] or field[height - 1 - j][x]:
                field_new[j][x] = True
                
    return field_new

def fold(field, direction, line):
    if direction == 'x':
        return fold_x(field, line)
    elif direction == 'y':
        return fold_y(field, line)
    else:
        print('Cant fold', direction, '? ??')
        exit(-2)


#print('\n'.join(''.join('#' if a else '.' for a in l) for l in field))

for direc, line in folds:
    field = fold(field, direc, line)
    #print('Folded --------', direc)
    #print('\n'.join(''.join('#' if a else '.' for a in l) for l in field))
    #break

count = 0
for l in field:
    for b in l:
        if b:
            count += 1
            
print(count, 'dots visible')


print('\n'.join(''.join('#' if a else '.' for a in l) for l in field))

