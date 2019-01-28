"""
Todo: MTCR search tree + a better Neural network

Module needed:
numpy
scipy

"""
import random
import math

import Evaluation as Evl


# Initialize the board with all zeros except the middle
def setBoard(dimension):
    gameBoard = []
    for i in range(0, dimension):
        new_row = []
        for i in range(0, dimension):
            new_row.append(0)
        gameBoard.append(new_row)
    # Set the middle elements to the standard opening
    for i in range(int(dimension / 2 - 1), int(dimension / 2 + 1)):
        for j in range(int(dimension / 2 - 1), int(dimension / 2 + 1)):
            if (i + j) % 2 == 0:

                gameBoard[i][j] = 1

            else:
                gameBoard[i][j] = -1

    return(gameBoard)


def makeMove(gameBoard,color,position):
    dimension = len(gameBoard)

    # Vertical axis
    xAxis = position[0]
    # Horizontal axis(2nd loop)
    yAxis = position[1]
    gameBoardTemp = []

    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(gameBoard[i][j])
        gameBoardTemp.append(new_row)
    gameBoardTemp[xAxis][yAxis]=color

    # horizontal case
    for i in range(dimension):

        block = gameBoardTemp[xAxis][i]
        if (i==yAxis+1 or i==yAxis-1) and block == color:
            continue
        if block==color:
            isValid = True
            # see if there is zero entries between the two same color ones
            for j in range(min(i,yAxis)+1,max(i,yAxis)):
                if gameBoardTemp[xAxis][j]==0 or gameBoardTemp[xAxis][j]==color:
                    isValid = False
            if isValid:
                for j in range(min(i, yAxis), max(i, yAxis) + 1):
                    gameBoardTemp[xAxis][j]=color

    # vertical case
    for i in range(dimension):
        block = gameBoardTemp[i][yAxis]
        if (i==xAxis+1 or i==xAxis-1) and block == color:
            continue
        if block==color:
            isValid = True
            for j in range(min(i,xAxis)+1,max(i,xAxis)):
                if gameBoardTemp[j][yAxis]==0 or gameBoardTemp[j][yAxis]==color:
                    isValid = False
            if isValid:
                for j in range(min(i, xAxis), max(i, xAxis) + 1):
                    gameBoardTemp[j][yAxis]=color

    # diagonal cases: lower right(++) lower left(--) upper right(-+） upper left(--)
    for PoOrNeg in [1,-1]:
        for PoOrNeg2 in [1, -1]:
            for i in range(1,dimension):
                isValid = False
                if xAxis + PoOrNeg*i >= dimension or yAxis + PoOrNeg2*i >= dimension or xAxis + PoOrNeg*i < 0 or  yAxis + PoOrNeg2*i < 0:
                    break

                block = gameBoardTemp[xAxis + PoOrNeg*i][yAxis + PoOrNeg2*i]
                if block==0:
                    break
                if i==1 and block==color:
                    continue
                if block == color:

                    isValid = True
                for j in range(1,i):
                    if gameBoardTemp[xAxis + PoOrNeg*j][yAxis + PoOrNeg2*j]!=-color:
                        isValid = False
                if isValid:

                    for j in range(i):
                        gameBoardTemp[xAxis +  PoOrNeg*j][yAxis +  PoOrNeg2*j] = color

    compare_ = compare_board(gameBoard,gameBoardTemp)
    if compare_:
        return gameBoardTemp
    else:
        return gameBoard


# comparing whether any legal change has been made between two boards
def compare_board(board1, board2):
    dimension = len(board1)
    count = 0
    for i in range(dimension):
        for j in range(dimension):
            if board1[i][j]!=board2[i][j]:
                #print(count)
                count+=1
    if count<=1:
        return False
    else:
        return True


# Return the true false value to determine whether this is a valid move
def test_validity(gameBoard,color,position):
    dimension = len(gameBoard)
    if gameBoard[position[0]][position[1]]!=0:
        return False
    gameBoardTemp = []
    # horizontal cases
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(gameBoard[i][j])
        gameBoardTemp.append(new_row)
    gameBoard_after = makeMove(gameBoardTemp,color,position)

    if compare_board(gameBoard,gameBoard_after):
        return True
    else:
        return False


def getValidMove(gameBoard, color):
    good_moves = []
    dimension = range(len(gameBoard))
    for i in dimension:
        for j in dimension:
            if test_validity(gameBoard,color,[i,j]):
                #print('{},{}'.format(i,j))
                good_moves.append([i,j])
    return good_moves


def getBoardValue(board,color):
    count = 0
    for i in board:
        for j in i:
            if j == color:
                count+=1
    return count


