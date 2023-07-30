import numpy as np
import pygame
import math


def normalize_data(data):
    return (data - data.min()) / (data.max() - data.min())


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        pass

    def backward(self, output_gradient, learning_rate):
        pass


class Dense(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    def backward(self, output_gradient, learning_rate):
        input_error = np.dot(self.weights.T, output_gradient)
        weights_gradient = np.dot(output_gradient, self.input.T)
        self.weights -= weights_gradient * learning_rate
        self.bias -= output_gradient * learning_rate
        return input_error


class Activation(Layer):
    def __init__(self, activation, activation_prime):
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input):
        self.input = input
        return self.activation(self.input)

    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient, self.activation_prime(self.input))


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x) ** 2


def reLu(x):
    return (x > 0) * x


def reLu_prime(x):
    return x > 0


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))


def mse(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / np.size(y_true)


class NeuralNetwork:
    def __init__(self, sizes, activation_function, activation_function_prime):
        self.layers = []
        for index, size in enumerate(sizes):
            if index != len(sizes) - 1:
                self.layers.append(Dense(sizes[index], sizes[index + 1]))
                self.layers.append(Activation(activation_function, activation_function_prime))

    def predict(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def train(self, input, actual, learning_rate):
        output = self.predict(input)
        weights_gradient = mse_prime(actual, output)
        for layer in reversed(self.layers):
            weights_gradient = layer.backward(weights_gradient, learning_rate)
        return mse(actual, output)


def draw_network(network, s, position, green, red, spacing_x=50, spacing_y=20):
    x, y, z = 0, 0, 0
    layers = []
    for lay in network.layers:
        if type(lay) == Dense:
            layers.append(lay)

    for lay in layers:
        for next_node in range(len(lay.weights[0])):
            for weight in lay.weights:
                start_pos = x * spacing_x + position[0], (y - len(layers[x].weights[0]) / 2) * spacing_y + position[1]
                end_pos = (x + 1) * spacing_x + position[0], (z - len(layers[x].weights) / 2) * spacing_y + position[1]
                if weight[y] > 0:
                    pygame.draw.line(s, green, start_pos, end_pos, math.ceil(weight[y]))
                else:
                    pygame.draw.line(s, red, start_pos, end_pos, math.floor(weight[y]))
                z += 1
            y += 1
            z = 0
        w = 0
        for bias in lay.bias:
            if bias > 0:
                pygame.draw.circle(s, green, ((x + 1) * spacing_x + position[0], (w - len(layers[x].weights) / 2) * spacing_y + position[1]), math.ceil(bias[0]) * 2)
            else:
                pygame.draw.circle(s, red, ((x + 1) * spacing_x + position[0], (w - len(layers[x].weights) / 2) * spacing_y + position[1]), math.floor(bias[0]) * -2)
            w += 1
        x += 1
        y = 0


nn = NeuralNetwork([2, 3, 3, 1], tanh, tanh_prime)
