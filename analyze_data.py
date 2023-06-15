import matplotlib.pyplot as plt
import random
import getpass
import numpy as np
import math

x, y = [], []

name = "10_400_9_1686843959.6458101.txt"

path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"+name
file = open(path, "r")



x_alt, y_alt = [], []
x_ind, y_ind = [], []
x_comp, y_comp = [], []

start = False
alt, ind, comp = False, False, False
type = ""
data_min, data_max = 100000, 0
data_y_max = 0

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

offset = 8  #offset for max value
width = 10      
print("Width of each pillar is: "+str(width+1))

def even_out(x, y):
    x_n, y_n = [], []

    for i in range(data_min, data_max+1):
        x_n.append(i)
        y_n.append(0)

    for i in range(0, len(x)):
        y_n[x[i]-data_min] += y[i]
    #print(x_n)
    #print(y_n)

    sorted_data = sorted(zip(x_n, y_n), key =lambda pair:pair[0])
    x_sorted, y_sorted = zip(*sorted_data)

    """print("!!!!")
    print(x_sorted)
    print("!!!!!")
    print(y_sorted)"""

    x_grouped = [x_sorted[i:i+width] for i in range(0, len(x_sorted), width)]
    y_grouped = [sum(y_sorted[i:i+width]) for i in range(0, len(y_sorted), width)]


    x_final, y_final = [], []
    for i in range(0, len(y_grouped)):
        p = x_grouped[i]
        for k in p:
            x_final.append(k)
            y_final.append(y_grouped[i])

    return (x_final, y_final)

def compute_avg(x, y):
    sum = 0.0
    c = 0
    if len(y) == 0: return 0.0

    for i in range(0, len(x)):
        sum += (x[i] * y[i])
        c += y[i]
    return sum / c

def compute_std_deviation(x, y, avg):
    sum = 0.0
    c = 0
    if len(y) == 0: return 0.0

    for i in range(0, len(x)):
        sum += pow(x[i]-avg, 2)*y[i]
        c += y[i]
    return math.sqrt(sum/c)

#TODO average for each type and for all results
#maybe standard derivation
#median
avg = compute_avg(x, y)
print("Average of all players: "+str(avg))
avg_alt = compute_avg(x_alt, y_alt)
print("Average of all altruist players: "+str(avg_alt))
avg_ind = compute_avg(x_ind, y_ind)
print("Average of all neutral players: "+str(avg_ind))
avg_comp = compute_avg(x_comp, y_comp)
print("Average of all competitive players: "+str(avg_comp))

std = compute_std_deviation(x, y, avg)
print("Standard derivation of all players: "+str(std))
std_alt = compute_std_deviation(x_alt, y_alt, avg_alt)
print("Standard derivation of all altruist players: "+str(std_alt))
std_ind = compute_std_deviation(x_ind, y_ind, avg_ind)
print("Standard derivation of all neutral players: "+str(std_ind))
std_comp = compute_std_deviation(x_comp, y_comp, avg_comp)
print("Standard derivation of all competitive players: "+str(std_comp))


plt.figure(0)
plt.bar(x, y)
plt.title("all together wrong")

"""p = even_out(x, y)
x, y = p[0], p[1]

for k in p[1]: data_y_max = max(data_y_max, k)
#print(data_y_max)

p = even_out(x_alt, y_alt)
x_alt, y_alt = p[0], p[1]

p = even_out(x_ind, y_ind)
x_ind, y_ind = p[0], p[1]

p = even_out(x_comp, y_comp)
x_comp, y_comp = p[0], p[1]

plt.figure(1)
plt.bar(x, y)
plt.title("all players")
plt.ylim(0, data_y_max+offset)

plt.figure(2)
plt.bar(x_alt, y_alt)
plt.title("altruist")
plt.ylim(0, data_y_max+offset)

plt.figure(3)
plt.bar(x_ind, y_ind)
plt.title("neutral")
plt.ylim(0, data_y_max+offset)

plt.figure(4)
plt.bar(x_comp, y_comp)
plt.title("competitive")
plt.ylim(0, data_y_max+offset)"""



#plt.figure(2)
#plt.bar(x_alt, y_alt)


#plt.tight_layout()

plt.show()

file.close()