def getBoard_eval_with_human(board,color):
    a=1
    b=1
    c=1
    final_eval = 0
    """The ratio of our disks and the opponent's disks, normalized, and adjusted through time."""
    NumOfOurs = getBoardValue(board,color)
    NumOfOppo = getBoardValue(board,-1*color)
    time_dependent_board_score = a*(1/(1+math.exp(-1*(NumOfOppo+NumOfOurs-len(board)*len(board)/2))))
    final_eval+=a*(time_dependent_board_score)*(NumOfOurs/(NumOfOurs+NumOfOppo))
    """The ratio of our mobility and the opponent's, adjusted through time."""
    Mobility_Your = len(getValidMove(board,color))
    Mobility_them = len(getValidMove(board, -1*color))
    final_eval+=c*(1-time_dependent_board_score)*(Mobility_Your/(Mobility_them+Mobility_Your))
    """The save spots we have, through time adjusted."""
    stable_Your = 0
    stable_Oppo = 0
    holder = 1
    for i in {0,7}:
        for j in {0,7}:
            if (board[i][j]==color):
                stable_Your+=1
                for k in range(1,8):
                    if(holder<=2):
                        if (board[i+k][j]==color):
                            stable_Your+=1
                        else:
                            break
                    else:
                        if (board[i - k][j] == color):
                            stable_Your += 1
                        else:
                            break
                    if (board[i + k*(-1)^(holder-1)][j] == color):
                        stable_Your += 1
                    else:
                        break
            elif(board[i][j]==-1*color):
                stable_Oppo+=1
                for k in range(1,8):
                    if(holder<=2):
                        if (board[i+k][j]==-1*color):
                            stable_Oppo+=1
                        else:
                            break
                    else:
                        if (board[i - k][j] == -1*color):
                            stable_Oppo += 1
                        else:
                            break
                    if (board[i + k*(-1)^(holder-1)][j] == -1*color):
                        stable_Oppo += 1
                    else:
                        break
            holder+=1
    if(stable_Your==0):
        final_eval-=c*(stable_Oppo)
    else:
        final_eval+=c*(stable_Your)
    return final_eval


def printBoard(gameBoard):
    # print the board for checking
    #Set horizontal Boundares
    print('The current game board:')
    print('-----------------------------------------------------')
    for i in range(len(gameBoard)):
        print('{:4d}'.format(i), end=" ")
    print()
    print('-----------------------------------------------------')

    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[i])+1):
            if j<len(gameBoard[i]):
                print('{:4d}'.format(gameBoard[i][j]), end=" ")
            else:
                print('---{}'.format(i))

    print('-----------------------------------------------------')


def random_step(board,step,start_color):
    for i in range(step):
        possible_step = getValidMove(board,start_color)
        board=makeMove(board,start_color,random.choice(possible_step))
        possible_step = getValidMove(board, -1*start_color)
        board = makeMove(board, -1*start_color, random.choice(possible_step))
    printBoard(board)
    return board

def min_max2(Board,color,depth):
    """Execution of the min-max search tree, fix the memory problem by recursion. Input being the board and color with a depth(<5 recommended)
    and output being the best choice """
    dimension = len(Board)
    boardTemp = []
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(Board[i][j])
        boardTemp.append(new_row)
    new_step_cashe = []
    possible_decisions = getValidMove(boardTemp, color)
    for j in possible_decisions:
        new_board = makeMove(boardTemp, color, j)
        new_step_cashe.append([new_board, j, 0])
    #print(new_step_cashe)
    for k in new_step_cashe:
        k[2]=min_max2con(k[0],-color,depth-1,color)
    best_value = 0
    best_path = []
    for k in new_step_cashe:
        #print(k[2])
        if k[2]>best_value:
            best_value=k[2]
            best_path=k[1]
        else:
            if k[2]==best_value:
                a = random.randint(1,101)
                if a >=25:
                    best_path = k[1]
    return(best_path)


def min_max2con(Board,color,depth,player_color):
    '''Complementing the main method, iterate all possibilites through recursion and the min-max decision tree.'''
    #print(color)
    #print(player_color)
    if depth == 0:
        #print('{}...{}'.format(0,getBoardValue(Board,player_color)))
        #Could be replaced by a better evaluation principle.
        return getBoardValue(Board,player_color)
    else:
        if color==player_color:
            val = -99999
            #create all the possible children from this game position
            children_nodes = []
            possible_moves = getValidMove(Board,color)
            for j in possible_moves:
                new_board= makeMove(Board,color,j)
                new_color = -1*color
                children_nodes.append([new_board,new_color,player_color])
            for child in children_nodes:
                if min_max2con(child[0],child[1],depth-1,player_color)>val:
                    val = min_max2con(child[0],child[1],depth-1,player_color)
            #print('{},{}...{}'.format(depth,val,'+'))
            return val
        else:
            val = 9999
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                if min_max2con(child[0], child[1], depth - 1, player_color) < val:
                    val = min_max2con(child[0], child[1], depth - 1, player_color)
            #print('{},{}...{}'.format(depth, val, '-'))
            return val


