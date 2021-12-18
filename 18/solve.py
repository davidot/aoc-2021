#!/bin/python3

import sys
import copy

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)
    
filename = sys.argv[1]

sums = []


index = 0
    
def parse_sum(line):
    global index
    index = 0

    def parse_pair():
        global index
        result = []

        if line[index] != '[':
            print("Bad input 1", line, index, line[index])
            exit(-1)
        
        index += 1
        
        if line[index] == ',' or line[index] == ']':
            print("Bad input 2", line, index, line[index])
            exit(-1)
            
        if line[index] == '[':
            result.append(parse_pair())
        else:
            # We SHOULD always find a , here
            number_end = line.find(',', index)
            if number_end < 0:
                print("Bad input 3", line, index, line[index])
                exit(-1)
            
            
            result.append(int(line[index:number_end]))
            index = number_end
        
        if line[index] != ',':
            print("Bad input 4", line, index, line[index])
            exit(-1)
            
        index += 1
        
        if line[index] == '[':
            result.append(parse_pair())
        else:
            # We SHOULD always find a ] here
            number_end = line.find(']', index)
            if number_end < 0:
                print("Bad input 5", line, index, line[index])
                exit(-1)
            
            result.append(int(line[index:number_end]))
            index = number_end
        
        if line[index] != ']':
            print("Bad input 6", line, index, line[index])
            exit(-1)
            
        index += 1
        
        if len(result) != 2:
            print("Bad input 7", line, index, line[index])
            exit(-1)
            
        
        return result
        
    return parse_pair()
        
    
    

with open(filename) as f:
    for l in f:
        l = l.strip()
        if l == '':
            continue
            
        sums.append(parse_sum(l))

def is_array(l):
    return isinstance(l, list)

def reduce(arr):
    arr = arr
    change = True
    
    def check_explode():
    
        def add_right(item, add):
            if is_array(item[0]):
                add_right(item[0], add)
            else:
                item[0] += add
                
        def add_left(item, add):
            while is_array(item[1]):
                item = item[1]
            
            item[1] += add
            
    
        def rec_explode(item, depth):
            #print("Rec expl on", depth, " with", item)
            if depth < 4:
                if is_array(item[0]):
                    l, r, exploded = rec_explode(item[0], depth + 1)
                    if exploded:
                        if is_array(item[1]):
                            add_right(item[1], r)
                        else:
                            item[1] += r
                        
                        return l, 0, True

                if is_array(item[1]):                
                    l, r, exploded = rec_explode(item[1], depth + 1)
                    if exploded:
                        if is_array(item[0]):
                            add_left(item[0], l)
                        else:
                            item[0] += l
                        
                        return 0, r, True

                return 0, 0, False

            # Any nested pair can explode!
            
            #print("Potential explode", item)
            
            if is_array(item[0]):
                l = item[0][0]
                r = item[0][1]
                if is_array(l) or is_array(r):
                    print("Exploding array?", item[0])
                    exit(-3)
                item[0] = 0
                
                if is_array(item[1]):
                    add_right(item[1], r)
                else:
                    item[1] += r
                    
                
                return l, 0, True

            if is_array(item[1]):
                l = item[1][0]
                r = item[1][1]
                if is_array(l) or is_array(r):
                    print("Exploding array?", item[1])
                    exit(-3)
                item[1] = 0
                
                if is_array(item[0]):
                    add_left(item[0], l)
                else:
                    item[0] += l
                
                return 0, r, True

            return 0, 0, False
         
        #print("Checking explode on", arr)
        _, _, exploded = rec_explode(arr, 1)
        
        return exploded
                    

    def check_split():
        
        def rec_split(item):
            for i in range(2):
                if is_array(item[i]):
                    if rec_split(item[i]):
                        return True
                elif item[i] > 9:
                    val = item[i]
                    item[i] = [val // 2, (val + 1) // 2]
                    return True
            
            return False

        split = rec_split(arr)
        return split        
          
        
    
    #print("Start", arr)
    
    while change:
        change = False
        
        if check_explode():
            change = True
            #print("Boom ", arr)
        elif check_split():
            change = True
            #print("Split", arr)
            
            
        #break
        
    return arr
        

running_sum = copy.deepcopy(sums[0])
for i in range(1, len(sums)):
    running_sum = [running_sum, copy.deepcopy(sums[i])]
    reduce(running_sum)
    
    
def magnitude(arr):
    def mag(item):
        if is_array(item):
            return 3 * mag(item[0]) + 2 * mag(item[1])
        return item

    return mag(arr)

    
print(magnitude(running_sum))


computes = 0
max_mag = 0

for i in range(len(sums)):
    for j in range(len(sums)):
        if i == j:
            continue
        max_mag = max(max_mag, magnitude(reduce([copy.deepcopy(sums[i]), copy.deepcopy(sums[j])])))
        
        
print("Maximum magnitude: ", max_mag)



# the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up.



