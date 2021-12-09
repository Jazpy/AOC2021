import numpy as np

boards = []
with open('inputs/d4.txt', 'r') as in_f:
    numbers = [int(x) for x in in_f.readline().split(',')]
    in_f.readline()

    curr_board = []
    for line in in_f.readlines():
        if line.strip() == '':
            boards.append(np.array(curr_board))
            curr_board = []
            continue

        curr_board.append(np.array([int(x) for x in line.split()]))

def verify_board(b, n):
    b[b == n] = -1

    for i in range(5):
        if sum(b[:, i]) == -5 or sum(b[i, :]) == -5:
            return True

    return False

def get_score(b, n):
    return sum(b[b != -1]) * n

last_score = 0
for n in numbers:
    for idx, b in enumerate(boards):
        if b.any() and verify_board(b, n):
            last_score = get_score(b, n)
            boards[idx] = np.empty(0)

print(last_score)
