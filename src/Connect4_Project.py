#@staticmethod
def CreateCursorAndConnection():
    #global sql_host, sql_user, sql_password
    
    def check_db_exists():
        
        if mycon.is_connected() == False:
            print("Error in connection, please retry.")
            return False
        
        else:
            try:
                cursor.execute('use connect4;')
                print('Database exists. Using connect4')
        
            except:
                cursor.executemany('create database connect4;', 'use connect4;')
                print('Database doesn\'t exist. Creating and using connect4.')
            
            try:
                table_create = 'create table UserData(pName varchar(30) primary key, pPass varchar(30) not null, pTotal int default 0, pWins int default 0, pLosses int default 0, pDraws int default 0);'
                cursor.execute(table_create)
                cursor.commit()
                print('Table "UserData" successfully created!')
            
            except: #cursor.fetchone() == "ERROR 1050 (42S01): Table 'UserData' already exists":
                #cursor.rollback()
                print('Error while creating table. Table may already exist.')
                os.system('cls')

    try:
        mycon = SQL.connect(host = f'{sql_host}', user = f'{sql_user}', password = f'{sql_password}')
        cursor = mycon.cursor()
        check_db_exists()
        return cursor, mycon
       
    except: #SQL.Error as e:
        #print(e)
        print('Unexpected ERROR ecountered! \nPlease check system software for compatability.')
        time.sleep(1)
        return None, None

#@staticmethod
# inherit connection cursor_obj, connection_obj (mycon) from CreateCursor?
def CloseCursorAndConnection(cursor_obj, connection_obj):
    try:
        cursor_obj.close()
        connection_obj.close()
    except: pass

def SelectAllPlayerStats():
    cursor_obj, connection_obj = CreateCursorAndConnection()
    
    select_all_stats = "select pName as 'Player', pTotal as 'Games Played', pWins as 'Wins', pLosses as 'Losses', pDraws as 'Draws' from UserData order by pWins;"
    cursor_obj.execute(select_all_stats) 
    #count_row = 0
    
    for head in col_heads:
        if head == 'Total Games': print("| %12s"%head, "%2s"%end, end = '')
        else: print("| %8s"%head, "%6s"%end, end = '')
    print()

    for i in cursor_obj.fetchall():
        for col in i:
            print("| %7s"%col,"%7s"%end, end = '')
        #count_row += 1
        print()
    
    CloseCursorAndConnection(cursor_obj, connection_obj)

def SelectPlayerStats():
    cursor_obj, connection_obj = CreateCursorAndConnection()

    player = input("Enter Player Name: ")
    select_single_stats = f"select pName as 'Player', pTotal as 'Games Played', pWins as 'Wins', pLosses as 'Losses', pDraws as 'Draws' from UserData where pName = '{player}' order by pWins ;"
    cursor_obj.execute(select_single_stats) 
    
    for head in col_heads:
        if head == 'Total Games': print("| %12s"%head, "%2s"%end, end = '')
        else: print("| %8s"%head, "%6s"%end, end = '')
    print()
    
    i = cursor_obj.fetchone()
    for col in i:
        print("| %7s"%col,"%7s"%end, end = '')
    print()
    time.sleep(3)

    CloseCursorAndConnection(cursor_obj, connection_obj)

def RegisterPlayer():
    cursor_obj, connection_obj = CreateCursorAndConnection()

    while True:
        player = input("Enter Player Name: ")
        if bool(player) == False:
            print('Invalid Input. Please retry.')
            time.sleep(0.8)
            os.system('cls')
        else: break

    password = input("Enter Player Password: ")
    c_pass = input("Confirm Player Password: ")
    
    insert = f"insert into userdata(pName, pPass) values('{player}', '{password}');"
    
    if c_pass == password:
        try: 
            cursor_obj.execute(insert)
            connection_obj.commit()
            print('\nRegistration successful.')
        except: 
            connection_obj.rollback()
            print('\nError while registering. \nPlayer Name may already be registered. \nPlease retry with different Player Name.')

    CloseCursorAndConnection(cursor_obj, connection_obj)

def RemovePlayer():
    cursor_obj, connection_obj = CreateCursorAndConnection()

    player = input("Enter Player ID: ")
    password = input("Enter Player Password: ")
    c_pass = input("Confirm Player Password: ")

    delete = f"delete from userdata where pName = '{player}' and pPass = '{password}');"
    if c_pass == password:
        try: cursor_obj.execute(delete); connection_obj.commit(); print('Removal successful.')
        except: connection_obj.rollback(); print('Error while removing.')

    CloseCursorAndConnection(cursor_obj, connection_obj)

