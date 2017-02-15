from django.shortcuts import *
from django.http import *
from .models import User
from django.core.mail import *
from random import *

score_board_lis = []

# creating initial game board
board_matrix = [['em' for x in range(8)] for y in range(8)]
#notice the fact that every piece is made of 11 characters i'll use this in future
pice_val = {'wr': 'IMGs/wr.png', 'wk': 'IMGs/wk.png', 'wn': 'IMGs/wn.png', 'wp': 'IMGs/wp.png',
            'wq': 'IMGs/wq.png', 'bb': 'IMGs/bb.png', 'bk': 'IMGs/bk.png', 'bn': 'IMGs/bn.png',
            'bp': 'IMGs/bp.png', 'bq': 'IMGs/bq.png', 'br': 'IMGs/br.png', 'em': 'IMGs/em.gif',
            'wb': 'IMGs/wb.png'}

for i in range(8):
    board_matrix[6][i] = 'bp'
    board_matrix[1][i] = 'wp'
board_matrix[7] = ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']
board_matrix[0] = ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']

# converting board_matrix to icons address
for i in range(8):
    for j in range(8):
        board_matrix[i][j] = pice_val[board_matrix[i][j]]

def home_page(request):
    return render(request, "Chess/home.html")

def login_page(request):
    return render(request, "Chess/login.html")

def signup_page(request):
    return render(request, "Chess/signup.html")

def info_signup(request):
    same = User.objects.filter(username = request.POST['username'])
    if (not same):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if(password != password2):
            error = "Password And Repeat Password Fields Data Doesn't Match !"
            context = {'error1' : error}
            return render(request, 'Chess/signup.html', context)

        #generating activation key and save user
        key = randint(1000, 9999)

        # sending an email with activation key for user
        send_mail(
            'Activation key',
            'Hello dear ' + str(username) + '/nHere is your activation key:' + str(key),
            'mypythonaichess@gmail.com',
            [email],
            fail_silently = False,
        )
        user_board = change_board_to_string(board_matrix)
        score_board_lis.append([username, 0])

        #turn = True means that starting turn is with white
        user = User(username = username, email = email, password = password, activation_key = key, activation_status = 0,
                    user_board = user_board, user_score = 0, turn = True)

        user.save()

        context = {'user': user, 'board' : board_matrix}
        return render(request, 'Chess/activation.html', context)
    else:
        error = "This username has been taken already !"
        context = {'error': error}
        return render(request, 'Chess/signup.html', context)

def info_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.filter(username = username, password = password)

    if (user):
        user_1 = User.objects.get(username = username, password = password)

        # checking if the user's account is activated or not
        if (user_1.activation_status == 0):
            context = {'user' : user_1}
            return render(request, 'Chess/activation.html', context)
        else:
            user_board = change_string_to_board(user_1.user_board)
            context = {'user': user_1, 'board' : user_board}
            return render(request, 'Chess/info.html', context)
    else:
        error = "Wrong Username Or Password !"
        context = {'error': error}
        return render(request, 'Chess/login.html', context)

def activation(request):
    #getting username for the user recognization
    username = request.POST['username']
    user = User.objects.get(username = username)
    activation_key = request.POST['activation_key']
    activation_key = int(activation_key)

    #checking if the key enterd is corroct or not
    if (int(user.activation_key) == activation_key):
        user.activation_status = 1
        user.save()
        context = {'user' : user, 'board' :  board_matrix}
        return render(request, 'Chess/info.html', context)
    else:
        error = "WRONG CODE !!"
        context = {'error' : error, 'user' : user}
        return render(request, 'Chess/activation.html', context)

class bishop():
    def move(self, board, strt_x, strt_y, end_x, end_y):

        # if(board[end_x][end_y][6] == 'k'):
        #     return False
        dis = abs(strt_x - end_x)
        if(abs(strt_x - end_x) != abs(end_y - strt_y)):
            return False
        if(strt_x > end_x):
            if(strt_y > end_y):
                for i in range(1, dis):
                    if(board[end_x + i][end_y + i] != 'IMGs/em.gif'):
                        return False
            else:
                for i in range(1, dis):
                    if(board[end_x + i][end_y - i] != 'IMGs/em.gif'):
                        return False
        else:
            if(strt_y > end_y):
                for i in range(1, dis):
                    if(board[end_x - i][end_y + i] != 'IMGs/em.gif'):
                        return False
            else:
                for i in range(1, dis):
                    if(board[end_x - i][end_y - i] != 'IMGs/em.gif'):
                        return False
        return True

