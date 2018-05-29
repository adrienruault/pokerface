import os
import sys

from utils.config import process_config


def create_dirs(dirs):
    """
    dirs - a list of directories to create if these directories are not found
    :param dirs:
    :return exit_code: 0:success -1:failed
    """
    try:
        for dir_ in dirs:
            if not os.path.exists(dir_):
                os.makedirs(dir_)
        return 0
    except Exception as err:
        print("Creating directories error: {0}".format(err))
        exit(-1)




def set_up_experience(rel_path_to_config):
    # capture the config path from the run arguments
    # then process the json configuration file
    cur_dir = sys.path[0] #<-- absolute dir the script is in
    abs_file_path = os.path.join(cur_dir, rel_path_to_config)
    config = process_config(abs_file_path)

    # create the experiments dirs
    rel_path_xp_dir = 'xp/' + config.exp_name
    config.xp_dir = os.path.join(cur_dir, rel_path_xp_dir)

    if os.path.isdir(config.xp_dir):
        print("Experience " + config.exp_name + " already exists")
        exit(0)

    config.tfrecords_dir = config.xp_dir + '/tfrecords'
    config.summary_dir = config.xp_dir + '/summaries'
    config.train_summary_dir = config.summary_dir + '/train'
    config.test_summary_dir = config.summary_dir + '/test'
    config.checkpoint_dir = config.xp_dir + '/checkpoints'



    dirs_to_create = [config.xp_dir, config.tfrecords_dir,
                      config.summary_dir, config.train_summary_dir,
                      config.test_summary_dir, config.checkpoint_dir]

    create_dirs(dirs_to_create)

    # Transforming data_file path into absolute path
    config.data_file = os.path.join(cur_dir, config.data_file)

    return config
