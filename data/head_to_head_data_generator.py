

import sys

sys.path.append(sys.path[0] + "/../src")


from gameframework import Simulator


def main():

    simulator = Simulator()

    df = simulator.generate_training_set(nb_trainings=10000, verbose = True)
    df.to_csv(sys.path[0] + '/head_to_head.csv')




if __name__ == '__main__':
    main()
