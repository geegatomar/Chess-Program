#!/bin//bash/python3

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

board = [['_']*8 for i in range(8)]
MOVES_NEXT = 'w'
CASTLING_AVAILABILTY = "KQkq"
EN_PASSANT = '-'


def interpret_FEN():
    l = FEN.replace("/", " ").split()
    #print(l)
    for row in range(8):
        ptr = 0
        for i in range(len(l[row])):
            if l[row][i].isalpha():
                board[row][ptr] = l[row][i]
                ptr += 1
            else:
                ptr += int(l[row][i])
    global MOVES_NEXT
    MOVES_NEXT = l[8]
    global CASTLING_AVAILABILTY
    CASTLING_AVAILABILTY = l[9]
    global EN_PASSANT
    EN_PASSANT = l[10]


def board_view():
    for i in range(8):
        print('  _ ', end="")
    print()
    for rows in range(8):
        for square in range(8):
            print('|', board[rows][square], "", end="")
        print('|')



interpret_FEN()
board_view()
#from ChessFEN import *

PGN = "1.e4 d5 2.exd5 Nf6 3.d4 Nxd5 4.c4 Nb6 5.Nc3 g6 6.Be3 Bg7 7.h3 O-O 8.Qd2 Nc6 9.Nf3 e5 10.d5 Ne7 11.g4 f5 12.O-O-O e4 13.Ng5 h6 14.Ne6 Bxe6 15.dxe6 Qxd2+ 16.Rxd2 Rad8 17.Bc5 Rxd2 18.Kxd2 Rd8+ 19.Kc2 Nc6 20.gxf5 Nd4+ 21.Bxd4 Rxd4 22.Rg1 g5 23.c5 Nc4 24.Bxc4 Rxc4 25.Rd1 Bf6 26.Kb3 Rxc5 27.Nxe4 Rxf5 28.Nxf6+ Kf8 29.Ng4 h5 30.Ne3 Rf3 31.Rd5 g4 32.hxg4 1-0"
set_of_moves = []
PLAYER1 = 'w'
PLAYER2 = 'b'
alpha_to_index = dict(zip(list("abcdefgh"), list("01234567")))
num_to_index = dict(zip(list("876543210"), list("01234567")))


def decide_player():
    global PLAYER1
    global PLAYER2
    if MOVES_NEXT == 'w':
        PLAYER1, PLAYER2 = 'w', 'b'
    else:
        PLAYER1, PLAYER2 = 'b', 'w'


def interpret_PGN():
    global set_of_moves
    set_of_moves = PGN.replace('.', ' ').split(' ')
    ind = 0
    while ind < len(set_of_moves):
        set_of_moves.remove(set_of_moves[ind])
        ind += 2
    print(set_of_moves)


def is_pawn_move(move):
    return len(move[1]) == 2


def make_pawn_move(move):
    color, finalpos = move
    col = int(alpha_to_index[finalpos[0]])
    row = int(num_to_index[finalpos[1]])
    if color == 'w':
        if board[row + 2][col] == 'P':
            board[row + 2][col] = '_'
        else:
            board[row + 1][col] = '_'
        board[row][col] = 'P'
    else:
        if board[row - 2][col] == 'p':
            board[row - 2][col] = '_'
        else:
            board[row - 1][col] = '_'
        board[row][col] = 'p'


