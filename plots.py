import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import os
import pandas as pd

SIZE = 20
ITERATIONS = 2000
AMOUNT = 12
ALT = 4
IND = 4
COM = 4

file_name = ''+str(SIZE)+'_'+str(ITERATIONS)+'_' + \
    str(AMOUNT)+'_'+str(ALT)+'_'+str(IND)+'_'+str(COM)
script_dir = os.path.dirname(__file__)
rel_path = "maze_data/main_data/"+file_name+".txt"
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path)

alt_dict = {}
ind_dict = {}
com_dict = {}
role = ""
current_dict = alt_dict
c = 0
for x in f:
    c += 1
    if (x[0] == "r"):
        break

    values = x.split()
    if (values[0] == "player:"):
        role = values[2]
        print("Role Change: "+role)
    else:
        (key, val) = values
        if (role == "Individualist"):
            if (int(key) not in ind_dict):
                ind_dict[int(key)] = 0
            ind_dict[int(key)] += int(val)
        if (role == "Competitive"):
            if (int(key) not in com_dict):
                com_dict[int(key)] = 0
            com_dict[int(key)] += int(val)
        if (role == "Altruist"):
            if (int(key) not in alt_dict):
                alt_dict[int(key)] = 0
            alt_dict[int(key)] += int(val)
        

altlist = [key for key, val in alt_dict.items() for _ in range(val)]
# plt.hist(altlist, bins=33, alpha = 0.333, color='g')
comlist = [key for key, val in com_dict.items() for _ in range(val)]
# plt.hist(comlist, bins=33, alpha = 0.333,color='b')
indlist = [key for key, val in ind_dict.items() for _ in range(val)]
# plt.hist(indlist, bins=33, alpha = 0.333,color='r')


plt.figure(0,figsize=(5,5))
plt.hist(altlist, 100, histtype='bar', color='r', alpha=0.7)
plt.title("Altruistic Part")
plt.xlabel("# of steps")
plt.ylabel("# of agents")
plt.show()

plt.figure(1,figsize=(5,5))
plt.hist(indlist, 100, histtype='bar', color='g', alpha=0.7)
plt.title("Individualistic Part")
plt.xlabel("# of steps")
plt.ylabel("# of agents")
plt.show()

plt.figure(2,figsize=(5,5))
plt.hist(comlist, 100, histtype='bar', color='b', alpha=0.7)
plt.title("Competitive Part")
plt.xlabel("# of steps")
plt.ylabel("# of agents")
plt.show()

