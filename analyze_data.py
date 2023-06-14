import matplotlib.pyplot as plt
import random
import getpass
import numpy as np
import math

x, y = [], []

name = "25_2000_10_1686751473.8268073.txt"
path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"+name
file = open(path, "r")

x_alt, y_alt = [], []
x_ind, y_ind = [], []
x_comp, y_comp = [], []

start = False
alt, ind, comp = False, False, False
type = ""
data_min, data_max = 100000, 0


while True:

    line = file.readline()

    if not line: break
    line = line.split(" ")


    if line[0] == "player:":
        alt, ind, comp = False, False, False
        type = line[2].split("\n")[0]
        if type == "Altruist":
            alt = True
        elif type == "Individualist":
            ind = True
        else: comp = True

        if not start: 
            start = True
        pass
    else:
        x.append(int(line[0]))
        y.append(int(line[1].split("\n")[0]))
        data_min = min(data_min, int(line[0]))
        data_max = max(data_max, int(line[0]))


        if alt: 
            x_alt.append(int(line[0]))
            y_alt.append(int(line[1].split("\n")[0]))
        elif ind: 
            x_ind.append(int(line[0]))
            y_ind.append(int(line[1].split("\n")[0]))
        elif comp:
            x_comp.append(int(line[0]))
            y_comp.append(int(line[1].split("\n")[0]))

#fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

#plt.figure(1)
#plt.bar(x, y)
#ax1.bar(x, y)
#ax1.set_title("all players")

#ax2.bar(x_alt, y_alt)
#ax2.set_title("Altruists")

#ax3.bar(x_ind, y_ind)
#ax3.set_title("Individualists")

#ax4.bar(x_comp, y_comp)
#ax4.set_title("Competitive")


def change_width(x, y):
    new_x, new_y = [], []
    #each value is 





plt.figure(1)
plt.bar(x, y)


"""xticks = np.linspace(data_min, data_max, 10)
xticks = np.ceil(xticks)

# Split the data based on xticks intervals
splitted_data = np.digitize(x, xticks)

# Plot the splitted data
for i in range(1, len(xticks)):
    indices = np.where(splitted_data == i)
    plt.bar(np.array(x)[indices], np.array(y)[indices])

plt.xticks(xticks)"""

#plt.figure(2)
#plt.bar(x_alt, y_alt)


#plt.tight_layout()

plt.show()

file.close()