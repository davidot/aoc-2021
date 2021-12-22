#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

steps = []

with open(filename) as file:
    for l in file:
        l = l.strip()
        if l == '':
            continue
        parts = l.split(' ')
        if len(parts) != 2:
            print("Wrong input?", l)
            exit(-1)
        on_off = parts[0]
        if on_off not in ['on', 'off']:
            print("Wrong input?", l)
            exit(-1)
        on_off = on_off == 'on'

        coords = parts[1].split(',')
        if len(coords) != 3:
            print("Wrong input?", l)
            exit(-1)

        steps.append((on_off, *map(lambda a: (int(a[0]), int(a[1])), map(lambda x: x.split('..'), map(lambda x: x.split('=')[1], coords)))))

print(steps)


def part1():
    cube_on = set()

    for (operation, (x1, x2), (y1, y2), (z1, z2)) in steps:
        xs = max(-50, x1)
        xe = min(51, x2 + 1)
        ys = max(-50, y1)
        ye = min(51, y2 + 1)
        zs = max(-50, z1)
        ze = min(51, z2 + 1)

        hit = set(((x, y, z) for x in range(xs, xe) for y in range(ys, ye) for z in range(zs, ze)))

        if operation:
            cube_on |= hit
        else:
            cube_on -= hit

    return len(cube_on)

print('#Part 1 after init phase: ', part1())


on_intervals = []

def intersect(one, other):
    start = max(one[0], other[0])
    end = max(min(one[1], other[1]), start - 1)
    return start, end

for operation, xx, yy, zz in steps:
    coords = (xx, yy, zz)

    cubes_to_remove = []

    new_cubes = {}

    for i in range(len(on_intervals)):
        c_int = on_intervals[i]

        # compute overlapping cube
        x_int = intersect(c_int[0], coords[0])
        y_int = intersect(c_int[1], coords[1])
        z_int = intersect(c_int[2], coords[2])

        if x_int[1] < x_int[0] or y_int[1] < y_int[0] or z_int[1] < z_int[0]:
            # no overlap
            continue

        # is the same so just remove this, if on we add it later, if off we want to remove this
        if c_int[0] == x_int and c_int[1] == y_int and c_int[2] == z_int:
            cubes_to_remove.append(i)
            continue



        shared = (x_int, y_int, z_int)
        
        # if shared intersect with x other cubes we just do -x (minus one)
        if shared in new_cubes:
            new_cubes[shared] -= c_int[3]
        else:
            new_cubes[shared] = -c_int[3]

    # pop in reverse order to preserve indices
    cubes_to_remove.sort()
    cubes_to_remove.reverse()
    for x in cubes_to_remove:
        on_intervals.pop(x)

    for c, v in new_cubes.items():
        on_intervals.append((*c, v))

    if operation:
        on_intervals.append((*coords, 1))


def size(coord):
    return coord[1] - coord[0] + 1

def area(coords):
    return size(coords[0]) * size(coords[1]) * size(coords[2])
    
score = 0
    
for inter in on_intervals:
    score += area(inter) * inter[3]
    
print('#Part 2 total score: ', score)

