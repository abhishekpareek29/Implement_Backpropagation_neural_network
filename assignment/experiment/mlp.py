#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: mlp.py
# Author: Qian Ge <qge2@ncsu.edu>

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../')

import src.network2 as network2
import src.mnist_loader as loader
import src.activation as act

DATA_PATH = '../../data/'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store_true',
                        help='Check data loading.')
    parser.add_argument('--sigmoid', action='store_true',
                        help='Check implementation of sigmoid.')
    parser.add_argument('--gradient', action='store_true',
                        help='Gradient check')
    parser.add_argument('--train', action='store_true',
                        help='Train the model')
    parser.add_argument('--test', action='store_true',
                        help='Test the model')
    parser.add_argument('--train_with_tvd', action='store_true',
                        help='Train the model with train and valid data')

    return parser.parse_args()

def load_data():
    train_data, valid_data, test_data = loader.load_data_wrapper(DATA_PATH)
    print('Number of training: {}'.format(len(train_data[0])))
    print('Number of validation: {}'.format(len(valid_data[0])))
    print('Number of testing: {}'.format(len(test_data[0])))
    return train_data, valid_data, test_data

def test_sigmoid():
    z = np.arange(-10, 10, 0.1)
    y = act.sigmoid(z)
    y_p = act.sigmoid_prime(z)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(z, y)
    plt.title('sigmoid')

    plt.subplot(1, 2, 2)
    plt.plot(z, y_p)
    plt.title('derivative sigmoid')
    plt.show()

def gradient_check():
    train_data, valid_data, test_data = load_data()
    model = network2.Network([784, 20, 10])
    model.gradient_check(training_data=train_data, layer_id=1, unit_id=5, weight_id=3)

def test_model():
    # load train_data, valid_data, test_data.
    train_data, valid_data, test_data = load_data()
    # load the model.
    model = network2.load('../../sgd_model.json')
    accuracy = model.accuracy(test_data, convert=False)
    total_cost = model.total_cost(test_data, 0.0, convert=True)
    print('Accuracy: {}'.format(accuracy))
    print('Total Cost: {}'.format(total_cost))

def train_with_train_valid_data():
    # load train_data, valid_data, test_data
    train_data, valid_data, test_data = load_data()
    # Concat train and valid dataset
    train_valid_data = [[],[]]
    train_data[0].extend(valid_data[0])
    train_data[1].extend(valid_data[1])
#     train_valid_data.append(train_data[0] + valid_data[0])
#     train_valid_data.append(train_data[1] + valid_data[1])
    print(len(train_data[0]))
    print(len(train_data[1]))

    # construct the network
    model = network2.Network([784, 20, 10])
    # train the network using SGD
    model.SGD(
        training_data=train_data,
        epochs=20,
        mini_batch_size=128,
        eta=7e-3,
        lmbda = 0.0,
        evaluation_data=None,
        monitor_evaluation_cost=False,
        monitor_evaluation_accuracy=False,
        monitor_training_cost=True,
        monitor_training_accuracy=True)
    model.save('../../sgd_model_opt.json')

def main():
    # load train_data, valid_data, test_data
    train_data, valid_data, test_data = load_data()
    # construct the network
    model = network2.Network([784, 20, 10])
    # train the network using SGD
    epoch_size = 20
    ev_cost, ev_acc, train_cost, train_acc = model.SGD(
        training_data=train_data,
        epochs=epoch_size,
        mini_batch_size=128,
        eta=7e-3,
        lmbda = 0.0,
        evaluation_data=valid_data,
        monitor_evaluation_cost=True,
        monitor_evaluation_accuracy=True,
        monitor_training_cost=True,
        monitor_training_accuracy=True)

    model.save('../../sgd_model.json')

    z = np.arange(0, epoch_size, 1)
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.plot(z, train_cost)
    plt.title('train_cost')

    plt.subplot(2, 2, 2)
    plt.plot(z, train_acc)
    plt.title('train_acc')

    plt.subplot(2, 2, 3)
    plt.plot(z, ev_cost)
    plt.title('ev_cost')

    plt.subplot(2, 2, 4)
    plt.plot(z, ev_acc)
    plt.title('ev_acc')
    plt.show()

if __name__ == '__main__':
    FLAGS = get_args()
    if FLAGS.input:
        load_data()
    if FLAGS.sigmoid:
        test_sigmoid()
    if FLAGS.train:
        main()
    if FLAGS.gradient:
        gradient_check()
    if FLAGS.test:
        test_model()
    if FLAGS.train_with_tvd:
        train_with_train_valid_data()
