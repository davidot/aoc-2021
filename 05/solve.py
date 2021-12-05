lines = []

filename = "input.txt"

with open(filename) as file:
    for line in file:
        if line.strip() == '':
            continue

        parts = line.split(' -> ')
        def parse_line(part):
            p = part.split(',')
            if len(p) != 2:
                raise Exception("Wrong input")
            return [int(p[0]), int(p[1])]


        if len(parts) != 2:
            raise Exception("Wrong input")

        lines.append([parse_line(parts[0]), parse_line(parts[1])])


# print(lines)

board = [[0 for _ in range(1000)] for _ in range(1000)]

def add_line1(l_board, line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    if x1 != x2 and y1 != y2:
        return

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            l_board[y][x1] += 1
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            l_board[y1][x] += 1
    else:
        raise Exception(f"uh what? {line}")

def add_diag_line(l_board, line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    if x1 == x2 or y1 == y2:
        return

    swapped = False

    if x1 > x2:
        # print('preswap', x1, y1, x2, y2)
        swapped = True
        temp = x2
        x2 = x1
        x1 = temp
        # print('midswap', x1, y1, x2, y2)
        temp = y2
        y2 = y1
        y1 = temp
        # print('postswap', x1, y1, x2, y2)

    if y2 > y1:
        x, y = x1, y1
        while x < x2 and y < y2:
            # print(x, y)
            # if x >= 1000 or y >= 1000:
            #     print(x, y, x1, y1, x2, y2)
            l_board[y][x] += 1
            x += 1
            y += 1

        if x != x2 or y != y2:
            print('f1', x1, y1, x2, y2, swapped)
            raise Exception("oh no")
        else:
            l_board[y2][x2] += 1

    elif y1 > y2:
        x, y = x1, y1
        while x < x2 and y > y2:
            # if x >= 1000 or y >= 1000:
            #     print(x, y, x1, y1, x2, y2)
            l_board[y][x] += 1
            x += 1
            y -= 1

        if x != x2 or y != y2:
            print('f2', x1, y1, x2, y2, swapped, x, y)
            raise Exception("oh no")
        else:
            l_board[y2][x2] += 1
    else:
        raise Exception("wrong input???")


for l in lines:
    add_line1(board, l)

hits1 = 0

for y in board:
    for x in y:
        if x >= 2:
            hits1 += 1

print(hits1)

for l in lines:
    add_diag_line(board, l)

hits2 = 0

for y in board:
    for x in y:
        if x >= 2:
            hits2 += 1

print(hits2)




