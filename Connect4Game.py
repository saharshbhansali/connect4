#This is the Code for the User-Defined Module

def new_board(board = {}):
    board = {i : [i if j==ROW_Count else '---' for j in range(ROW_Count+1)] for i in range(COL_Count)} 
    return board    

def display():
    global main_board
    for i in range(ROW_Count+1): 
        for j in range(COL_Count): 
            print('%7s'%main_board[j][-i-1], end = '\t')  
        print()
    print()

def win_condition():
    global main_board, Human, AI, ROW_Count, COL_Count, Plot_What    
    
    for i in range(ROW_Count-Plot_What+1):
        for j in range(COL_Count):
            col = main_board[j][i:i+Plot_What]
            if col.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
            elif col.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'
            
    for i in range(ROW_Count):
        for j in range(COL_Count-Plot_What+1):
            row = [main_board[k][i] for k in range(j, j+Plot_What)]
            if row.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
            elif row.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'            
    
    up_diag = []
    for i in range(ROW_Count-Plot_What+1):
        for j in range(COL_Count-Plot_What+1):
            up_diag = []
            for k in range(Plot_What):
                up_diag += [main_board[j+k][i+k]]            
                      
            if up_diag.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
            elif up_diag.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'
    
    down_diag = []
    for i in range(Plot_What-1, ROW_Count):
        for j in range(COL_Count-Plot_What+1):
            down_diag = []
            for k in range(Plot_What):
                down_diag += [main_board[j+k][i-k]]
            
            if down_diag.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
            elif down_diag.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'

    count = 0
    for i in main_board:
        count += main_board[i].count('---')
    if count==0:
        return 'It is a Draw!'

    return ''
                  
def move_maker(board, move, player):
    global ROW_Count
    for i in range(ROW_Count):
        if board[move][i]=='---':
            board[move][i] = player
            break

def check_legal():
    global COL_Count, turn, AI, AI, main_board
    
    move = ''
    while (len(move) == 0 or move == ''):
        move = input('Enter column of choice (integer from 0 to 6): ')
    
    
    if ord(move[0])<48 or ord(move[0])>57 or len(move) == 0:
        chk_move = check_legal()
        return chk_move
    
    else:
        int_move = int(move)
        while int_move<0 or int_move>COL_Count-1 or main_board[int_move].count('---') == 0:    
     
            if int_move in range(7): print('Selected column is full')
            else: print('Column out of range.')
            move = check_legal()
            try:
                int_move = int(move)
                return int_move
            except:
                print("Unexpected ERROR occured")
                chk_move = check_legal()
                return chk_move
        
        return int_move
        
def update(move_list, move):
    move_list += [move]
    
def undo(player, opp):
    global main_board, move_list, turn
    
    a = len(move_list)
    if a <= 0:
        print('Cannot undo, board is empty.')
    
    else:
        del move_list[a-1:]
        a -= 1
        main_board = new_board()

        for i in range(len(move_list)):
            m = move_list[i]
            if i%2==0:
                if starter == 1:
                    move_maker(main_board, m, 'X')
                else:
                    move_maker(main_board, m, 'O')
            else:
                if (starter+1)%2 == 1:
                    move_maker(main_board, m, 'X')
                else:
                    move_maker(main_board, m, 'O')
        turn = (turn+1)%2

def all_valid_loc(board):
    global COL_Count, ROW_Count
    
    valid_loc = []
    for col in range(COL_Count):
        if board[col].count('---') != 0:
            valid_loc += [col]

    return valid_loc

def eval_4(block, player, opp, score):
    global Plot_What

    if block.count(player) == Plot_What:
        score += 100
    elif block.count(player) == Plot_What-1 and block.count('---') == 1:
        score += 8
    elif block.count(player) == Plot_What-2 and block.count('---') == 2:
        score += 2
    elif block.count(opp) == Plot_What-1 and block.count('---') == 1:
        score -= 8.5
    elif block.count(opp) == Plot_What-1 and block.count('---') == 2:
        score-= 2.2
    elif block.count(opp) == Plot_What:
        score -= 100.2

    return score

