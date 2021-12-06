import numpy as np

boards = []
with open('inputs/7.txt', 'r') as in_f:
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

for n in numbers:
    for b in boards:
        if verify_board(b, n):
            print(get_score(b, n))
            quit()