def is_valid(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def change_on_board(row, col, piece, a, b):
    board[row + a][col + b] = '_'
    board[row][col] = piece


def knight_move(color, row, col):
    print(row, col)
    if color == 'w':
        for a in [-1, -2, 1, 2]:
            for b in [-1, -2, 1, 2]:
                if is_valid(row + a, col + b) and abs(a) != abs(b):
                    if board[row + a][col + b] == 'N':
                        change_on_board(row, col, 'N', a, b)
                        return
    else:
        for a in [-1, -2, 1, 2]:
            for b in [-1, -2, 1, 2]:
                if is_valid(row + a, col + b) and abs(a) != abs(b):
                    if board[row + a][col + b] == 'n':
                        change_on_board(row, col, 'n', a, b)
                        return


def bishop_move(color, row, col):
    for a in range(-7, 7):
        if is_valid(row + a, col + a) and a != 0:
            if board[row + a][col + a] in 'Bb':
                if color == 'w' and board[row + a][col + a] == 'B':
                    change_on_board(row, col, 'B', a, a)
                    return
                if color == 'b' and board[row + a][col + a] == 'b':
                    change_on_board(row, col, 'b', a, a)
                    return

        if is_valid(row - a, col + a) and a != 0:
            if board[row - a][col + a] in 'Bb':
                if color == 'w' and board[row - a][col + a] == 'B':
                    change_on_board(row, col, 'B', -a, a)
                    return
                if color == 'b' and board[row - a][col + a] == 'b':
                    change_on_board(row, col, 'b', -a, a)
                    return


def rook_move(color, row, col):
    for a in range(-7, 7):
        if is_valid(row + a, col):
            if board[row + a][col] == 'R' and color == 'w' and a != 0:
                change_on_board(row, col, 'R', a, 0)
                return
            if board[row + a][col] == 'r' and color == 'b' and a != 0:
                change_on_board(row, col, 'r', a, 0)
                return
        if is_valid(row, col + a):
            if board[row][col + a] == 'R' and color == 'w' and a != 0:
                change_on_board(row, col, 'R', 0, a)
                return
            if board[row][col + a] == 'r' and color == 'b' and a != 0:
                change_on_board(row, col, 'r', 0, a)
                return


def queen_move(color, row, col):
    for a in range(-7, 7):
        if is_valid(row + a, col):
            if board[row + a][col] == 'Q' and color == 'w' and a != 0:
                change_on_board(row, col, 'Q', a, 0)
                return
            if board[row + a][col] == 'q' and color == 'b' and a != 0:
                change_on_board(row, col, 'q', a, 0)
                return
        if is_valid(row, col + a):
            if board[row][col + a] == 'Q' and color == 'w' and a != 0:
                change_on_board(row, col, 'Q', 0, a)
                return
            if board[row][col + a] == 'q' and color == 'b' and a != 0:
                change_on_board(row, col, 'q', 0, a)
                return
        if is_valid(row + a, col + a):
            if board[row + a][col + a] == 'Q' and color == 'w' and a != 0:
                change_on_board(row, col, 'Q', a, a)
                return
            if board[row + a][col + a] == 'q' and color == 'b' and a != 0:
                change_on_board(row, col, 'q', a, a)
                return
        if is_valid(row + a, col - a):
            if board[row + a][col + a] == 'Q' and color == 'w' and a != 0:
                change_on_board(row, col, 'Q', a, -a)
                return
            if board[row + a][col - a] == 'q' and color == 'b' and a != 0:
                change_on_board(row, col, 'q', a, -a)
                return


def king_move(color, row, col):
    if color == 'w':
        for i in range(-1, 1):
            for j in range(-1, 1):
                if board[row + i][col + j] == 'K' and i * j != 0:
                    change_on_board(row, col, 'K', i, j)
    else:
        for i in range(-1, 1):
            for j in range(-1, 1):
                if board[row + i][col + j] == 'k' and i * j != 0:
                    change_on_board(row, col, 'k', i, j)


def make_move(move):
    color = move[0]
    piece = move[1][0]
    row = int(num_to_index[move[1][2]])
    col = int(alpha_to_index[move[1][1]])
    if piece == 'N':
        knight_move(color, row, col)
    elif piece == 'B':
        bishop_move(color, row, col)
    elif piece == 'R':
        rook_move(color, row, col)
    elif piece == 'Q':
        queen_move(color, row, col)
    else:
        king_move(color, row, col)


def is_capture(move):
    return 'x' in move[1]


def capture_by_pawn(color, pos):
    initial_col = int(alpha_to_index[pos[0]])
    row = int(num_to_index[pos[2]])
    col = int(alpha_to_index[pos[1]])
    if color == 'w':
        board[row + 1][initial_col] = '_'
        board[row][col] = 'P'
    else:
        board[row - 1][initial_col] = '_'
        board[row][col] = 'p'


def capture(move):
    color, playmove = move
    if playmove[0].islower():
        capture_by_pawn(color, playmove[0] + playmove[-2:])
    else:
        #print(playmove[0])
        make_move((color, playmove[0] + playmove[-2:]))


def is_castling(move):
    return '-' in move[1]


def king_side_castling(color):
    if color == 'w':
        board[7][6] = 'K'
        board[7][4] = '_'
        board[7][5] = 'R'
        board[7][7] = '_'
    else:
        board[0][6] = 'k'
        board[0][4] = '_'
        board[0][5] = 'r'
        board[0][7] = '_'


def queen_side_castling(color):
    if color == 'w':
        board[7][2] = 'K'
        board[7][4] = '_'
        board[7][3] = 'R'
        board[7][0] = '_'
    else:
        board[0][2] = 'k'
        board[0][4] = '_'
        board[0][3] = 'r'
        board[0][0] = '_'


def make_castling_move(move):
    color, castlemove = move
    if len(castlemove.split('-')) == 2:
        king_side_castling(color)
    else:
        queen_side_castling(color)


def is_check(move):
    return '+' in move[1]


def check_move(move):
    color, pos = move
    if len(pos) == 5:
        make_move((color, pos[0] + pos[2:4]))
    else:
        make_move((color, pos[0:4]))


def is_promotion(move):
    return '=' in move[1]


def promotion_move(move):
    color = move[0]
    piece_after_promotion = move[1][:-1]
    if is_capture(move):
        pawn_prev_col = move[1][0]
        row = int(num_to_index[move[1][3]])
        col = int(alpha_to_index[move[1][2]])
        if color == 'w':
            board[row + 1][pawn_prev_col] = '_'
            board[row][col] = piece_after_promotion
        else:
            board[row - 1][pawn_prev_col] = '_'
            board[row][col] = piece_after_promotion.lower()

    else:
        row = int(num_to_index[move[1][1]])
        col = int(alpha_to_index[move[1][0]])
        if color == 'w':
            board[row + 1][col] = '_'
            board[row][col] = piece_after_promotion
        else:
            board[row - 1][col] = '_'
            board[row][col] = piece_after_promotion.lower()


def is_enpassant(move):
    pass


def make_enpassant(move):
    pass


def is_out_of_danger(move):
    return 'a' in move[1]


def out_of_danger_move(move):
    color, pos = move
    make_move((color, pos[0] + pos[2:]))


def play_game():
    decide_player()
    for i in range(len(set_of_moves) - 1):
        if i % 2 == 0:
            move = (PLAYER1, set_of_moves[i])
        else:
            move = (PLAYER2, set_of_moves[i])
        print(move)
        if is_enpassant(move):
            make_enpassant(move)
        elif is_pawn_move(move):
            make_pawn_move(move)
        elif is_castling(move):
            make_castling_move(move)
        elif is_check(move):
            check_move(move)
        elif is_promotion(move):
            promotion_move(move)
        elif is_capture(move):
            capture(move)
        elif is_out_of_danger(move):
            out_of_danger_move(move)
        else:
            make_move(move)
        board_view()

    decider = set_of_moves[-1]
    if '/' in decider:
        return "DRAW"
    elif decider[0] == '1':
        return "WHITE wins"
    elif decider[0] == '0':
        return "BLACK wins"
    else:
        return "Game in progress"


interpret_PGN()
print(set_of_moves)
print(play_game())
board_view()




