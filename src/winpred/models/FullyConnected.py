
from base.BaseModel import BaseModel
import tensorflow as tf


class FullyConnected(BaseModel):
    def __init__(self, config):
        super(FullyConnected, self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)


        self.cards = tf.placeholder(tf.float32,
                                    shape=(None, 7, 19),
                                    name="cards")

        self.winprob = tf.placeholder(tf.float32,
                                      shape=(None, 1),
                                      name="winprob")

        flat_cards = tf.reshape(self.cards, shape=(-1, 7*19))

        W_fc1 = tf.Variable(tf.truncated_normal((7*19, 1024), stddev=0.01))
        b_fc1 = tf.Variable(tf.constant(0.0, shape=(1024,)))
        fc1 = tf.nn.relu(tf.matmul(flat_cards, W_fc1) + b_fc1)

        W_fc2 = tf.Variable(tf.truncated_normal((1024, 512), stddev=0.01))
        b_fc2 = tf.Variable(tf.constant(0.0, shape=(512,)))
        fc2 = tf.nn.relu(tf.matmul(fc1, W_fc2) + b_fc2)

        W_fc3 = tf.Variable(tf.truncated_normal((512, 1), stddev=0.01))
        b_fc3 = tf.Variable(tf.constant(0.0, shape=(1,)))


        output = tf.sigmoid(tf.matmul(fc2, W_fc3) + b_fc3)
        self.pred = output

        with tf.name_scope("loss"):
            self.loss = tf.losses.mean_squared_error(self.winprob, self.pred)
            optimizer = tf.train.AdamOptimizer()

            self.train_op = tf.contrib.training.create_train_op(
                                            total_loss=self.loss,
                                            optimizer=optimizer,
                                            global_step=self.global_step_tensor
                                            )

            self.accuracy = tf.reduce_mean(tf.abs(self.pred - self.winprob))


    def init_saver(self):
        # here you initialize the tensorflow saver that will be used in saving the checkpoints.
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