def PlayerLogin():
    global player1, player2

    cursor_obj, connection_obj = CreateCursorAndConnection()

    while True:
        player = input("Enter Player Name: ")
        if bool(player) == False:
            print('Invalid Input. Please retry.')
            time.sleep(0.8)
            os.system('cls')
        elif player == player1 or player == player2:
            print('Player is already logged in. Please Retry.')
            time.sleep(0.8)
            os.system('cls')
        else: break

    select_pPass = f"select pPass as 'Password' from UserData where pName = '{player}';"
    cursor_obj.execute(select_pPass)
    a = cursor_obj.fetchone()
    # print(a)
    if a and bool(a) == True: 
        password = input("Enter Player Password: ")
        
        if a[0] == password: 
            print('Login successful.')
            return player
        else: 
            print('Unsucessful login. Please retry.')
            return False
            #can close connection with CloseCursorAndConnection() and add recursive PlayerLogin(CreateCursorAndConnection()) here
    
    else: print('Player Name does not exist. Please Sign-In first.')
    
    CloseCursorAndConnection(cursor_obj, connection_obj)

def UpdatePlayerStats(win_player, loss_player, draw = False):
    cursor_obj, connection_obj = CreateCursorAndConnection()

    try:        
        if draw == True and win_player != loss_player:
            cursor_obj.execute(f"update userdata set pTotal = pTotal + 1, pDraws = pDraws + 1 where pName in ('{win_player}','{loss_player}');")
            print('Successfully updated data.')
        elif draw == False and win_player != loss_player:
            cursor_obj.execute(f"update userdata set pTotal = pTotal + 1, pWins = pWins + 1 where pName = '{win_player}';")
            cursor_obj.execute(f"update userdata set pTotal = pTotal + 1, pLosses = pLosses + 1 where pName = '{loss_player}';")
            print('Successfully updated data.')
        else: print('Error while updating data. Contact Admin for help.')

        connection_obj.commit()

    except: print('Error while updating data. Contact Admin for help.'); connection_obj.rollback()

    CloseCursorAndConnection(cursor_obj, connection_obj)

