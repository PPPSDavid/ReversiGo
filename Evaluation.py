"""
The algorithum below is aiming at providing a 2-layer neural network based evaluation to the Reversi AI.
"""
import numpy as np
class EvaluationNetwork:

    def __init__ (self,x,y,c):
        """
        :param x: the input vector (all the board)
        :param y: the expected output vector, one dimensional, the win ratio
        :param c:the learning rate, 0.1-0.01
        """
        self.input = x
        self.weight_ih = np.random.rand(self.input.shape[1],100)
        self.weight_ho = np.random.rand(100,1)
        self.y = y
        self.output = np.zeros(y.shape)
        self.c = c

    def feed_forward(self):
        self.hidden_layer = sigmoid(np.dot(self.input,self.weight_ih))
        #Update the value of the hidden layer
        self.output = sigmoid(np.dot(self.hidden_layer,self.weight_ho))
        #Update the output layer value

    def backprop(self):
        d_weight_ho = np.dot(self.hidden_layer.T, (2*(self.y-self.output)*sigmoid_derivative(self.output)))
        d_weight_ih = np.dot(self.input.T, (np.dot(2*(self.y - self.output)* sigmoid_derivative(self.output) , self.weight_ho.T) \
                                            * sigmoid_derivative(self.hidden_layer)))
        #update the weight using gradiant decend

        self.weight_ih += self.c*d_weight_ih
        self.weight_ho += self.c*d_weight_ho

if __name__ == '__main__':
    test = EvaluationNetwork([1,1,1],0,0.1)
    test.feed_forward()
    print('{},{}'.format(test.outputtest.y))