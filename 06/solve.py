nums = []

filename = "input.txt"

with open(filename) as file:
    for line in file:
        if line.strip() == '':
            continue

        for n in line.split(','):
            n = n.strip()
            nums.append(int(n))


print(nums)

until_days1 = 80
current_part1 = [i for i in nums]

days = 1
while days <= until_days1:
    num_now = len(current_part1)
    for i in range(num_now):
        current_part1[i] -= 1
        if current_part1[i] < 0:
            current_part1[i] = 6
            current_part1.append(8)

    # print(f'After day {days}: {current_part1}')
    days += 1


print(f'After {until_days1} days got {len(current_part1)}')


current_part2 = {i: 0 for i in range(9)}
print(current_part2)
for i in nums:
    current_part2[i] += 1

print(current_part2, nums)

until_days2 = 256
days = 1

while days <= until_days2:
    current = current_part2.copy()
    current[9] = 0
    print(current)
    for i in range(9):
        current_part2[i] = current[i + 1]

    current_part2[6] += current[0]

    if current_part2[8] != 0:
        raise Exception("Something went wrong!")

    current_part2[8] += current[0]

    # print(current)
    # print('real curr', current_part2)

    days += 1

print('done', current_part2)

print(f'After {until_days2} days got {sum(current_part2.values())}')