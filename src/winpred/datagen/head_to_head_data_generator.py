

import sys

sys.path.append(sys.path[0] + "/../../")
#print(sys.path)


from gameframework import Simulator


def main():

    simulator = Simulator()

    df = simulator.generate_training_set(nb_trainings=10000, verbose = True)
    df.to_csv(sys.path[0] + '/../../../data/test.csv')




if __name__ == '__main__':
    main()
