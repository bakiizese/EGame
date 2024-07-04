import random

def analyze_and_move(board, player, opponent):
    # Check for any winning moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                # Simulate placing player's move
                board[i][j] = player
                if is_winner(board, player):
                    return i, j
                board[i][j] = ' '

    # Check for any blocking moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                # Simulate placing opponent's move
                board[i][j] = opponent
                if is_winner(board, opponent):
                    board[i][j] = player
                    return i, j
                board[i][j] = ' '

    # If no winning or blocking move, make a random move
    while True:
        i, j = random.randint(0, 2), random.randint(0, 2)
        if board[i][j] == ' ':
            return i, j

def is_winner(board, player):

    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

btns = {
    '00': 'btn1',
    '01': 'btn2',
    '02': 'btn3',
    '10': 'btn4',
    '11': 'btn5',
    '12': 'btn6',
    '20': 'btn7',
    '21': 'btn8',
    '22': 'btn9',
    }

def Caller(board, pl, op):
    bt = analyze_and_move(board, pl, op)
    my_st = ''.join(map(str, bt))
    return (btns[my_st], my_st)



