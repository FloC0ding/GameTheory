import matplotlib.pyplot as plt
import random

x, y = [], []

name = "20_False_200_5_1686646669.5775082.txt"
path = "C:/Users/Florian/git/Game Theory/Maze_Measuring_Data/"+name
file = open(path, "r")


while True:

    line = file.readline()

    if not line: break
    line = line.split(" ")

    if line[0] == "player:":
        """(r, g, b) = (random.random(), random.random(), random.random())
        print(r)
        print(g)
        print(b)
        plt.bar(x, y, color=(r, g, b))
        x.clear()
        y.clear()"""
        pass
    else:
        x.append(int(line[0]))
        y.append(int(line[1].split("\n")[0]))

plt.bar(x, y)
plt.xlabel('Number of steps to comlete maze')
plt.xlabel('Number of players finished with x many steps')

plt.show()

file.close()