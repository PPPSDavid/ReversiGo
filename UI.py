"""
Version: 1.0
Implementing type: Print statement
1. Setup game according to user input
2. choose between match among two people and with AI
3. choose AI difficulties
4. See hints/ possible moves, see real-time evaluation of board

"""

import GameCore as GM
import sys

def make_move(type,color,gameboard,depth):
    if type == 1:
        dim1 = input('please print the first dimension')
        dim2 = input('please print the second dimension')
        return GM.makeMove(gameboard,color,[dim1,dim2])
    else:
        if type==2:
            return GM.makeMove(gameboard, color, GM.min_max2(gameboard,color,depth))
        if type==3:
            return GM.makeMove(gameboard, color, GM.alpha_beta1(gameboard, color, depth))



while True:
    # setup the game
    print('Welcome to the Reversi Game! press 1 to start, press any other int to quit.')
    try:
        commmand = int(input('please choose.'))
    except ValueError:
        print('This is not a proper input')
        continue
    if commmand == 0:
        break

    try:
        board_size = int(input('please indecate the board size (defult 8):'))
    except ValueError:
        print('This is not a proper input')
        continue
    gameboard = GM.setBoard(board_size)
    print('setting up the gameboard...')
    GM.printBoard(gameboard)

    print('please indecate the game type: 1 for pvp, 2 for pve, 3 for eve')
    try:
        game_type = int(input('please choose.'))
    except ValueError:
        print('This is not a proper input')
        continue
    if game_type==3:
        #eve
        print('EvE selected, please choose the algorithum for player 1')
        ai_type1 = int(input('3 for AB, 2 for min max.'))
        search_depth1 =int(input('please indecate the desired search depth'))
        print('please choose the algorithum for player 2')
        ai_type2 = int(input('3 for AB, 2 for min max.'))
        search_depth2 = int(input('please indecate the desired search depth'))
        print('----------------------------------------------------')
        print('GAME START')
        test_1 = GM.getValidMove(gameboard, 1)
        test_2 = GM.getValidMove(gameboard, -1)
        while (len(test_1) != 0 or len(test_2) != 0):
            if len(test_1) != 0:
                gameboard = make_move(ai_type1,1,gameboard,search_depth1)
                test_1 = GM.getValidMove(gameboard, 1)
                test_2 = GM.getValidMove(gameboard, -1)
                print('The following step is {}'.format(1))
                GM.printBoard(gameboard)
                input('press any key to see next step')

            if len(test_2) != 0:

                gameboard = make_move(ai_type2,-1,gameboard,search_depth2)
                test_1 = GM.getValidMove(gameboard, 1)
                test_2 = GM.getValidMove(gameboard, -1)
                print('The following step is {}'.format(-1))
                GM.printBoard(gameboard)
                input('press any key to see next step')
    if GM.getBoardValue(gameboard,1)>GM.getBoardValue(gameboard,-1):
        print('1 Wins by {}'.format(GM.getBoardValue(gameboard,1)-GM.getBoardValue(gameboard,-1)))
    else:
        print('-1 Wins by {}'.format(-GM.getBoardValue(gameboard, 1) + GM.getBoardValue(gameboard, -1)))