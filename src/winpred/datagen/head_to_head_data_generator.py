

import sys

sys.path.append(sys.path[0] + "/../../")
#print(sys.path)


from gameframework import Simulator


def main():

    simulator = Simulator()
    nb_trainings = 1000
    df = simulator.generate_training_set(nb_trainings=nb_trainings, verbose = True)
    df.to_csv(sys.path[0] + '/../../../data/test.csv')




if __name__ == '__main__':
    main()