# imported the game from the same directory
def Connect4_2PlayerGame():

    """import random, sys, os, math, pickle as pi, time
    turn = random.randint(0,1)
    starter = turn
    move = 0
    move_list = []
    logs = open('move_logs.dat', 'wb')
    pi.dump(move_list, logs)
    logs.close()

    ROW_Count = 6 
    COL_Count = 7 
    Plot_What = 4 
    AI = 'O'
    Human = 'X'
    main_board = {}
    
    """
    def new_board(board):
        global COL_Count, ROW_Count
        # creating board using list composition code adapted to a dictonary. using STACK for each column.
        board = {i : [i if j==ROW_Count else '---' for j in range(ROW_Count+1)] for i in range(COL_Count)} 
        # "j if j==0 else" part is to check if row is printed straight
        return board
        #display() to check that the board came out correctly.

    def display():
        global main_board
        for i in range(ROW_Count+1): # i is for each row
            for j in range(COL_Count): # j for each column
                # access column key (j+1) and then print a particular row (i-1)
                # print last row first for proper looking board (board[j][-i-1])
                print('%7s'%main_board[j][-i-1], end = '\t')  
            print()
        print()

    def win_condition():
        global main_board, Human, AI, ROW_Count, COL_Count, Plot_What
        
        # vertical win condition:
        for i in range(ROW_Count-Plot_What+1):
            # using list slicing
            for j in range(COL_Count):
                # j signifies the column to enter, and i:i+4 is the list slice of 4 terms/moves
                # list slicing is upper-bound exclusive
                col = main_board[j][i:i+Plot_What]
                # check: print(col, 'row',i ,'col', j)
                if col.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
                elif col.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'
                

        # horizontal win condition:
        for i in range(ROW_Count):
            for j in range(COL_Count-Plot_What+1):
                row = [main_board[k][i] for k in range(j, j+Plot_What)]
                #check: row = [(board[k][i],f'row {i}, col {k}') for k in range(j, j+4)]
                #check: print(row)
                if row.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
                elif row.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'

                
        # diagonal win condition: 
        # positive slope diagonals
        up_diag = []
        for i in range(ROW_Count-Plot_What+1):
            for j in range(COL_Count-Plot_What+1):
                up_diag = []
                for k in range(Plot_What):
                    up_diag += [main_board[j+k][i+k]]
                
                # check: print(up_diag)            
                if up_diag.count(Human) == Plot_What: return f'Player 1 ({Human}) Wins!'
                elif up_diag.count(AI) == Plot_What: return f'Player 2 ({AI}) Wins!'

        # negative slope diagonals
        down_diag = []
        for i in range(Plot_What-1, ROW_Count):
            for j in range(COL_Count-Plot_What+1):
                down_diag = []
                for k in range(Plot_What):
                    down_diag += [main_board[j+k][i-k]]

                # check: print(down_diag)
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
        # this will find first empty spot in the column and play the move
        for i in range(ROW_Count):
            if board[move][i]=='---':
                board[move][i] = player
                break

    def check_legal():
        global COL_Count, turn, AI, AI, main_board
        
        move = ''
        while (len(move) == 0 or move == ''):
            move = input('Enter column of choice (integer from 0 to 6): ')
        # print(move, ord(move[0]), turn, len(move)) # check
        
        if ord(move[0])<48 or ord(move[0])>57 or len(move) == 0:
            # due to the limits of the ord function, max row and col is 9
            # doesnt work when move is given blank.
            chk_move = check_legal()
            return chk_move
        else:
            int_move = int(move)
            while int_move<0 or int_move>COL_Count-1 or main_board[int_move].count('---') == 0: # alternative to all_valid_loc       
                # so that the move doesn't give error (and stays within limits of dictionary)
                # .count('---') to check for full columns. '---' can later be replaced with " " <blank space>
                if int_move in range(7): print('Selected column is full')
                else: print('Column out of range.')
                move = check_legal()
                try:
                    int_move = int(move)
                    return int_move
                except:
                    print("Unexpected ERROR occured")
                    #turn+=1
                    #turn%=2
                    #recursion and pass also work # idk why tho
                    # Using recursion:
                    chk_move = check_legal()
                    return chk_move
                
            # print(int_move)
            return int_move
            
    def update(move_list, move):
        logs = open('move_logs.dat', 'rb')
        move_list = pi.load(logs)
        logs.close()
        # check: print('Past moves: ',move_list)
        move_list += [move]
        # check: print('Updated: ', move_list)
        with open('move_logs.dat', 'wb') as logs:
            pi.dump(move_list, logs)

    def undo(player, opp):
        global main_board, Human, AI, move_list, turn
        
        try:
            logs = open('move_logs.dat', 'rb')
            move_list = pi.load(logs)
            # check: print('loaded: ',move_list)
            logs.close()
        except: pass

        if len(move_list) <= 0:
            print('Cannot undo, board is empty.')
        else:
            del move_list[len(move_list)-1:]
            # check: print('reduced list: ', move_list)

            with open('move_logs.dat', 'wb') as logs:
                pi.dump(move_list, logs)

            main_board = new_board(main_board)

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

    def all_valid_loc(board):
        global COL_Count, ROW_Count
        
        valid_loc = []
        for col in range(COL_Count):
            if board[col].count('---') != 0:
                valid_loc += [col]

        return valid_loc
    
    global main_board, turn, starter, move, move_list, ROW_Count, COL_Count, Plot_What, AI, Human
    main_board = new_board(main_board)
    winner = win_condition()

    while not winner:
        menu = ' '
        try:
                logs = open('move_logs.dat', 'rb')
                move_list = pi.load(logs)
                # check: print('loaded: ',move_list)
                logs.close()
        except: pass
        
        menu = input('Enter:\n"QUIT" to exit.\n"UNDO" to undo last move\nClick the "Enter" key to continue with the game: ')
        os.system('cls')
        
        if menu.upper() == 'QUIT':
            time.sleep(5)
            print("GAME OVER")
            time.sleep(1)
            return 'Game ended with QUIT'

        elif menu.upper() == 'UNDO': #and opponent_choice == '1': 
            undo(Human, AI)
            display()
            time.sleep(1) 
            if len(move_list) >= 0: turn = (turn+1)%2
        
        else:
            try:
                if turn == 1:
                    print(f'Player 1\'s ({Human}\'s) turn.')
                    print()
                    display()
                    move = check_legal()
                    # print(move) # check
                    move_maker(main_board, move, Human)
                    update(move_list, move)
                    time.sleep(1.2)
                    os.system('cls')
                    
                elif turn == 0 and not win_condition():
                    
                    #if opponent_choice == '1':
                    print(f'Player 2\'s ({AI}\'s) turn.')
                    print()                    
                    display()
                    move = check_legal()
                    move_maker(main_board, move, AI)
                    update(move_list, move)
                    time.sleep(1.2)
                    os.system('cls')
              
            except: pass    
                    
            turn+=1
            turn%=2
            
            display()
            time.sleep(2)  

        if win_condition():
            print(win_condition())
            time.sleep(1)
            print("GAME OVER")
            return win_condition()
            time.sleep(1)
            break 

'''PlayerLogin(main_cursor, main_connection, 'p4', 'password')
UpdatePlayerStats(main_cursor, main_connection, 'p4', 'p1', draw = False)
UpdatePlayerStats(main_cursor, main_connection, 'p4', 'p3', draw = True)
SelectAllPlayerStats(main_cursor, main_connection)
CloseConnection(main_connection)'''

