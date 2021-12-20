#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)
    
filename = sys.argv[1]

enhancement = ""
in_image = []

with open(filename) as file:
    first = True
    for l in file:
        l = l.strip()
        if first:
            enhancement = l
            first = False
            continue
        
        if l == '':
            continue
        
        in_image.append(l.replace('#', '1').replace('.', '0'))

if len(in_image) != len(in_image[0]):
    print("Non square not sure if this handles that")

def expand(inp, fill, amount=2):
    if len(inp) != len(inp[0]):
        print("expand only works on already square stuff")
        exit(-2)
        
    new_size = len(inp) + 2 * amount
    
    img = [[fill for _ in range(new_size)] for _ in range(new_size)]

    for x, l in enumerate(inp):
        for y, c in enumerate(l):
            img[amount + x][amount + y] = c
            
    return img
    

image = expand(in_image, '0', 2)

enhancement = enhancement.replace('#', '1').replace('.', '0')

outside_val = '0'

def iteration(in_image, outside_val):
    if outside_val == '0':
        new_outside_val = enhancement[0]
    else:
        new_outside_val = enhancement[-1]

    img_size = len(in_image)

    out_image = [['x' for _ in range(img_size)] for _ in range(img_size)]

    def get_c(x, y):
        if x < 0 or x >= img_size or y < 0 or y >= img_size:
            return outside_val
        return in_image[x][y]

    border_non_outside = False

    for x in range(img_size):
        for y in range(img_size):
            bin_n = ''
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    bin_n += get_c(i, j)

            new_val = enhancement[int(bin_n, 2)]
            out_image[x][y] = new_val
            if not border_non_outside and new_val != new_outside_val:
                if x < 2 or x >= img_size - 2 or y < 2 or y >= img_size - 2:
                    border_non_outside = True
    
    
    if border_non_outside:
        out_image = expand(out_image, new_outside_val, 2)
    
    return out_image, new_outside_val

iters = 50



def count_lights(image, outside):
    if outside == '1':
        print("Outside is on so infinity lights are on????")
        exit(-2)
        
    count = 0
    for x in range(len(image)):
        for y in range(len(image)):
            if image[x][y] == '1':
                count += 1
    
    return count
    

for i in range(iters):
    image, outside_val = iteration(image, outside_val)
    #image = expand(image, outside_val)
    
    if i == 1:
        print('#Part 1 after 2 iters ligths on', count_lights(image, outside_val))
    
    #print('\n'.join(''.join('.' if c == '0' else '#' for c in l) for l in image))
    #print(outside_val)

print('#Part 2 after 50 iters ligths on', count_lights(image, outside_val))

