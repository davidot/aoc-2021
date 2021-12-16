#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

input_string = ""

with open(filename) as file:
    for l in file:
        input_string = l.strip()
        break

if len(input_string) == 0:
    print("Did not read any input?")
    exit(-1)

to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

binary_string = ''.join(to_binary[c] for c in input_string)



index = 0

def get_packet():
    global index
    
    def get_bits(count):
        global index
        bits = binary_string[index:index+count]
        index += count
        return bits
        
    def get_num(count):
        return int(get_bits(count), 2)
    
    version = get_num(3)
    type_id = get_num(3)
    
    if type_id == 4:
        # literal

        part = get_bits(5)
        binary_num = part[1:]
        while part[0] == "1":
            part = get_bits(5)
            binary_num += part[1:]
        
        number = int(binary_num, 2)
        return version, type_id, number
    
    length_type_id = get_bits(1)
    
    if length_type_id == "0":
        subpacket_bit_length = get_num(15)
        end_index = index + subpacket_bit_length
        
        packets = []
        
        while index < end_index:
            packets.append(get_packet())
        
    elif length_type_id == "1":
        subpacket_count = get_num(11)
        
        packets = [get_packet() for i in range(subpacket_count)]
    else:
        print('Wrong bit??', length_type_id)
        exit(-2)
    
    
    
    return version, type_id, packets


packet = get_packet()

def sum_version(packet):
    version_sum = packet[0]
    if packet[1] == 4:
        return version_sum
        
    for p in packet[2]:
        version_sum += sum_version(p)
    
    return version_sum
 
print('Total version: ', sum_version(packet))



def evaluate(packet):
    if packet[1] == 4:
        return packet[2]
    
    if packet[1] == 0:
        return sum(evaluate(p) for p in packet[2])
        
    if packet[1] == 1:
        val = 1
        for p in packet[2]:
            val *= evaluate(p)
        return val
        
    if packet[1] == 2:
        return min(evaluate(p) for p in packet[2])

    if packet[1] == 3:
        return max(evaluate(p) for p in packet[2])
        
    if len(packet[2]) != 2:
        print("comparison with non two??")
    
    lhs = evaluate(packet[2][0])
    rhs = evaluate(packet[2][1])
    
    if packet[1] == 5:
        return 1 if lhs > rhs else 0
    
    if packet[1] == 6:
        return 1 if lhs < rhs else 0

    if packet[1] == 7:
        return 1 if lhs == rhs else 0
        
    print("Unknown packets type", packet[1])

print('Evaluate expression', evaluate(packet))

print(index, len(binary_string), int(binary_string[index:], 2))
