import random
from chess import generate_legal_moves, is_game_over, pre_game_over

scores = {'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -
          10**5, 'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 10**5}


def evaluate(fen):
    global scores
    sc = 0
    for i in fen:
        if (i not in scores):
            continue
        sc += scores[i]
    return sc


def minimax(tmp_board, all_moves, white, over, depth, alpha=-10**5-5, beta=10**5+5):
    if (over or depth == 0):
        if (over):
            if (tmp_board.split()[1] == 'b'):
                return (tmp_board, 10**5+1)
            elif (tmp_board.split()[1] == 'w'):
                return (tmp_board, -10**5-1)
            else:
                return (tmp_board, 0)
        if (white):
            mx = -10**5
            move = ''
            for i in all_moves:
                val = evaluate(i.split()[0])

                if (mx < val):
                    mx = val
                    move = i
            return (move, mx)
        else:
            mn = 10**5
            move = ''
            for i in all_moves:
                val = evaluate(i.split()[0])

                if (mn > val):
                    mn = val
                    move = i
            return (move, mn)

    if (white):
        mx = -10**6
        move = ''
        for i in all_moves:
            tmp_all_moves = generate_legal_moves(i)
            val = minimax(i, tmp_all_moves, 0,
                          is_game_over(i), depth-1, alpha, beta)
            if (mx < val[1]):
                mx = val[1]
                move = i
            alpha = max(alpha, mx)
            if (beta <= alpha):
                break
        return (move, mx)
    else:
        mn = 10**6
        move = ''
        for i in all_moves:
            tmp_all_moves = generate_legal_moves(i)
            val = minimax(i, tmp_all_moves, 1,
                          is_game_over(i), depth-1, alpha, beta)
            if (mn > val[1]):
                mn = val[1]
                move = i
            beta = min(beta, mn)
            if (beta <= alpha):
                break
        return (move, mn)


board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"

white = 1
moves = 0
evaluations = []
winner = ''

while ((not is_game_over(board))):
    all_moves = generate_legal_moves(board)
    if (moves % 20 == 0):
        board = random.choice(all_moves)
    elif (moves % 20 == 1):
        board = random.choice(all_moves)
    else:
        if (white):
            print(board)
            winner = "white"
            result = minimax(board, all_moves, 1, is_game_over(board), 1)
            board = result[0]
            white ^= 1
        else:
            print(board)
            winner = "black"
            if (pre_game_over(board)[0]):
                board = pre_game_over(board)[1]
            else:
                board = random.choice(all_moves)
            white ^= 1
    moves += 1
    board_evaluation = evaluate(board.split()[0])
    evaluations.append(board_evaluation)
print(board)
print(winner)
print(evaluations)