class knight():
    def move(self, board, strt_x, strt_y, end_x, end_y):
        dis_x = abs(strt_x - end_x)
        dis_y = abs(strt_y - end_y)
        if((dis_x == 1) and (dis_y == 2)):
            # if(board[end_x][end_y][6] == 'k'):
            #     return False
            return True
        if((dis_x == 2) and (dis_y == 1)):
            # if(board[end_x][end_y][6] == 'k'):
            #     return False
            return True
        return False

class king():
    def move(self, board, strt_x, strt_y, end_x, end_y):
        if(strt_x == end_x):
            if(abs(strt_y - end_y) != 1):
                return False
        if(strt_y == end_y):
            if(abs(strt_x - end_x) != 1):
                return False
        if((end_x != strt_x) and (strt_y != end_y)):
            if(abs(strt_y - end_y) + abs(strt_x - end_x) != 2):
                return False
        if(check(board, end_x, end_y, board[strt_x][strt_y][5])):
            return False
        return True

    def castling(self, board, strt_x, strt_y, end_x, end_y, user):
        if(strt_x != end_x):
            return False
        if(strt_y - end_y == 2):
            for i in range(1, strt_y):
                if(board[strt_x][i] != 'IMGs/em.gif'):
                    return False
                if(check(board, strt_x, i, board[strt_x][strt_y][5]) and (i != 1)):
                    return False
            if(check(board, strt_x, strt_y, board[strt_x][strt_y][5])):
                return False
            if(board[strt_x][strt_y][5] == 'w' and user.white_left_rook and user.white_king):
                return True
            if(board[strt_x][strt_y][5] == 'b' and user.black_left_rook and user.black_king):
                return True
            return False

        elif(end_y - strt_y == 2):
            for i in range(strt_y + 1, end_y + 1):
                if(board[strt_x][i] != 'IMGs/em.gif'):
                    return False
                if(check(board, strt_x, i, board[strt_x][strt_y][5])):
                    return False
            if(check(board, strt_x, strt_y, board[strt_x][strt_y][5])):
                return False
            if(board[strt_x][strt_y][5] == 'w' and user.white_king and user.white_right_rook):
                return True
            if(board[strt_x][strt_y][5] == 'b' and user.black_king and user.black_right_rook):
                return True
            return False
        return False

class queen():
    def move(self, board, strt_x, strt_y, end_x, end_y):
        # if(board[end_x][end_y][6] == 'k'):
        #     return False
        if(strt_y == end_y):
            if(strt_x > end_x):
                strt_x, end_x = end_x, strt_x
            for i in range(strt_x + 1, end_x):
                if(board[i][strt_y] != 'IMGs/em.gif'):
                    return False
            return True
        elif(strt_x == end_x):
            if(strt_y > end_y):
                strt_y, end_y = end_y, strt_y
            for i in range(strt_y + 1, end_y):
                if(board[strt_x][i] != 'IMGs/em.gif'):
                    return False
            return True

        if(abs(strt_x - end_x) != abs(strt_y - end_y)):
            return False

        dis = abs(strt_x - end_x)
        if(strt_x > end_x):
            if(strt_y > end_y):
                for i in range(1, dis):
                    if(board[end_x + i][end_y + i] != 'IMGs/em.gif'):
                        return False
            else:
                for i in range(1, dis):
                    if(board[end_x + i][end_y - i] != 'IMGs/em.gif'):
                        return False
        else:
            if(strt_y > end_y):
                for i in range(1, dis):
                    if(board[end_x - i][end_y + i] != 'IMGs/em.gif'):
                        return False
            else:
                for i in range(1, dis):
                    if(board[end_x - i][end_y - i] != 'IMGs/em.gif'):
                        return False
        return True

