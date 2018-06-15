
from base.BaseModel import BaseModel
import tensorflow as tf
import numpy as np


class Model(BaseModel):
    def __init__(self, config):
        super(Model, self).__init__(config)
        self.config = config
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)

        batch_size = self.config.batch_size

        # Be careful to keep None at the batch size dim because the placeholder
        # is also used for testing which involves a batch size of 1 wich might
        # be different from the training batch size
        self.cards = tf.placeholder(tf.float32,
                                    shape=(None, 7, 17),
                                    name="cards")

        self.winprob = tf.placeholder(tf.float32,
                                      shape=(None, 4),
                                      name="winprob")

        keep_prob = tf.cond(self.is_training,
                            lambda: tf.constant(self.config.keep_prob, dtype=tf.float32),
                            lambda: tf.constant(1.0, dtype=tf.float32))

        with tf.name_scope("lstm"):
            lstm_size = 256
            lstm_plain = tf.contrib.rnn.BasicLSTMCell(lstm_size)
            lstm = tf.contrib.rnn.DropoutWrapper(lstm_plain,
                                                    input_keep_prob=keep_prob,
                                                    output_keep_prob=keep_prob)


        with tf.name_scope("lstm_init"):
            # Initial state of the LSTM memory.
            hidden_state, current_state = tf.cond(self.is_training,
                                lambda: (tf.zeros([batch_size, lstm_size]),) * 2,
                                lambda: (tf.zeros([1, lstm_size]),) * 2)
            state = hidden_state, current_state

        with tf.name_scope("embedding_net"):
            # Definition of weights for fully connected before entering the LSTM
            W_fc1 = tf.Variable(tf.truncated_normal((17, 1024), stddev=0.01))
            b_fc1 = tf.Variable(tf.constant(0.0, shape=(1024,)))


            W_fc2 = tf.Variable(tf.truncated_normal((1024, 512), stddev=0.01))
            b_fc2 = tf.Variable(tf.constant(0.0, shape=(512,)))

        with tf.name_scope("lstm_output"):
            W_final = tf.Variable(tf.truncated_normal((lstm_size, 1), stddev=0.01))
            b_final = tf.Variable(tf.constant(0.0, shape=(1,)))



        self.pred = []
        loss = 0.0
        train_stages = [1, 4, 5, 6]

        for timestep in range(7):
            with tf.name_scope("embedding_net"):
                current_card = self.cards[:, timestep, :]
                fc1 = tf.nn.relu(tf.matmul(current_card, W_fc1) + b_fc1)
                fc1_drop = tf.nn.dropout(fc1, keep_prob=keep_prob)

                fc2 = tf.nn.relu(tf.matmul(fc1, W_fc2) + b_fc2)
                fc2_drop = tf.nn.dropout(fc2, keep_prob=keep_prob)

            with tf.name_scope("lstm"):
                output, state = lstm(fc2_drop, state)

            with tf.name_scope("lstm_output"):
                logits = tf.matmul(output, W_final) + b_final
                proba = tf.squeeze(tf.nn.sigmoid(logits), axis=1)

                self.pred.append(proba)


            if timestep in train_stages:
                with tf.name_scope("loss"):
                    stage = train_stages.index(timestep)
                    stage = train_stages.index(timestep)
                    loss += tf.losses.mean_squared_error(self.winprob[:, stage],
                                                         self.pred[timestep])

        with tf.name_scope("loss"):
            self.loss = tf.identity(loss, name="total_loss")


        with tf.name_scope("optimizer"):
            optimizer = tf.train.AdamOptimizer()

            self.train_op = tf.contrib.training.create_train_op(
                                            total_loss=self.loss,
                                            optimizer=optimizer,
                                            global_step=self.global_step_tensor
                                            )

        with tf.name_scope("accuracy"):
            self.preflop_acc = tf.reduce_mean(tf.abs(self.pred[1] - self.winprob[:,0]))
            self.flop_acc = tf.reduce_mean(tf.abs(self.pred[4] - self.winprob[:,1]))
            self.turn_acc = tf.reduce_mean(tf.abs(self.pred[5] - self.winprob[:,2]))
            self.river_acc = tf.reduce_mean(tf.abs(self.pred[6] - self.winprob[:,3]))
            self.accuracy = (self.preflop_acc + self.flop_acc +
                             self.turn_acc + self.river_acc) / 4

    def init_saver(self):
        # here you initialize the tensorflow saver that will be used in saving the checkpoints.
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
