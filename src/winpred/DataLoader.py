import os

import numpy as np
import pandas as pd
import tensorflow as tf




class DataLoader:

    suit_convert = {'H': 1, 'D': 2, 'C': 3, 'S': 4}

    value_convert = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,\
                    '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}


    def __init__(self, config):
        self.data_file = config.data_file

        self.train_file = config.tfrecords_dir +  '/train.tfrecords'
        self.test_file = config.tfrecords_dir + '/test.tfrecords'

        #if config.generate_tfrecords == "True":
        self.write_train_and_test_sets(train_ratio=config.train_ratio)

        cards_batch, winprob_batch = self.build_batch_ops(
                                                batch_size=config.batch_size,
                                                filename=self.train_file
                                                )
        self.getter_cards_batch = cards_batch
        self.getter_winprob_batch = winprob_batch

        cards_test, winprob_test = self.build_batch_ops(
                                                batch_size=1,
                                                filename=self.test_file
                                                )
        self.getter_cards_test = cards_test
        self.getter_winprob_test = winprob_test








    def write_train_and_test_sets(self, train_ratio=0.8):
        df = pd.read_csv(self.data_file, delimiter=',', index_col=0)
        data = df.values

        # shuffle indices and then split into train and test sets
        num_data = data.shape[0]
        num_train = int(num_data * train_ratio)
        num_test = num_data - num_train

        indices = np.arange(num_data)
        np.random.shuffle(indices)

        train_indices = indices[:num_train]
        test_indices = indices[num_train:]

        train_set = data[train_indices]
        test_set = data[test_indices]


        self.__write_tfrecords(train_set, filename=self.train_file)
        self.__write_tfrecords(test_set, filename=self.test_file)

        self.num_data = num_data
        self.num_train = num_train
        self.num_test = num_test



    def __write_tfrecords(self, data, filename):
        """
        Take the dataset as input in numpy array format and then writes the
        corresponding tfrecords at the location specified by filename.
        """

        writer = tf.python_io.TFRecordWriter(filename)

        # iterate over every data point, the idea is to transform them one by one
        # in tfrecord format and to write them to a tfrecords file
        for i in range(data.shape[0]):
            card_vec = data[i][0:7]

            # create container for cards in onehot format
            cards_one_hot = np.zeros((7, 17), dtype=np.int64)

            winprob = [data[i][8], data[i][12], data[i][16], data[i][20]]


            for j, card in enumerate(card_vec):
                one_hot_card = self.one_hot_factory(card)
                cards_one_hot[j] = one_hot_card

            # Create a feature
            feature_dict = {'winprob': tf.train.Feature(float_list=tf.train.FloatList(value=winprob)),
                       'cards': tf.train.Feature(int64_list=tf.train.Int64List(value=cards_one_hot.flatten()))}

            feature = tf.train.Features(feature=feature_dict)

            # create an example from feature and write it to the target file
            example = tf.train.Example(features=feature)
            writer.write(example.SerializeToString())


    def build_batch_ops(self, batch_size, filename):

        with tf.name_scope("batch_getter"):
            reader = tf.TFRecordReader()
            filename_queue = tf.train.string_input_producer([filename])
            _, serialized_example = reader.read(filename_queue)

            # Define features
            read_features = {
                'winprob': tf.FixedLenFeature([4], dtype=tf.float32),
                'cards': tf.FixedLenFeature([119], dtype=tf.int64)}

            # Extract features from serialized data
            read_data = tf.parse_single_example(serialized=serialized_example,
                                                features=read_features)

            cards_op = tf.reshape(read_data['cards'], shape=(7, 17))
            winprob_op = read_data['winprob']

            # tensorflow operation that can be run in order to get a batch
            cards_batch, winprob_batch = tf.train.shuffle_batch([cards_op, winprob_op], batch_size=batch_size,\
                                                capacity=3*batch_size, num_threads=1,\
                                                min_after_dequeue=batch_size)

        return cards_batch, winprob_batch





    @classmethod
    def one_hot_factory(cls, card):

        card_list = card.split("-")

        one_hot_rank = np.zeros(13)
        one_hot_rank[cls.value_convert[card_list[0]] - 1] = 1.

        one_hot_suit = np.zeros(4)
        one_hot_suit[cls.suit_convert[card_list[1]] - 1] = 1.

        one_hot = np.concatenate((one_hot_rank, one_hot_suit))
        return one_hot