class pawn():
    def move(self, board, strt_x, strt_y, end_x, end_y, col):
        if(not col):
            if(strt_x == 6):
                if ((strt_x - end_x == 1) and (abs(strt_y - end_y) == 1)) :
                    if(board[end_x][end_y] != 'IMGs/em.gif'):
                        return True
                    else:
                        return False
                if((strt_y == end_y) and (strt_x - end_x <= 2) and ((strt_x - end_x) > 0)):
                    for i  in range(end_x, strt_x):
                        if(board[i][strt_y] != 'IMGs/em.gif'):
                            return False
                    return True
                return False
            else:
               if((strt_x - end_x == 1) and abs((strt_y - end_y) == 1)):
                   if(board[end_x][end_y] != 'IMGs/em.gif'):
                        return True
                   else:
                       return False
               if((strt_y == end_y) and (strt_x - end_x == 1) and (board[end_x][end_y] == 'IMGs/em.gif')):
                   return True
               else:
                   return False

        else:
            if(strt_x == 1):
                if((end_x - strt_x == 1) and (abs(strt_y - end_y) == 1)):
                    if(board[end_x][end_y] != 'IMGs/em.gif'):
                        return True
                    else:
                        return False
                if((strt_y == end_y) and (end_x - strt_x <= 2) and (end_x - strt_x > 0)):
                    for i in range(strt_x + 1, end_x + 1):
                        if(board[i][end_y] != 'IMGs/em.gif'):
                            return False
                    return True
            else:
                if((end_x - strt_x == 1) and (abs(strt_y - end_y) == 1)):
                    if(board[end_x][end_y] != 'IMGs/em.gif'):
                        return True
                    else:
                        return False
                if((end_x - strt_x == 1) and (strt_y == end_y) and (board[end_x][end_y] == 'IMGs/em.gif')):
                    return True
                else:
                    return False

class rook():
    def move(self, board, strtx, strty, endx, endy):
        # if(board[endx][endy][6] == 'k'):
        #     return False

        if((strty != endy) and (strtx != endx)):
            return False

        if(strtx != endx):
            if(strtx > endx):
                strtx, endx = endx, strtx
            for i in range(strtx + 1, endx):
                if(board[i][strty] != 'IMGs/em.gif'):
                    return False
        else:
            if(strty > endy):
                endy, strty = strty, endy
            for i in range(strty + 1, endy):
                if(board[strtx][i] != 'IMGs/em.gif'):
                    return False
        return True

