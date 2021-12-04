filename = "input.txt"


boards = []
draws = []

def read_numbers(line, splitter):
    numbers = []
    for part in line.split(splitter):
        if part.strip() == '':
            continue
        numbers.append(int(part.strip()))
    
    return numbers

with open(filename) as file:
    reading_draws = True
    current_board = []
    for line in file:
        if line.strip() == '':
            continue

        if reading_draws:
            draws = read_numbers(line, ',')
            reading_draws = False
            continue
        
        if len(current_board) == 5:
            boards.append(current_board)
            current_board = []
        
        next_row = read_numbers(line, ' ')
        current_board.append(next_row)
        
    if len(current_board) != 5:
        print('Missing parts for last board!')
    else:
        boards.append(current_board)

def compute_score_for_board(board):
    picked = [[False for _ in range(5)] for _ in range(5)]
    
    def has_won():
        for i in range(5):
            if all(picked[i]):
                return True
            
            any_false = False
            
            for j in range(5):
                if not picked[j][i]:
                    any_false = True
                    break
            if not any_false:
                return True
    
    i = 0
    won = False
    
    while i < len(draws):
        next_num = draws[i]
        for r, row in enumerate(board):
            for c, spot in enumerate(row):
                if spot == next_num:
                    picked[r][c] = True
        if has_won():
            won = True
            #print(f'Board won after: {i} draws')
            break
        i += 1
    
    if not won:
        print('Board never won!!')
        return len(draws) + 1, -1
    
    sum = 0
    
    for r, row in enumerate(picked):
        for c, spot in enumerate(row):
            if not spot:
                sum += board[r][c]

    #print(f'Got sum {sum}')
    
    score = sum * draws[i]
    return i + 1, score
    


#print(draws)
#print(boards)

min_turns = len(draws) + 1
score = -1


# All boards win eventually so no need for that edge case
max_turns = 0
max_turns_score = -1

for b in boards:
    turns, new_score = compute_score_for_board(b)
    if turns == min_turns:
        print(f'Got same turns but score: {score} vs new {new_score}')
    if turns < min_turns:
        min_turns = turns
        score = new_score
        
        
    if turns > max_turns:
        max_turns_score = new_score
        max_turns = turns

print(f'min_turns {min_turns}, score {score}')
print(f'max_turns {max_turns}, score {max_turns_score}')