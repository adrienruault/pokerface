from datetime import datetime

import tensorflow as tf


class BaseTrain:
    def __init__(self, sess, model, data, config):
        self.model = model
        self.config = config
        self.sess = sess
        self.data = data
        self.init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.sess.run(self.init)

    def train(self):

        coord = tf.train.Coordinator()
        thread = tf.train.start_queue_runners(coord=coord)

        for cur_epoch in range(self.model.cur_epoch_tensor.eval(self.sess), self.config.num_epochs + 1, 1):
            date = datetime.now()
            string_date = "[%02d:%02d:%02d]" % (date.hour, date.minute, date.second)
            print(string_date, "running epoch", cur_epoch+1, "out of", self.config.num_epochs)

            self.train_epoch()
            self.sess.run(self.model.increment_cur_epoch_tensor)

        # Stop the threads
        coord.request_stop()

        # Wait for threads to stop
        coord.join(thread)

    def train_epoch(self):
        """
        implement the logic of epoch:
        -loop over the number of iterations in the config and call the train step
        -add any summaries you want using the summary
        """
        raise NotImplementedError

    def train_step(self):
        """
        implement the logic of the train step
        - run the tensorflow session
        - return any metrics you need to summarize
        """
        raise NotImplementedError