def movement(request):
    move = request.POST['movement']
    username = request.POST['username']
    user = User.objects.get(username = username)
    user_board = change_string_to_board(user.user_board)
    turn  = user.turn

    #creating new game
    if(move[:7] == "NEWGAME"):
        user_board = change_board_to_string(board_matrix)
        context = {'board' : board_matrix, 'user' : user}
        user.user_board = user_board
        user.white_right_rook = True
        user.white_king = True
        user.white_left_rook = True
        user.black_left_rook = True
        user.black_right_rook = True
        user.black_king = True
        user.turn = True
        user.save()
        return render(request, 'Chess/info.html', context)

    if(move == 'bot'):
        move1 = AI(user_board)
        move_strt_row = move1[0]
        move_strt_col = move1[1]
        move_end_row = move1[2]
        move_end_col = move1[3]

    else:
        if ((len(move) < 5) or (len(move) > 5)):
            error = "Wrong Move Descripton !"
            context = {'board': user_board, 'error': error, 'user': user}
            return render(request, 'Chess/info.html', context)

        move_strt_col = ord(move[0]) - 97
        move_strt_row = ord(move[1]) - 49
        move_end_col = ord(move[3]) - 97
        move_end_row = ord(move[4]) - 49

        # checking if the move is valid or not
        # Wrong move input error
        if((move_end_col < 0) or (move_end_col > 7)):
            error = "WRONG MOVE INPUT !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

        if((move_strt_row < 0 ) or (move_strt_row > 7)):
            error = "WRONG MOVE INPUT !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

        if((move_strt_col < 0) or (move_strt_col > 7)):
            error = "WRONG MOVE INPUT !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

        if((move_end_row < 0) or (move_end_row > 7)):
            error = "WRONG MOVE INPUT !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

        if(move[:2] == move[3:5]):
            error = "WRONG MOVE INPUT !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    #Wrong turn Error
    if((user_board[move_strt_row][move_strt_col][5] == 'w') and (not turn)):
            error = "NOT YOUR TURN !"
            context = {'board' : user_board, 'error' : error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    if((user_board[move_strt_row][move_strt_col][5] == 'b') and turn):
        error = "NOT YOUR TURN !"
        context = {'board': user_board, 'error': error, 'user': user}
        return render(request, 'Chess/info.html', context)

    #Not a valid move for this piece
    if (user_board[move_strt_row][move_strt_col][5] == user_board[move_end_row][move_end_col][5]):
        error = "INVALID MOVE !"
        context = {'board': user_board, 'error': error, 'user': user}
        return render(request, 'Chess/info.html', context)

    if(user_board[move_strt_row][move_strt_col][6] == 'r'):
        if(not rook.move(rook, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col)):
            error = "INVALID MOVE !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    castling_flag = False
    if(user_board[move_strt_row][move_strt_col][6] == 'k'):
        if(not king.castling(king, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col, user)):
            if(not king.move(king, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col)):
                error = "INVALID MOVE !"
                context = {'board': user_board, 'error': error, 'user' : user}
                return render(request, 'Chess/info.html', context)
            if(check(user_board, move_end_row, move_end_col, user_board[move_strt_row][move_strt_col][5])):
                error = "INVALID MOVE !"
                context = {'board' : user_board, 'error' : error, 'user' : user}
                return render(request, 'Chess/info.html', context)
        else:
            castling_flag = True
        if(user_board[move_strt_row][move_strt_col][5] == 'b'):
            user.black_king = False
        else:
            user.white_king = False

    if(user_board[move_strt_row][move_strt_col][6] == 'p'):
        col = True
        if(user_board[move_strt_row][move_strt_col][5] == 'b'):
            col = False
        if(not pawn.move(pawn, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col, col)):
            error = "INVALID MOVE !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    if(user_board[move_strt_row][move_strt_col][6] == 'b'):
        if(not bishop.move(bishop, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col)):
            error = "INVALID MOVE !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    if(user_board[move_strt_row][move_strt_col][6] == 'q'):
        if(not queen.move(queen, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col)):
            error = "INVALID MOVE !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    if(user_board[move_strt_row][move_strt_col][6] == 'n'):
        if(not knight.move(knight, user_board, move_strt_row, move_strt_col, move_end_row, move_end_col)):
            error = "INVALID MOVE !"
            context = {'board': user_board, 'error': error, 'user' : user}
            return render(request, 'Chess/info.html', context)

    #changing turn
    turn = not turn

    #make the move
    strt_pic = user_board[move_strt_row][move_strt_col]
    end_pic = user_board[move_end_row][move_end_col]

    user_board[move_end_row][move_end_col] = user_board[move_strt_row][move_strt_col]
    user_board[move_strt_row][move_strt_col] = 'IMGs/em.gif'
    if(castling_flag):
        if(move_strt_col > move_end_col):
            user_board[move_strt_row][move_end_col + 1] = user_board[move_strt_row][0]
            user_board[move_strt_row][0] = 'IMGs/em.gif'
        else:
            user_board[move_strt_row][move_end_col - 1] = user_board[move_strt_row][7]
            user_board[move_strt_row][7] = 'IMGs/em.gif'

    other_king_x = 0
    other_king_y = 0
    self_king_x = 0
    self_king_y = 0
    for i in range(8):
        for j in range(8):
            if (user_board[move_end_row][move_end_col][5] != user_board[i][j][5]):
                if (user_board[i][j][6] == 'k'):
                    other_king_x = i
                    other_king_y = j
                    break
            if (user_board[move_end_row][move_end_col][5] == user_board[i][j][5]):
                if (user_board[i][j][6] == 'k'):
                    self_king_x = i
                    self_king_y = j

    if(tie_round(user_board, other_king_x, other_king_y)):
        error = "IT'S A TIE !"
        context = {'board' : user_board, 'user' : user, 'error' : error}
        user.user_board = change_board_to_string(board_matrix)
        user.white_king = True
        user.black_king = True
        user.turn = True
        user.white_left_rook = True
        user.white_right_rook = True
        user.black_left_rook = True
        user.black_right_rook = True
        user.save()
        return render(request, 'Chess/info.html', context)

    #if the king is check and move other piece and it stays check
    if(check(user_board, self_king_x, self_king_y, user_board[move_end_row][move_end_col][5])):
        error = 'Your King Is Check !'
        user_board[move_strt_row][move_strt_col] = strt_pic
        user_board[move_end_row][move_end_col] = end_pic
        context = {'board' : user_board, 'error' : error, 'user' : user}
        return render(request, 'Chess/info.html', context)

    #check-mate state
    # if (king.check_mate(king, user_board, other_king_x, other_king_y)):
    if(no_move_poss(user_board, user_board[other_king_x][other_king_y][5], other_king_x, other_king_y)):
        if (user_board[move_end_row][move_end_col][5] == 'b'):
            error = 'Black Is The Winner !!'
            context = {'board': user_board, 'error': error, 'user': user}
            return render(request, 'Chess/info.html', context)
        else:
            error = 'White Is The Winner !!'
            user.user_board = change_board_to_string(board_matrix)
            user.user_score += 1
            user.turn = True
            user.white_king = True
            user.white_right_rook = True
            user.white_left_rook = True
            user.black_left_rook = True
            user.black_right_rook = True
            user.black_king = True
            user.save()
            context = {'board': user_board, 'error': error, 'user': user}
            return render(request, 'Chess/info.html', context)

    if(user_board[move_end_row][move_end_col][6] == 'r'):
        if((move_strt_row == 0) and (move_strt_col == 0)):
            user.white_left_rook = False
        elif((move_strt_row == 0) and (move_strt_col == 7)):
            user.white_right_rook = False
        elif((move_strt_row == 7) and (move_strt_col == 0)):
            user.black_left_rook = False
        elif((move_strt_row == 7) and (move_strt_col == 7)):
            user.black_right_rook = False

    if(user_board[move_end_row][move_end_col][6] == 'p'):
        if((user_board[move_end_row][move_end_col][5] == 'w') and (move_end_row == 7)):
            user_board[move_end_row][move_end_col] = 'IMGs/wq.png'
        elif((user_board[move_end_row][move_end_col][5] == 'b') and (move_end_row == 0)):
            user_board[move_end_row][move_end_col] = 'IMGs/bq.png'

    context = {'board' : user_board, 'user' : user}
    user_board = change_board_to_string(user_board)
    user.user_board = user_board
    user.turn = turn
    user.save()

    return render(request, 'Chess/info.html', context)

def change_string_to_board(s):
    board = [['.' for y in range(8)] for x in range(8)]
    j = 0
    k = 0
    for i in range(0, 704 - 10, 11):
        board[k][j] = s[i : i + 11]
        j += 1
        if(j == 8):
            j = 0;
            k += 1;

    return board

def change_board_to_string(board):
    s = ''
    for i in range(8):
        for j in range(8):
            s += board[i][j]
    return s

#
#the global thing is the problem
#score_board has some serious problems
#
def score_board(request):
    global score_board_lis

    user = User.objects.get(username = request.POST['username'])
    s = ''
    for i in range(len(score_board_lis)):
        s += str(i)
    context = {'score_board' : score_board_lis, 's' : s, 'user' : user}
    return render(request, 'Chess/score_board.html', context)

def check(board, pos_x, pos_y, kingcol):
    for i in range(8):
        for j in range(8):
            if (board[i][j][5] != kingcol):
                if(board[i][j][6] == 'r'):
                    if(rook.move(rook, board, i, j, pos_x, pos_y)):
                        return True
                if(board[i][j][6] == 'p'):
                    col = False
                    if(kingcol == 'b'):
                        col = True
                    if(pawn.move(pawn, board, i, j, pos_x, pos_y, col)):
                        return True
                if(board[i][j][6] == 'q'):
                    if(queen.move(queen, board, i, j, pos_x, pos_y)):
                        return True
                if(board[i][j][6] == 'b'):
                    if(bishop.move(bishop, board, i, j, pos_x, pos_y)):
                        return True
                if(board[i][j][6] == 'n'):
                    if(knight.move(knight, board, i, j, pos_x, pos_y)):
                        return True
                if(board[i][j][6] == 'k'):
                    if(king.move(king, board, i, j, pos_x, pos_y)):
                        return True
    return False

def no_move_poss(board, col, king_x, king_y):
    for i in range(8):
        for j in range(8):
            for k in range(8):
                for l in range(8):
                    if((i, j) == (k, l)):
                        continue
                    if(board[i][j][5] == col):
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[i][j][6] == 'p'):
                            if(pawn.move(pawn, board, i, j, k, l, col)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, king_x, king_y, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return False

                        elif(board[i][j][6] == 'r'):
                            if(rook.move(rook, board, i, j, k, l)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, king_x, king_y, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return  False

                        elif(board[i][j][6] == 'q'):
                            if(queen.move(queen, board, i, j, k, l)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, king_x, king_y, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return False

                        elif(board[i][j][6] == 'b'):
                            if(bishop.move(bishop, board, i, j, k, l)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, king_x, king_y, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return False
                        elif(board[i][j][6] == 'n'):
                            if(knight.move(knight, board, i, j, k, l)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, king_x, king_y, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return False
                        elif(board[i][j][6] == 'k'):
                            if(king.move(king, board, i, j, k, l)):
                                board[k][l] = board[i][j]
                                board[i][j] = 'IMGs/em.gif'
                                if(check(board, k, l, col)):
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    continue
                                else:
                                    board[i][j] = strt_pic
                                    board[k][l] = end_pic
                                    return False

    return True

def tie_round(board, king_x, king_y):
    if(check(board, king_x, king_y, board[king_x][king_y][5])):
        return False
    if(no_move_poss(board, board[king_x][king_y][5], king_x, king_y)):
        return True
    else:
        return False

def AI(board):
    bk_x = 0
    bk_y = 0
    wk_x = 0
    wk_y = 0
    for i in range(8):
        for j in range(8):
            if(board[i][j][5:7] == 'bk'):
                bk_x = i
                bk_y = j
            if(board[i][j][5:7] == 'wk'):
                wk_x = i
                wk_y = j

    for i in range(8):
        for j in range(8):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] == 'w'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] == 'w'):
                            if (board[i][j][6] == 'n'):
                                if (knight.move(knight, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] == 'w'):
                            if (board[i][j][6] == 'b'):
                                if (bishop.move(bishop, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] == 'w'):
                            if (board[i][j][6] == 'r'):
                                if (rook.move(rook, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] == 'w'):
                            if (board[i][j][6] == 'q'):
                                if (queen.move(queen, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] == 'w'):
                            if (board[i][j][6] == 'k'):
                                if (king.move(king, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, k, l, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    #move the piece without hitting
    for i in range(5, 8):
        for j in range(3, 6):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(4, 8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'n'):
                                if (knight.move(knight, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'b'):
                                if (bishop.move(bishop, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(4):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'n'):
                                if (knight.move(knight, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(5):
        for j in range(3, 6):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(5):
        for j in range(3):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(5):
        for j in range(6, 8):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'r'):
                                if (rook.move(rook, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'q'):
                                if (queen.move(queen, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(8):
        for j in range(8):
            if (board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if ((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if (board[k][l][5] != 'b'):
                            if (board[i][j][6] == 'k'):
                                if (king.move(king, board, i, j, k, l)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if (not check(board, k, l, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(5, 8):
        for j in range(3):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic

    for i in range(5, 8):
        for j in range(6, 8):
            if(board[i][j][5] == 'b'):
                for k in range(8):
                    for l in range(8):
                        if((i, j) == (k, l)):
                            continue
                        strt_pic = board[i][j]
                        end_pic = board[k][l]
                        if(board[k][l][5] != 'b'):
                            if(board[i][j][6] == 'p'):
                                if(pawn.move(pawn, board, i, j, k, l, False)):
                                    board[k][l] = board[i][j]
                                    board[i][j] = 'IMGs/em.gif'
                                    if(not check(board, bk_x, bk_y, 'b')):
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
                                        return [i, j, k, l]
                                    else:
                                        board[k][l] = end_pic
                                        board[i][j] = strt_pic
