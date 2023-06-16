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

file_name = ''+str(SIZE)+'_'+str(ITERATIONS)+'_'+str(AMOUNT)+'_'+str(ALT)+'_'+str(IND)+'_'+str(COM)+".txt"
script_dir = os.path.dirname(__file__)
rel_path = "maze_data/main_data/"+file_name
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path)

alt_dict = {}
ind_dict = {}
com_dict = {}

current_dict = alt_dict
c = 0
for x in f:
    print(c)
    c+=1
    if(x[0] == "r"):
        break
    
    values = x.split()
    if(values[0] == "player:"):
        role = values[2]
        if(role == "Individualist"):
            current_dict = ind_dict
        if(role == "Competitive"):
            current_dict = com_dict
        if(role == "Altruist"):
            current_dict = alt_dict
    else:
        (key, val) = values
        if(int(key) not in current_dict):
            current_dict[int(key)] = 0
        current_dict[int(key)] += int(val)

altlist = [key for key, val in alt_dict.items() for _ in range(val)]
# plt.hist(altlist, bins=33, alpha = 0.333, color='g')
comlist = [key for key, val in com_dict.items() for _ in range(val)]
# plt.hist(comlist, bins=33, alpha = 0.333,color='b')
indlist = [key for key, val in ind_dict.items() for _ in range(val)]
# plt.hist(indlist, bins=33, alpha = 0.333,color='r')

red = col.to_rgba('red', alpha=1)
green = col.to_rgba('green', alpha=0.7)
blue = col.to_rgba('blue', alpha=0.3)
colors = [red, green, blue]

plt.hist([altlist, indlist, comlist], bins = 25, label=['Data 1', 'Data 2', 'Data 3'], color = colors)
plt.show()