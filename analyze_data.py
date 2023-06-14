import matplotlib.pyplot as plt
import random
import getpass

x, y = [], []

name = "31_150_1_1686736021.6639714.txt"
path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"+name
file = open(path, "r")

x_alt, y_alt = [], []
x_ind, y_ind = [], []
x_comp, y_comp = [], []

start = False
alt, ind, comp = False, False, False
type = ""

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
plt.figure(1)
plt.bar(x, y)

plt.figure(2)
plt.bar(x_alt, y_alt)


#plt.tight_layout()

plt.show()

file.close()