# Game variables and imports (along with sys, os and time)
import random, math, pickle as pi
turn = random.randint(0,1)
starter = turn
move = 0
move_list = []

logs = open('move_logs.dat', 'wb')
pi.dump(move_list, logs)
logs.close()

ROW_Count = 6 
COL_Count = 7 
Plot_What = 4 
AI = 'O'
Human = 'X'
main_board = {}

# Data Handling variables and imports.
import time, sys, os, mysql.connector as SQL #sqlite3 as SQL,
#print(dir(SQL))
#help(SQL)

end = '|'
cont = 'Y'
col_heads = ('Player', 'Total Games', 'Wins', 'Losses', 'Draws')
main_over = False
sub_over = False
sub_menu = 0
main_menu = 0
player1, player2 = '', ''

sql_host = input('Enter SQL Server Host name: ')
sql_user = input('Enter SQL Server Username: ')
sql_password = input('Enter SQL Server Password: ')

main_cursor, main_connection = CreateCursorAndConnection()
if (main_cursor, main_connection) == (None, None): cont = 'no'
else: CloseCursorAndConnection(main_cursor, main_connection)

while cont.upper() == 'Y':
    main_menu = input('MAIN MENU: \n1. Single Player \n2. Two Players \n3. Leaderboard \n4. Quit \n>>> ')
    
    if main_menu in ('1', '2', '3', '4'):
        time.sleep(1)
        os.system('cls')

        if main_menu == '1': #SINGLE PLAYER (both AI and Guest are there.)        
            import Connect4 as C4
            C4.main()

        elif main_menu == '2': #2 PLAYERS
            player1, player2 = '', ''

            while sub_menu not in ('1', '2', '3', '4', '5') or sub_over == False:
                time.sleep(0.5)
                os.system('cls')
                sub_menu = input('2 PLAYER MODE: \n1. Sign-up \n2. Log-in  \n3. Play \n4. Log-out \n5. Show Player Stats \n6. Exit to MAIN MENU \n>>> ')
                time.sleep(1.5)
                os.system('cls')

                if sub_menu == '1': #Registration
                    RegisterPlayer()
                    time.sleep(1)
                    continue

                elif sub_menu == '2': #Log-In
                    if bool(player1) == False:
                        player1 = PlayerLogin()

                    elif bool(player1) == True and bool(player2) == False:
                        player2 = PlayerLogin()
                        
                    else:
                        print('Two players already logged-in. Log-out of one account to log-in.')
                    
                    time.sleep(1)
                    continue
                
                elif sub_menu == '4': #Log-out
                    log_out_player = input('Enter Player Name: ')
                    
                    if log_out_player == player1:
                        player1 = ''
                        print(f'{log_out_player} successfully Logged-Out')
                    elif log_out_player == player2: 
                        player2 = ''
                        print(f'{log_out_player} successfully Logged-Out')
                    else:
                        print('Incorrect Player Name entered, please retry.')
                    
                    time.sleep(1.5)
                    continue
                
                elif (player1 == '' or player2 == '') and sub_menu == '3':
                    print('This option needs 2 players to be logged in. \nPlease Log-In and RETRY.')
                    time.sleep(0.5)

                elif sub_menu == '3' and (bool(player1) == bool(player2) == True) and player1 != player2: #2 PLAYER GAME
                    result = Connect4_2PlayerGame()

                    if result == 'Player 1 (X) Wins!':
                        UpdatePlayerStats(win_player = player1, loss_player = player2, draw = False)
                    
                    elif result == 'Player 2 (O) Wins!':
                        UpdatePlayerStats(win_player = player2, loss_player = player1, draw = False)
                    
                    elif result == 'It is a Draw!':
                        UpdatePlayerStats(win_player = player1, loss_player = player2, draw = True)
                    
                    elif result == 'Game ended with QUIT':
                        print('Someone QUIT the game!')
                    
                    else:
                        print('ERROR! The game ended unexpectedly.')
                    
                    time.sleep(2)
                    result = ''

                elif sub_menu == '5': #Single Playr Stats
                    SelectPlayerStats()
                    continue
                
                elif sub_menu == '6':
                    sub_over = True
                    break

                else:
                    print('Invalid input. Please RETRY.')

        elif main_menu == '3':
            SelectAllPlayerStats()
            
        elif main_menu == '4':
            time.sleep(2)
            sys.exit("GAME OVER")
            time.sleep(2)

    if main_menu in ('1', '2', '3', '4'):
        cont = input('\nPress "Y" to continue. Press any other key to exit. ')
    else: 
        cont = input('\nERROR in input. \nPress "Y" to retry. \nPress any other key to exit. \n> ')
    
    time.sleep(0.5)
    os.system('cls')
# End