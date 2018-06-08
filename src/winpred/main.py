import os
import sys

import tensorflow as tf

from DataLoader import DataLoader
from trainers.Trainer import Trainer
from models.FullyConnected import FullyConnected as Model

from utils.dirs import create_dirs, set_up_experience






def main():

    config = set_up_experience('configs/config.json')

    with tf.Session() as sess:
        # create an instance of the model you want
        model = Model(config)
        #load model if exists
        model.load(sess)
        # create your data generator
        data = DataLoader(config)

        # create trainer and pass all the previous components to it
        trainer = Trainer(sess, model, data, config)

        # here you train your model
        trainer.train()


if __name__ == '__main__':
    main()