def alpha_beta1(Board,color,depth):
    dimension = len(Board)
    boardTemp = []
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(Board[i][j])
        boardTemp.append(new_row)
    new_step_cashe = []
    possible_decisions = getValidMove(boardTemp, color)
    for j in possible_decisions:
        new_board = makeMove(boardTemp, color, j)
        new_step_cashe.append([new_board, j, 0])
    #print(new_step_cashe)
    for k in new_step_cashe:
        #change this to change the method
        k[2] = alpha_beta1con(k[0],-color,depth-1,color,[-9999,99999])
    best_value = 0
    best_path = []
    for k in new_step_cashe:
        #print(k[1],end=",")
        if k[2] > best_value:
            best_value = k[2]
            best_path = k[1]
        else:
            if k[2] == best_value:
                a = random.randint(1, 101)
                if a >= 25:
                    best_path = k[1]
    #print()
    #print(best_path)
    return best_path


def alpha_beta1con(Board, color, depth,player_color,value_pair):
    '''Complementing the main method, iterate all possibilites through recursion and the min-max decision tree.'''
    # print(color)
    # print(player_color)
    #print('{}|||{}'.format(depth,value_pair))
    _min = value_pair[0]
    _max = value_pair[1]
    test = getValidMove(Board,color)
    if depth == 0 or len(test)==0:
        # print('{}...{}'.format(0,getBoardValue(Board,player_color)))
        # Could be replaced by a better evaluation principle.
        return getBoardValue(Board, player_color)
    else:
        if color == player_color:
            #the Max nodes
            val = _min
            # create all the possible children from this game position
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con(child[0], child[1], depth - 1, player_color,[val,_max])
                if temp > val:
                    val = temp
                #If a children of max node is higher than the max of its parent, Purning.
                if temp>_max:
                    #print('cut')
                    return _max

            # print('{},{}...{}'.format(depth,val,'+'))
            return val
        else:
            #a min node, which should cut if the children of such node has a lower value than min
            val = _max
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con(child[0], child[1], depth - 1, player_color,[_min,val])
                if temp < val:
                    val = temp
                if temp < _min:
                    #print('cut')
                    return _min
            # print('{},{}...{}'.format(depth, val, '-'))
            return val


def alpha_beta2(Board,color,depth,output,neuralnetwork):
    dimension = len(Board)
    boardTemp = []
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(Board[i][j])
        boardTemp.append(new_row)
    new_step_cashe = []
    possible_decisions = getValidMove(boardTemp, color)
    for j in possible_decisions:
        new_board = makeMove(boardTemp, color, j)
        new_step_cashe.append([new_board, j, 0])
    # print(new_step_cashe)
    for k in new_step_cashe:
        # change this to change the method
        k[2] = alpha_beta1con2(k[0], -color, depth - 1, color, [-9999, 99999],neuralnetwork)
    best_value = 0
    best_path = []
    for k in new_step_cashe:
        # print(k[1],end=",")
        if k[2] > best_value:
            best_value = k[2]
            best_path = k[1]
        else:
            if k[2] == best_value:
                a = random.randint(1, 101)
                if a >= 25:
                    best_path = k[1]
    # print()
    # print(best_path)
    #If the color is equal to the final winning one, set to 1, otherwise set to 0
    output.append([Board,0,color])
    return best_path


def alpha_beta1con2(Board, color, depth,player_color,value_pair,neuralnetwork):
    '''Complementing the main method, iterate all possibilites through recursion and the min-max decision tree.'''
    # print(color)
    # print(player_color)
    #print('{}|||{}'.format(depth,value_pair))
    _min = value_pair[0]
    _max = value_pair[1]
    test = getValidMove(Board,color)
    if depth == 0 or len(test)==0:
        # print('{}...{}'.format(0,getBoardValue(Board,player_color)))
        # Could be replaced by a better evaluation principle.
        return eval(Board,player_color,neuralnetwork)
    else:
        if color == player_color:
            #the Max nodes
            val = _min
            # create all the possible children from this game position
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con(child[0], child[1], depth - 1, player_color,[val,_max])
                if temp > val:
                    val = temp
                #If a children of max node is higher than the max of its parent, Purning.
                if temp>_max:
                    #print('cut')
                    return _max

            # print('{},{}...{}'.format(depth,val,'+'))
            return val
        else:
            #a min node, which should cut if the children of such node has a lower value than min
            val = _max
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con(child[0], child[1], depth - 1, player_color,[_min,val])
                if temp < val:
                    val = temp
                if temp < _min:
                    #print('cut')
                    return _min
            # print('{},{}...{}'.format(depth, val, '-'))
            return val