def score_board(board, player):
    global Human, Human, AI, AI, ROW_Count, COL_Count, Plot_What 

    if player == AI:
        opp = Human
    elif player == Human:
        opp = AI

    score = 0    
    centre_col = [board[COL_Count//2][i:i+Plot_What] for i in range(ROW_Count)]
    centre_count = centre_col.count(player)
    score += (centre_count*5)
    opp_cen_count = centre_col.count(opp)
    score -= (opp_cen_count*3)    
    
    for i in range(ROW_Count):
        for j in range(COL_Count-Plot_What+1):
            row = [board[k][i] for k in range(j, j+Plot_What)]
            score = eval_4(row, player, opp, score)    
    
    for i in range(ROW_Count-Plot_What+1):        
        for j in range(COL_Count):
            col = board[j][i:i+Plot_What]
            score = eval_4(col, player, opp, score)
   
    up_diag = []
    for i in range(ROW_Count-Plot_What+1):
        for j in range(COL_Count-Plot_What+1):
            up_diag = []
            for k in range(Plot_What):
                up_diag += [board[j+k][i+k]]                      
            score = eval_4(up_diag, player, opp, score)
    
    
    down_diag = []
    for i in range(Plot_What-1, ROW_Count):
        for j in range(COL_Count-Plot_What+1):
            down_diag = []
            for k in range(Plot_What):
                down_diag += [board[j+k][i-k]]            
            score = eval_4(down_diag, player, opp, score)

    return score

def best_move(board, player):

    best_score = 0
    valid_loc = all_valid_loc(board)
    best_move = random.choice(valid_loc)
    temp_board = {}
    
    for col in valid_loc:
        temp_board = new_board(temp_board)
        for i in range(COL_Count):
            for j in range(ROW_Count):
                temp_board[i][j] = main_board[i][j]

        move_maker(temp_board, col, player)
        score = score_board(temp_board, player)
        
        if best_score < score:
            best_move = col
            best_score = score
        
    return best_move

def minimax(board, alpha, beta, depth, maximizingPlayer):
    global AI, Human, Human, AI
    
    winner = win_condition()

    
    copy_board = {}
    valid_loc = all_valid_loc(board)
    colmn = random.choice(valid_loc)

    if depth == 0 or bool(winner):
        if winner == AI:
            return ( None, 1000000000)
        elif winner == Human:
            return (None, -1000000000)
        elif str(winner) == 'True': 
            return (None, 0)
        elif depth == 0:
            return (colmn, score_board(board, AI))

    if maximizingPlayer:
        val = -math.inf
        
        for col in valid_loc:         
            
            copy_board = new_board(copy_board)        
            for i in range(COL_Count):
                for j in range(ROW_Count):
                    copy_board[i][j] = board[i][j]

            move_maker(copy_board, col, AI)            
            
            
            new_score = minimax(copy_board, alpha, beta, depth-1, False)[1]
            if new_score > val:
                val = new_score
                colmn = col
                
            alpha = max(alpha, val) 
            if alpha >= beta:
                break

        return (colmn, val)
    
    else: 
        val = math.inf
        
        for col in valid_loc:            
            copy_board = new_board(copy_board)
            
            for i in range(COL_Count):
                for j in range(ROW_Count):
                    copy_board[i][j] = board[i][j]
           
            move_maker(copy_board, col, Human)            
            
            new_score = minimax(copy_board, alpha, beta, depth-1, True)[1]
            if new_score < val:
                val = new_score
                colmn = col
                
            beta = min(beta, val) 
            if beta <= alpha:
                break

        return (colmn, val)

#------ MAIN PROGRAM of the Connect4 Module---------

import random, os, math, time 

turn = random.randint(0,1)
starter = turn
move = 0
move_list = []


ROW_Count = 6
COL_Count = 7 
Plot_What = 4 
AI = 'O'
Human = 'X'

main_board = new_board()
winner = win_condition()
opponent_choice = ''
diff = {'2':3, '3':5, '4':7}

def main():
    global opponent_choice, winner, main_board, AI, Human, ROW_Count, COL_Count, Plot_What, turn, starter, move, move_list, diff
    while opponent_choice not in ('1', '2', '3', '4'):
        opponent_choice = input("Choose opponent: \n1. Human \n2. AI (Easy) \n3. AI (Medium) \n4. AI (Hard)\n>>> ")

        if opponent_choice in diff:
            d1 = diff[opponent_choice]
            
        time.sleep(0.5)
        os.system('cls')

    while not winner:
        menu = ' ' 
       
        if opponent_choice in diff and turn == 0: pass
        else:
            menu = input('Enter:\n"QUIT" to exit.\n"UNDO" to undo last move\nClick the "Enter" key to continue with the game: ')
            os.system('cls')
        
        if menu.upper() == 'QUIT':
            time.sleep(5)
            print("GAME OVER")
            break

        elif menu.upper() == 'UNDO' and opponent_choice in diff and  starter == 0 and len(move_list) < 2:
            print('Cannot undo, AI going first.')

        elif menu.upper() == 'UNDO' and opponent_choice in diff: 
            undo(Human, AI)
            undo(AI, Human)
            display()
            time.sleep(1)

        elif menu.upper() == 'UNDO' and opponent_choice == '1': 
            undo(Human, AI)
            display()
            time.sleep(1)

        else:
            try:
                if turn == 1:
                    print(f'Player 1\'s ({Human}\'s) turn.')
                    print()
                    display()
                    move = check_legal()
                    move_maker(main_board, move, Human)
                    update(move_list, move)
                    time.sleep(1.2)
                    os.system('cls')
                    
                elif turn == 0 and not win_condition():
                    
                    if opponent_choice == '1':
                        print(f'Player 2\'s ({AI}\'s) turn.')
                        print()                    
                        display()
                        move = check_legal()
                        move_maker(main_board, move, AI)
                        update(move_list, move)
                        time.sleep(1.2)
                        os.system('cls')
                    
                    elif opponent_choice in diff: 
                        print(f'AI\'s ({AI}\'s) turn.')                    
                        move, algo_score = minimax(board = main_board, alpha = -math.inf, beta = math.inf, depth = d1, maximizingPlayer = True)
                        print('Move played:', move, '\n')
                        time.sleep(1.5)
                        os.system('cls')
                        move_maker(main_board, move, AI)
                        update(move_list, move)

                        
            except: pass    
                    
            turn+=1
            turn%=2
            
            display()
            time.sleep(2)  

        if win_condition():
            print(win_condition())
            time.sleep(5)
            print("GAME OVER")
            time.sleep(1)
            break
        
#main()

#==============================================================================================================================================================================================================================================================================

