"""
Todo: Integrate code and come up with a loop of training
"""
import GameCore as GM
import Evaluation
import time

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
            print('the following step is {}'.format(1))
            GM.printBoard(board)

        if len(test_2) != 0:
            time_2 = time.time()
            board = GM.makeMove(board, -1, GM.alpha_beta2(board, -1, 2,output,neuralnetwork))
            new_time = time.time() - time_2
            time_2_total = time_2_total + (new_time)
            if new_time > time_2_max:
                time_2_max = new_time
            test_1 = GM.getValidMove(board, 1)
            test_2 = GM.getValidMove(board, -1)
            print('the following step is {}'.format(-1))
            GM.printBoard(board)
    return board

if __name__ == '__main__':
    c = Evaluation.NeuralNetwork(64,1,100,0.1)
    c.create_weight_matrices()
    data = []
    final_board = self_match(c,data)
    GM.printBoard(final_board)
    print(data)
    GM.training(final_board,data,c)
    final_board = self_match(c, data)
    GM.printBoard(final_board)
    print(data)
