#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

input_string = ""

with open(filename) as f:
    for l in f:
        input_string = l.strip()
        break
        

x_range = (-1, -1)
y_range = (-1, -1)

rightpart = input_string.split("x=")[1]
bothparts = rightpart.split(",")

def parse_range(s):
    s = s.strip()
    parts = s.split("..")
    if len(parts) != 2:
        print("Invalid range", parts)
        exit(-1)
        return -1, -1
    
    vals = int(parts[0].strip()), int(parts[1].strip())
    return min(vals), max(vals)

x_range = parse_range(bothparts[0])
y_range = parse_range(bothparts[1].split("y=")[1])

        
print(f"Input: _{input_string}_")
print(f"Target: x between {x_range[0]} and {x_range[1]}, y between {y_range[0]} and {y_range[1]}")

#The probe's x,y position starts at 0,0.
#The probe's x position increases by its x velocity.
#The probe's y position increases by its y velocity.
#Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
#Due to gravity, the probe's y velocity decreases by 1.

# Note we assume the area is in the positive x direction and negative y direction

if x_range[0] < 0 or y_range[0] >= 0:
    print("Only works for shooting right down")
    exit(-2)

def hits_area(velocity, y_only=False):
    x = 0
    y = 0
    x_vel = velocity[0]
    y_vel = velocity[1]
    steps = 0
    max_y = 0
    while x <= x_range[1] and y >= y_range[0]:
        if y <= y_range[1]:
            if y_only:
                print(f"Hit y only after {steps} steps {max_y} [{velocity[1]}]")
                return True
            elif x >= x_range[0]:
                return True

        x += x_vel
        
        #print(f"At {(x, y)}")
        
        if x > x_range[1] and not y_only:
            break
        
        y += y_vel
        max_y = max(max_y, y)
        
        #print(f"At {(x, y)}")
        
        if y < y_range[0]:
            break
        
        if x_vel != 0:
            x_vel -= 1 if x_vel > 0 else -1
        y_vel -= 1
        steps += 1
    
    #print("Out of loop")
    return False
        
    

def compute_x():
    hit_min = x_range[0]
    hit_max = x_range[1]
    
    xs = []
    
    for x in range(-1, x_range[1] + 2):
        if (x * (x + 1)) / 2 < x_range[0]:
            continue
        
        xx = 0
        x_v = x
        while xx <= x_range[1]:
            if xx >= x_range[0]:
                xs.append(x)
                break
            xx += x_v
            x_v -= 1
    
    return xs


def compute_all():
    # First try y values until we would never hit it
    
    y_max = 1
    y_hit = 0
    
    possible_ys = []
    
    for y in range(1, 1000):
        if hits_area((0, y), True):
            y_hit = y
            possible_ys.append(y)
    
    possible_xs = compute_x()
    
    hits = []
    for x in possible_xs:
        for y in possible_ys:
            if hits_area((x, y)):
                hits.append((x, y))
        for y in range(y_range[0] - 10, 1):
            if hits_area((x, y)):
                hits.append((x, y))
    
    print("Total hits", len(hits))
    sorted(hits)
    print(hits)
    
    print("7, -1", hits_area((7, -1)))
    
    #while hits_area((0, y_max), True) or y_max < 1000:
    #    y_max += 1
    #    if y_max % 10 == 0:
    #        print(f"Trying {y_max}")
    
    #y_max -= 1

    print(f"Got y max {y_max}")

#print("7, -1", hits_area((7, -1)))
#print("7, -2", hits_area((7, -2)))
compute_all()

