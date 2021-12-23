#!/bin/python3

import sys

if len(sys.argv) < 2:
    print('Provide filename')
    exit(0)

filename = sys.argv[1]

cost = {1: 1, 2: 10, 3: 100, 4: 1000}

hallway_size = 11
room_index = [2, 4, 6, 8]

steps = {}

hallway_index = []
h_i = 0

for j in range(hallway_size):
    if j in room_index:
        hallway_index.append(None)
    else:
        hallway_index.append(h_i)
        h_i += 1

for j, h_j in enumerate(hallway_index):
    if h_j is None:
        continue

    for i in range(4):
        r_i = room_index[i]

        distance = abs(room_index[i] - j) + 1
        steps_on = [hallway_index[x] for x in range(min(r_i, j), max(r_i, j) + 1) if x not in room_index and x != j]

        steps[(h_j, i)] = (distance, tuple(steps_on))

class State:
    def __init__(self, rooms, hallway, score=0, history=None):
        self.rooms = tuple(tuple(r) for r in rooms)
        self.hallway = tuple(hallway)
        self.score = score
        self.history = history or []
        
    def im_move(self, hall_i, hall_v, room_i, room_d, room_v):
        n_hallway = list(self.hallway)
        n_hallway[hall_i] = hall_v
        n_rooms = [list(r) for r in self.rooms]
        n_rooms[room_i][room_d] = room_v
        return State(n_rooms, n_hallway, self.score + cost[max(room_v, hall_v)] * (steps[(hall_i, room_i)][0] + room_d), self.history + [self])

    def free_to_move(self, hall_i, room_i):
        #print(steps[(hall_i, room_i)][1])
        return all(self.hallway[h] == 0 for h in steps[(hall_i, room_i)][1])
        
    def can_enter(self, room_i):
        return all(occ in (0, room_i + 1) for occ in self.rooms[room_i])
        
    def enter_depth(self, room_i):
        if not self.rooms[room_i][0] == 0:
            print(self, room_i)
            print([str(h) for h in self.history])
            assert False
        for i in range(0, len(self.rooms[room_i])):
            if self.rooms[room_i][i] != 0:
                i -= 1
                break

        assert i >= 0
        return i

    def done(self):
        for i, room in enumerate(self.rooms):
            for r in room:
                if r != i + 1:
                    return False
        return True
        
    def __str__(self):
        return str((self.rooms, self.hallway, self.score))

init_state = None

with open(filename) as file:
    lines = [l.strip() for l in file.readlines() if l.strip() != '']
    
    start_position = [l.replace('#', '') for l in lines[2:4]]
    char_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    
    if len(start_position) != 2:
        print('Wrong input 1')
        exit(-1)

    if len(start_position[0]) != 4 and len(start_position[1]) != 4:
        print('Wrong input 2')
        exit(-1)
    
    rooms_init = [[0 for _ in range(2)] for _ in range(4)]
    
    for i in range(4):
        rooms_init[i][0] = char_map[start_position[0][i]]
        rooms_init[i][1] = char_map[start_position[1][i]]
        
    init_state = State(rooms_init, [0 for j in hallway_index if j is not None])
    


if init_state is None:
    print('No init state')
    exit(-1)

def generate_moves(state: State):
    for i, aut in enumerate(state.hallway):
        if aut == 0:
            continue
        
        want_room = aut - 1
        if state.can_enter(want_room) and state.free_to_move(i, want_room):
            depth = state.enter_depth(want_room)
            yield state.im_move(i, 0, want_room, depth, aut)

    for i, room in enumerate(state.rooms):
        if all(r in (i + 1, 0) for r in room):
            continue
        
        room_depth = room.count(0)
        occ = room[room_depth]
        
        for h_i, spot in enumerate(state.hallway):
            if spot != 0 or not state.free_to_move(h_i, i):
                continue
            yield state.im_move(h_i, occ, i, room_depth, 0)

def solve(init_state):
    states = [init_state]
    finish_states = []

    while states:
        new_states = []

        for state in states:
            for ns in generate_moves(state):
                if ns.done():
                    finish_states.append(ns)
                else:
                    new_states.append(ns)
            
        seen_states = {}
        for s in new_states:
            key = (s.rooms, s.hallway)
            if key not in seen_states:
                seen_states[key] = s
            else:
                pre_score = seen_states[key]
                if pre_score.score > s.score:
                    seen_states[key] = s
        
        states = seen_states.values()
        
    return min(f.score for f in finish_states)

print('Part 1: least score', solve(init_state))

# insert   
#D#C#B#A# -> 4, 3, 2, 1
#D#B#A#C# -> 4, 2, 1, 3

extra = [[4, 4], [3, 2], [2, 1], [1, 3]]

new_rooms = []
for i in range(4):
    new_rooms.append([init_state.rooms[i][0]] + extra[i] + [init_state.rooms[i][1]])
init_state.rooms = tuple(new_rooms)


print('Part 1: least score', solve(init_state))

