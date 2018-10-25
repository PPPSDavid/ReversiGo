import random
import time
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
    #Vertical axis
    xAxis = position[0]
    #Horizontal axis(2nd loop)
    yAxis = position[1]
    gameBoardTemp = []
    #horizontal cases
    for i in range(dimension):
        new_row = []
        for j in range(dimension):
            new_row.append(gameBoard[i][j])
        gameBoardTemp.append(new_row)
    gameBoardTemp[xAxis][yAxis]=color


#horizontal case

    for i in range(dimension):

        block = gameBoardTemp[xAxis][i]
        if (i==yAxis+1 or i==yAxis-1) and block == color:
            continue
        if block==color:
            isValid = True
            #see if there is zero entries between the two same color ones
            for j in range(min(i,yAxis)+1,max(i,yAxis)):
                if gameBoardTemp[xAxis][j]==0 or gameBoardTemp[xAxis][j]==color:
                    isValid = False
            if isValid:
                for j in range(min(i, yAxis), max(i, yAxis) + 1):
                    gameBoardTemp[xAxis][j]=color


#vertical case

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



#disgenal cases: lower right(++) lower left(--) upper right(-+） upper left(--)
    for PoOrNeg in [1,-1]:
        for PoOrNeg2 in [1, -1]:
            for i in range(1,dimension):
                isValid = False
                if xAxis + PoOrNeg*i >= dimension or yAxis + PoOrNeg2*i >= dimension or xAxis + PoOrNeg*i < 0 or  yAxis + PoOrNeg*i < 0:
                    break
                #print("{},{},{}".format(PoOrNeg, PoOrNeg2, i))
                block = gameBoardTemp[xAxis + PoOrNeg*i][yAxis + PoOrNeg2*i]
                if block==0:
                    break
                if i==1 and block==color:
                    continue
                if block == color:
                    #print("{},{},{}1".format(PoOrNeg, PoOrNeg2, i))
                    isValid = True
                for j in range(1,i):
                    if gameBoardTemp[xAxis + PoOrNeg*j][yAxis + PoOrNeg2*j]!=-color:
                        isValid = False
                if isValid:
                    #print("{},{},{},2".format(PoOrNeg,PoOrNeg2,i))
                    for j in range(i):
                        gameBoardTemp[xAxis +  PoOrNeg*j][yAxis +  PoOrNeg2*j] = color
    #print('{},{}!'.format(gameBoard[3][2],gameBoardTemp[3][2]))

    compare_ = compare_board(gameBoard,gameBoardTemp)
    if compare_:
        return gameBoardTemp
    else:
        return gameBoard
#comparing whether any legal change has been made between two boards
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

#Return the true false value to determine whether this is a valid move
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

def random_match(board,step,start_color):
    for i in range(step):
        possible_step = getValidMove(board,start_color)
        board=makeMove(board,start_color,random.choice(possible_step))
        possible_step = getValidMove(board, -1*start_color)
        board = makeMove(board, -1*start_color, random.choice(possible_step))
    printBoard(board)
    return board

#Simple min-max search with a changable depth
def min_max_search1(board,color,depth=7):
    dimension = len(board)
    cashe = []


    #major loop that covers depth times of search
    for i in range(depth):
        if i==0:
            # initialize a list to store all possible board after one step
            boardTemp = []
            for i in range(dimension):
                new_row = []
                for j in range(dimension):
                    new_row.append(board[i][j])
                boardTemp.append(new_row)
            new_step_cashe = []
            possible_decisions = getValidMove(boardTemp, color)
            for j in possible_decisions:
                new_board = makeMove(boardTemp, color, j)
                new_value = getBoardValue(new_board, color)
                new_step_cashe.append([new_board, [j], new_value])
            cashe.append(new_step_cashe)



        else:

            #expand the tree from each node

            new_step_cashe=[]

            for board_from_last_move in range(len(cashe[i-1])):
                if color == 1:
                    if i % 2 == 1:
                        color = -1
                    else:
                        color = 1
                else:
                    if i % 2 == 1:
                        color = 1
                    else:
                        color = -1

                #print('{}'.format(board_from_last_move))
                possible_decisions = getValidMove(cashe[i-1][board_from_last_move][0],color)
                #print(possible_decisions)
                #print(possible_decisions)
                #print('{}'.format(possible_decisions))
                for j in possible_decisions:
                    new_board = makeMove(cashe[i-1][board_from_last_move][0], color, j)
                    #if i == depth-1:
                        #printBoard(new_board)
                    new_value = getBoardValue(new_board, color)
                    preious_path = cashe[i - 1][board_from_last_move][1]
                    path_copy = []
                    length_pre = len(preious_path)
                    for k in range(length_pre):
                        path_copy.append(preious_path[k])

                    path_copy.append(j)
                    #if i == depth - 1:
                        #print('{},{}'.format(path_copy,new_value))
                    new_step_cashe.append([new_board, path_copy, new_value])

            cashe.append(new_step_cashe)
    #find the best choice based on the final step's expected value

    print('!!!!!!!!!!!!!!!!!!!!!!!!!')
    path = []
    value = []
    dimension = len(cashe[depth-1])
    for i in range(dimension):
        path.append(cashe[depth-1][i][1])
        value.append(cashe[depth-1][i][2])
    comparasion = [0,0]
    sum = 0
    count = 0
    result = []
    for i in range(dimension):
        #print(path[i][0])
        if path[i][0][0]==comparasion[0]and path[i][0][1]==comparasion[1]:
            sum=sum+value[i]
            count+=1
        else:
            #print(sum)
            #print(count)
            if count!=0:
                result.append([path[i-1][0],(sum)/count])
            comparasion=path[i][0]
            #print('aa')
            #print(comparasion)
            count = 1
            sum = value[i]
    result.append([path[i-1][0],sum/count])
    print(result)


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
    print(new_step_cashe)
    for k in new_step_cashe:
        k[2]=min_max2con(k[0],-color,depth-1,color)
    best_value = 0
    best_path = []
    for k in new_step_cashe:
        print(k[2])
        if k[2]>best_value:
            best_value=k[2]
            best_path=k[1]
        else:
            if k[2]==best_value:
                a = random.randint(1,101)
                if a >=25:
                    best_path = k[1]
    print(best_path)





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


#test case
if __name__ == '__main__':
    Board = setBoard(8)
    printBoard(Board)
    Board = makeMove(Board, 1, [4, 2])
    #printBoard(Board)
    #Board = makeMove(Board, -1, [3, 2])
    printBoard(Board)
    Board = makeMove(Board, -1, [5, 2])
    printBoard(Board)
    
    #Board = makeMove(Board, 1, [2, 2])
    #printBoard(Board)
    #temp = test_validity(Board,1,[2,2])
    #print('{}'.format(temp))
    #printBoard(Board)
    #test = getValidMove(Board,1)
    #print('{}'.format(test))
    #printBoard(Board)
    #x = getBoardValue(Board,-1)
    #printBoard(Board)
    #print(x)
    #y = makeMove(Board,1,[2,2])
    #printBoard(y)
    #printBoard(Board)

    


