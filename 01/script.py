
file = "input.txt"

numbers = []

with open(file) as f:
    for line in f:
        if line.strip() == '':
            continue
        numbers.append(int(line.strip()))


print(f'Got {len(numbers)} numbers')

if not numbers:
    exit(0)

# PART 1
increasing = 0
last = numbers[0]
for i in range(1, len(numbers)):
    if numbers[i] > last:
        increasing += 1
    last = numbers[i]

print(f'{increasing} increasing numbers')


# PART 2

if len(numbers) <= 2:
    print('Not enough data for windows')
    exit()

increasing_windows = 0
window_size = 1
last_window = sum(numbers[j] for j in range(0, 0 + 3))

for i in range(len(numbers) - 2):
    window_value = sum(numbers[j] for j in range(i, i + 3))
    if window_value > last_window:
        increasing_windows += 1
    last_window = window_value

print(f'{increasing_windows} increasing windows')