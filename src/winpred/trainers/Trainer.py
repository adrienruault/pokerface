from tqdm import tqdm
import numpy as np
import tensorflow as tf

from base.BaseTrain import BaseTrain



class Trainer(BaseTrain):
    def __init__(self, sess, model, data, config):
        super(Trainer, self).__init__(sess, model, data, config)

        # summary epoch
        summary_list = [tf.summary.scalar('loss', self.model.loss),
                       tf.summary.scalar('accuracy', self.model.accuracy),
                       tf.summary.scalar('preflop_acc', self.model.preflop_acc),
                       tf.summary.scalar('flop_acc', self.model.flop_acc),
                       tf.summary.scalar('turn_acc', self.model.turn_acc),
                       tf.summary.scalar('river_acc', self.model.river_acc)]

        self.summary_ops = tf.summary.merge(summary_list)

        self.train_writer = tf.summary.FileWriter(config.train_summary_dir, sess.graph)
        self.test_writer = tf.summary.FileWriter(config.test_summary_dir, sess.graph)


    def train_epoch(self):
        num_iter_per_epoch = int(self.data.num_train / self.config.batch_size)
        loop = tqdm(range(num_iter_per_epoch))
        losses = []
        accs = []

        for _ in loop:
            loss, acc = self.train_step()
            losses.append(loss)
            accs.append(acc)

        loss = np.mean(losses)
        acc = np.mean(accs)

        cur_epoch = self.model.global_step_tensor.eval(self.sess)
        glob_step = self.sess.run(self.model.global_step_tensor)

        summary_epoch = tf.Summary(
                value=[tf.Summary.Value(tag="epoch_loss", simple_value=loss),
                       tf.Summary.Value(tag="epoch_accuracy", simple_value=acc)]
                                  )

        self.train_writer.add_summary(summary_epoch, global_step=glob_step)

        #self.logger.summarize(cur_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):

        cards_batch, winprob_batch = self.sess.run([self.data.getter_cards_batch,
                                                    self.data.getter_winprob_batch])

        feed_dict = {
                     self.model.cards: cards_batch,
                     self.model.winprob: winprob_batch,
                     self.model.is_training: True
                    }

        glob_step = self.sess.run(self.model.global_step_tensor)


        # TRAINING
        if glob_step % self.config.summarize_every_n_iter == 0:
            _, loss, acc, summary = self.sess.run([self.model.train_op,
                                          self.model.loss,
                                          self.model.accuracy,
                                          self.summary_ops],
                                         feed_dict=feed_dict)

            self.train_writer.add_summary(summary, global_step=glob_step)
        else:
            _, loss, acc = self.sess.run([self.model.train_op,
                                          self.model.loss,
                                          self.model.accuracy],
                                         feed_dict=feed_dict)

        # ONLINE TESTING
        if glob_step % self.config.test_every_n_iter == 0:
            self.test_step(glob_step)

        return loss, acc


    def test_step(self, glob_step):
        cards_test, winprob_test = self.sess.run([self.data.getter_cards_test,
                                                  self.data.getter_winprob_test])
        test_dict = {
                     self.model.cards: cards_test,
                     self.model.winprob: winprob_test,
                     self.model.is_training: False
                    }

        summary = self.sess.run(self.summary_ops, feed_dict=test_dict)
        self.test_writer.add_summary(summary, global_step = glob_step)
