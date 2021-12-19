#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)
    
filename = sys.argv[1]

scanners = []

with open(filename) as file:
    scanner = []
    
    for l in file:
        l = l.strip()
        if l == '':
            continue
            
        if l.startswith('--- scanner'):
            if scanner is not None and len(scanner) > 0:
                scanners.append(scanner)
            scanner = []
            continue
        
        scanner.append(tuple(int(n) for n in l.split(',')))
    
    if len(scanner) > 0:
        scanners.append(scanner)

rotations = []

def add_rotation(x, y, z):
    def sign(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            print("Cannot have sign for 0")
            exit(-3)
    
    abss = [abs(x), abs(y), abs(z)]
    signs = [sign(x), sign(y), sign(z)]
    
    mat = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        mat[abss[i] - 1][i] = signs[i]
    
    
    # Only matrices with |A| = 1 are valid rotations (no mirroring)
    det = 0
    for i in range(3):
      det += mat[0][i] * (mat[1][(i+1) % 3] * mat[2][(i+2) % 3] - mat[1][(i+2)%3] * mat[2][(i+1) % 3])

    if det != 1:
        return

    rotations.append(mat)

for x in range(1, 4):
    for y in range(1, 4):
        for z in range(1, 4):
            if x == y or x == z or y == z:
                continue
            add_rotation(x, y, z)
            add_rotation(x, y, -z)
            add_rotation(x, -y, z)
            add_rotation(x, -y, -z)
            add_rotation(-x, y, z)
            add_rotation(-x, y, -z)
            add_rotation(-x, -y, z)
            add_rotation(-x, -y, -z)


def apply_rotation(coord, rotation):
    return (coord[0] * rotation[0][0] + coord[1] * rotation[0][1] + coord[2] * rotation[0][2],
            coord[0] * rotation[1][0] + coord[1] * rotation[1][1] + coord[2] * rotation[1][2],
            coord[0] * rotation[2][0] + coord[1] * rotation[2][1] + coord[2] * rotation[2][2])

def dist(c1, c2):
  return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2

scanners_dists = []

for s in scanners:
    distances = []
    for i in range(len(s)):
        c_dist = set()
        for j in range(len(s)):
            if i == j:
                continue
            c_dist.add(dist(s[i], s[j]))
        
        distances.append(c_dist)
    
    scanners_dists.append(distances)


sharing = {}

for i in range(len(scanners)):
    for j in range(i + 1, len(scanners)):
        for x in range(len(scanners_dists[i])):
            for y in range(len(scanners_dists[j])):
                if len(scanners_dists[i][x] & scanners_dists[j][y]) >= 11:
                    sharing.setdefault((i, j), set()).add((scanners[i][x], scanners[j][y]))
                    

 
picked_translation = {}

def compute_inverse(matrix):
    # since they always have det 1 we just transpose
    return [ [matrix[0][0], matrix[1][0], matrix[2][0]],
        [matrix[0][1], matrix[1][1], matrix[2][1]],
        [matrix[0][2], matrix[1][2], matrix[2][2]] ]
 
# we want to find which transformations work and what the translation has to be
for (i, j), pairs in sharing.items():
    for r in rotations:
        new_dists = set((dist(p[0], apply_rotation(p[1], r)) for p in pairs))
        if len(new_dists) == 1:
            # If all pairs have same distance now the rotation is correct
            
            a, b = next(iter(pairs))
            b = apply_rotation(b, r)
            
            picked_translation[(i, j)] = [(r, (a[0] - b[0], a[1] - b[1], a[2] - b[2]))]
            inv = compute_inverse(r)
            picked_translation[(j, i)] = [(inv, apply_rotation((b[0] - a[0], b[1] - a[1], b[2] - a[2]), inv))]
            break

#print(picked_translation)

 
# generate transformations from 0 to everything

done = [0]
picked_translation[(0, 0)] = []

for i in range(1, len(scanners)):
    if (0, i) in picked_translation:
        done.append(i)

ii = 0
while len(done) < len(scanners):
    if ii > 100:
        print("Too many iters")
        exit(4)
        break
    ii += 1
    #print("Going", picked_translation)

    for i in range(1, len(scanners)):
        if (0, i) not in picked_translation:
            continue

        tr = picked_translation[(0, i)]
        for j in range(1, len(scanners)):
            if (0, j) in picked_translation or (i, j) not in picked_translation:
                continue

            picked_translation[(0, j)] = [*picked_translation[(i, j)], *tr]
            done.append(j)

    
#for i in range(len(scanners)):
#    print(f'{i} by ', picked_translation.get((0, i), None))


def add(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])
    
def add_inv(c1, c2):
    return (c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2])
 
# This could be very wrong 
def apply_inv_rotation(coord, rotation):
    print(coord, rotation)
    return (coord[0] * rotation[0][0] + coord[1] * rotation[1][0] + coord[2] * rotation[2][0],
            coord[0] * rotation[0][1] + coord[1] * rotation[1][1] + coord[2] * rotation[2][1],
            coord[0] * rotation[0][2] + coord[1] * rotation[1][2] + coord[2] * rotation[2][2])

 
abs_points = set()

sonar_pos = []

 
for i, s in enumerate(scanners):

    sonar = (0, 0, 0)
    for t in picked_translation[(0, i)]:
        sonar = apply_rotation(sonar, t[0])
        sonar = add(sonar, t[1])
    
    sonar_pos.append(sonar)
    
    for point in s:
        for t in picked_translation[(0, i)]:
            point = apply_rotation(point, t[0])
            point = add(point, t[1])
        
        abs_points.add(point)

print('#PART 1 num of points: ', len(abs_points))

max_diff = 0

for a in sonar_pos:
    for b in sonar_pos:
        if a == b:
            continue
        
        max_diff = max(max_diff, sum(abs(a[i] - b[i]) for i in range(3)))
        
        
print("#part 2: max distance manhattan", max_diff)