def eval(Board,color,neural_network):
    '''
    A component of the new evaluation method based on renforcement learning, takes the current board situation and returns a probability of winning
    for player 'color'.
    Always predict the win percentage of 1, if color is -1, then return 1-x
    '''
    #Initialize the input vector
    input_vec = []
    for i in Board:
        for j in i:
            input_vec.append(j)
    #initialize the neural network and get result
    output = neural_network.run(input_vec)
    #compare to see which color is to be predicted
    if color == 1:
        return output
    else:
        return 1-output


def training(board,output,neuralnetwork):
    #Initialze the training samples
    if(getBoardValue(board,1)>getBoardValue(board,-1)):
        for i in output:
            if i[2]==1:
                i[1]=[1]
            else:
                i[1]=[0]
    else:
        for i in output:
            if i[2] == -1:
                i[1] = [1]
            else:
                i[1]=[0]
    print(output)
    #start training
    for i in output:
        input_vec = []
        for m in i[0]:
            for n in m:
                input_vec.append(n)
        neuralnetwork.train(input_vec,i[1])
    #return the new neural network
    return neuralnetwork


def alpha_beta_with_human(Board,color,depth):
    dimension = len(Board)
    boardTemp = []
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(Board[i][j])
        boardTemp.append(new_row)
    new_step_cashe = []
    possible_decisions = getValidMove(boardTemp, color)
    for j in possible_decisions:
        new_board = makeMove(boardTemp, color, j)
        new_step_cashe.append([new_board, j, 0])
    #print(new_step_cashe)
    for k in new_step_cashe:
        #change this to change the method
        k[2] = alpha_beta1con_with_human(k[0],-color,depth-1,color,[-9999,99999])
    best_value = 0
    best_path = []
    for k in new_step_cashe:
        #print(k[1],end=",")
        if k[2] > best_value:
            best_value = k[2]
            best_path = k[1]
        else:
            if k[2] == best_value:
                a = random.randint(1, 101)
                if a >= 25:
                    best_path = k[1]
    #print()
    #print(best_path)
    return best_path


def alpha_beta1con_with_human(Board, color, depth,player_color,value_pair):
    '''Complementing the main method, iterate all possibilites through recursion and the min-max decision tree.'''
    # print(color)
    # print(player_color)
    #print('{}|||{}'.format(depth,value_pair))
    _min = value_pair[0]
    _max = value_pair[1]
    test = getValidMove(Board,color)
    if depth == 0 or len(test)==0:
        # print('{}...{}'.format(0,getBoardValue(Board,player_color)))
        # Could be replaced by a better evaluation principle.
        return getBoardValue(Board, player_color)
    else:
        if color == player_color:
            #the Max nodes
            val = _min
            # create all the possible children from this game position
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con_with_human(child[0], child[1], depth - 1, player_color,[val,_max])
                if temp > val:
                    val = temp
                #If a children of max node is higher than the max of its parent, Purning.
                if temp>_max:
                    #print('cut')
                    return _max

            # print('{},{}...{}'.format(depth,val,'+'))
            return val
        else:
            #a min node, which should cut if the children of such node has a lower value than min
            val = _max
            children_nodes = []
            possible_moves = getValidMove(Board, color)
            for j in possible_moves:
                new_board = makeMove(Board, color, j)
                new_color = -1 * color
                children_nodes.append([new_board, new_color, player_color])
            for child in children_nodes:
                temp = alpha_beta1con_with_human(child[0], child[1], depth - 1, player_color,[_min,val])
                if temp < val:
                    val = temp
                if temp < _min:
                    #print('cut')
                    return _min
            # print('{},{}...{}'.format(depth, val, '-'))
            return val



# test case
if __name__ == '__main__':
    Board = setBoard(8)
    printBoard(Board)
    Board = makeMove(Board, 1, [4, 2])
    printBoard(Board)
    Board = makeMove(Board, -1, [5, 2])
    Board = makeMove(Board, 1, [6, 2])
    printBoard(Board)
    print(getValidMove(Board,-1))
    Board = makeMove(Board, -1, [6, 1])
    Board = makeMove(Board, 1, [6, 0])
    Board = makeMove(Board, -1, [7, 0])
    printBoard(Board)
    num = getBoard_eval_with_human(Board,1)
    num_2 = getBoard_eval_with_human(Board,-1)
    print(num)
    print(num_2)

    


