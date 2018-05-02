








def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print("missing or invalid arguments")
        exit(0)

    # create the experiments dirs
    create_dirs([config.summary_dir, config.checkpoint_dir])

    with tf.Session() as sess:
        # create tensorflow session
        sess = tf.Session()
        # create an instance of the model you want
        model = Model(config)
        #load model if exists
        model.load(sess)
        # create your data generator
        data = DataGenerator(config)
        # create tensorboard logger
        logger = Logger(sess, config)
        # create trainer and pass all the previous components to it
        trainer = Trainer(sess, model, data, config, logger)

        # here you train your model
        trainer.train()


if __name__ == '__main__':
main()
