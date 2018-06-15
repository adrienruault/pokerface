import os
import sys

import tensorflow as tf

from DataLoader import DataLoader
from trainers.Trainer import Trainer
from models.LSTM_dropout import Model

from utils.dirs import create_dirs, set_up_experience






def main():

    config = set_up_experience('configs/config.json')

    with tf.Session() as sess:
        # create an instance of the model you want
        model = Model(config)
        #load model if exists
        model.load(sess)

        # create your data generator
        # set generate_tfrecords to true in config file to write new tfrecords
        data = DataLoader(config)
        #data.write_train_and_test_sets(train_ratio=0.8)

        # create trainer and pass all the previous components to it
        trainer = Trainer(sess, model, data, config)

        # here you train your model
        trainer.train()


if __name__ == '__main__':
    main()
