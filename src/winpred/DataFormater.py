import os

import numpy as np
import pandas as pd
import tensorflow as tf




class DataFormater:

    suit_convert = {'H': 1, 'D': 2, 'C': 3, 'S': 4}

    rank_convert = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,\
                    '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}


    def __init__(self, config):
        self.data_file = config.data_file

        exp_folder = 'xp/' + config.exp_name
        tfrecords_folder = exp_folder + '/tfrecords'

        if not os.path.isdir(exp_folder):
            os.mkdir(exp_folder)

        if not os.path.isdir(tfrecords_folder):
            os.mkdir(tfrecords_folder)

        self.train_file = tfrecords_folder +  '/train.tfrecords'
        self.test_file = tfrecords_folder + '/test.tfrecords'




    def write_train_and_test_sets(self, train_ratio=0.8):
        df = pd.read_csv(self.data_file, delimiter=',', usecols=list(range(1,10)))
        data = df.values

        # shuffle indices and then split into train and test sets
        nb_data = data.shape[0]
        nb_train = int(nb_data * train_ratio)
        indices = np.arange(nb_data)
        np.random.shuffle(indices)

        train_indices = indices[:nb_train]
        test_indices = indices[nb_train:]

        train_set = data[train_indices]
        test_set = data[test_indices]

        self.__write_tfrecords(train_set, file_name=self.train_file)
        self.__write_tfrecords(test_set, file_name=self.test_file)



    def __write_tfrecords(self, data, file_name):

        writer = tf.python_io.TFRecordWriter(file_name)

        # iterate over every data point, the idea is to transform them one by one
        # in tfrecord format and to write them to a tfrecords file
        for i in range(data.shape[0]):
            card_vec = data[i][0:7]

            # create container for cards in onehot format
            cards_one_hot = np.zeros((7, 19), dtype=np.int64)

            winprob = data[i][8]


            for j, card in enumerate(card_vec):
                one_hot = self.one_hot_factory(card)
                cards_one_hot[j] = one_hot

            # Create a feature
            feature_dict = {'winprob': tf.train.Feature(float_list=tf.train.FloatList(value=[winprob])),
                       'cards': tf.train.Feature(int64_list=tf.train.Int64List(value=cards_one_hot.flatten()))}

            feature = tf.train.Features(feature=feature_dict)

            # create an example from feature and write it to the target file
            example = tf.train.Example(features=feature)
            writer.write(example.SerializeToString())


    def get_batch(self, batch_size=10):

        train_filename = self.train_file

        reader = tf.TFRecordReader()
        filename_queue = tf.train.string_input_producer([train_filename])
        _, serialized_example = reader.read(filename_queue)

        # Define features
        read_features = {
            'winprob': tf.FixedLenFeature([], dtype=tf.float32),
            'cards': tf.FixedLenFeature([133], dtype=tf.int64)}

        # Extract features from serialized data
        read_data = tf.parse_single_example(serialized=serialized_example,
                                            features=read_features)

        cards_op = tf.reshape(read_data['cards'], shape=(7, 19))
        winprob_op = read_data['winprob']

        cards_batch, winprob_batch = tf.train.shuffle_batch([cards_op, winprob_op], batch_size=batch_size,\
                                            capacity=3*batch_size, num_threads=1,\
                                            min_after_dequeue=batch_size)


    @classmethod
    def one_hot_factory(cls, card):

        card_list = card.split("-")

        one_hot_rank = np.zeros(14)
        one_hot_rank[cls.rank_convert[card_list[0]]] = 1.

        one_hot_suit = np.zeros(5)
        one_hot_suit[cls.suit_convert[card_list[1]]] = 1.

        one_hot = np.concatenate((one_hot_rank, one_hot_suit))
        return one_hot
