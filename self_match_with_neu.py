"""
Todo: Integrate code and come up with a loop of training
"""
import GameCore as GM
import Evaluation
import time
import numpy

def self_match(neuralnetwork,output):
    time_1_total = 0
    time_2_total = 0
    time_1_max = 0
    time_2_max = 0

    board = GM.setBoard(8)
    test_1 = GM.getValidMove(board, 1)
    test_2 = GM.getValidMove(board, -1)
    while (len(test_1) != 0 or len(test_2) != 0):
        if len(test_1) != 0:
            time_1 = time.time()
            board = GM.makeMove(board, 1, GM.alpha_beta2(board, 1, 2,output,neuralnetwork))
            new_time = time.time() - time_1

            time_1_total = time_1_total + (new_time)
            if new_time > time_1_max:
                time_1_max = new_time
            test_1 = GM.getValidMove(board, 1)
            test_2 = GM.getValidMove(board, -1)
            #print('the following step is {}'.format(1))
            #GM.printBoard(board)

        if len(test_2) != 0:
            time_2 = time.time()
            board = GM.makeMove(board, -1, GM.alpha_beta2(board, -1, 2,output,neuralnetwork))
            new_time = time.time() - time_2
            time_2_total = time_2_total + (new_time)
            if new_time > time_2_max:
                time_2_max = new_time
            test_1 = GM.getValidMove(board, 1)
            test_2 = GM.getValidMove(board, -1)
            #print('the following step is {}'.format(-1))
            #GM.printBoard(board)
    return board

def self_match1(neuralnetworok,times):
    values = []
    time_1_total = 0
    time_2_total = 0
    time_1_max = 0
    time_2_max = 0

    for i in range(times):
        board = GM.setBoard(8)
        test_1 = GM.getValidMove(board, 1)
        test_2 = GM.getValidMove(board, -1)

        while (len(test_1) != 0 or len(test_2) != 0):
            if len(test_1) != 0:
                time_1 = time.time()
                board = GM.makeMove(board, 1, GM.alpha_beta2(board, 1, 2,[],neuralnetworok))
                new_time = time.time() - time_1

                time_1_total = time_1_total + (new_time)
                if new_time > time_1_max:
                    time_1_max = new_time
                test_1 = GM.getValidMove(board, 1)
                test_2 = GM.getValidMove(board, -1)
                print('the following step is {}'.format(1))
                GM.printBoard(board)

            if len(test_2) != 0:
                time_2 = time.time()
                board = GM.makeMove(board, -1, GM.alpha_beta1(board, -1, 2))
                new_time = time.time() - time_2

                time_2_total = time_2_total + (new_time)
                if new_time > time_2_max:
                    time_2_max = new_time
                test_1 = GM.getValidMove(board, 1)
                test_2 = GM.getValidMove(board, -1)
                print('the following step is {}'.format(-1))
                GM.printBoard(board)

        value = [GM.getBoardValue(board, 1), GM.getBoardValue(board, -1)]
        if value[0] > value[1]:
            value.append(1)
        else:
            value.append(-1)
        values.append(value)
    count = 0
    for k in values:
        if k[2] == 1:
            count += 1
    print('1 wins {}, -1 wins {}'.format(count, times - count))
    print('1 takes {} time, -1 takes {} times'.format(time_1_total / times / 32, time_2_total / times / 32))
    print('The maximum time for 1 is {}, and for -1 is {}.'.format(time_1_max, time_2_max))
if __name__ == '__main__':
    final_matrix = []
    c = Evaluation.NeuralNetwork(64,1,100,0.1)
    c.create_weight_matrices()
    c.get_weight_matrices()
    print('Training start!')
    data = []
    for i in range (30):
        print('training {} starts'.format(i))
        final_board = self_match(c, data)
        GM.printBoard(final_board)
        GM.training(final_board, data, c)
        print('training {} completed'.format(i))
        c.get_weight_matrices()
    for j in range (10):
        print('{}'.format(c.error_list[10*j]))
    final_matrix.append(c.weights_in_hidden)
    final_matrix.append(c.weights_hidden_out)
    text_file = open("Output.txt", "w")
    text_file.write('{}'.format(final_matrix))
    text_file.close()
    print('------------------------------------------')
    self_match1(c,1)