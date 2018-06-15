

import sys

sys.path.append(sys.path[0] + "/../../")
#print(sys.path)


from gameframework import Simulator


def main(nb_trainings):

    simulator = Simulator()
    df = simulator.generate_training_set(nb_trainings=nb_trainings, verbose = True)
    df.to_csv(sys.path[0] + '/../../../data/lstm.csv')




if __name__ == '__main__':
    nb_trainings = int(sys.argv[1])
    main(nb_trainings)
