from tqdm import tqdm
import numpy as np
import tensorflow as tf

from base.BaseTrain import BaseTrain



class Trainer(BaseTrain):
    def __init__(self, sess, model, data, config):
        super(Trainer, self).__init__(sess, model, data, config)

        # summary epoch
        summary_list = [tf.summary.scalar('total_loss', self.model.loss),
                       tf.summary.scalar('average_accuracy', self.model.accuracy),
                       tf.summary.scalar('1_preflop_acc', self.model.preflop_acc),
                       tf.summary.scalar('2_flop_acc', self.model.flop_acc),
                       tf.summary.scalar('3_turn_acc', self.model.turn_acc),
                       tf.summary.scalar('4_river_acc', self.model.river_acc)]

        self.summary_ops = tf.summary.merge(summary_list)

        self.train_writer = tf.summary.FileWriter(config.train_summary_dir, sess.graph)
        self.test_writer = tf.summary.FileWriter(config.test_summary_dir, sess.graph)


    def train_epoch(self):
        num_iter_per_epoch = int(self.data.num_train / self.config.batch_size)
        loop = tqdm(range(num_iter_per_epoch))

        cur_epoch = self.model.global_step_tensor.eval(self.sess)
        glob_step = self.sess.run(self.model.global_step_tensor)

        losses = []
        accs = []
        test_losses = []
        test_accs = []

        for i in loop:
            loss, acc = self.train_step()
            losses.append(loss)
            accs.append(acc)

            # online testing
            if i % self.config.test_every_n_iter == 0:
                test_loss, test_acc = self.test_step()
                test_losses.append(test_loss)
                test_accs.append(test_acc)

        loss = np.mean(losses)
        acc = np.mean(accs)
        test_loss = np.mean(test_losses)
        test_acc = np.mean(test_accs)


        summary_epoch = tf.Summary(
                value=[tf.Summary.Value(tag="epoch_loss", simple_value=loss),
                       tf.Summary.Value(tag="epoch_accuracy", simple_value=acc)]
                                  )
        summary_test_epoch = tf.Summary(
                value=[tf.Summary.Value(tag="epoch_loss", simple_value=test_loss),
                       tf.Summary.Value(tag="epoch_accuracy", simple_value=test_acc)]
                                  )

        self.train_writer.add_summary(summary_epoch, global_step=glob_step)
        self.test_writer.add_summary(summary_test_epoch, global_step=glob_step)

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

        return loss, acc


    def test_step(self):
        cards_test, winprob_test = self.sess.run([self.data.getter_cards_test,
                                                  self.data.getter_winprob_test])
        test_dict = {
                     self.model.cards: cards_test,
                     self.model.winprob: winprob_test,
                     self.model.is_training: False
                    }

        loss, acc, summary = self.sess.run([self.model.loss,
                                            self.model.accuracy,
                                            self.summary_ops],
                                            feed_dict=test_dict)

        glob_step = self.sess.run(self.model.global_step_tensor)
        self.test_writer.add_summary(summary, global_step = glob_step)

        return loss, acc
