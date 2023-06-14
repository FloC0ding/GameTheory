import main_multithread as Maze
import graph

import threading
import time
import getpass
import copy

num_threads = 12

def runner(thread_num, maze):
    while not maze.finished:
        maze.pc_cooperative()
        time.sleep(0.0001)

mazes = []
for _ in range(num_threads):
    mazes.append(Maze.Maze())



k = graph.Graph(mazes[0].n_copy+1)

#copy differently such that no reference happens
for m in mazes:
    m.maze = k

"""def copy_edges(edges, vertices):
    copy = {}
    for v in vertices:
        copy[v] = []
    for v in edges:
        for u in edges[v]:
            k = graph.Vertex(u.pos_x, u.pos_y)
            copy[v].append(k)
    return copy

def copy_vertices(vertices):
    copy = set()
    for v in vertices:
        u = graph.Vertex(v.pos_x, v.pos_y)
        copy.add(u)
    return copy


size = mazes[0].n_copy
m =  graph.Graph(size)
v = m.vertices
e = m.neighbour_edges


for i in mazes: 
    i.maze.vertices = copy_vertices(v)
    i.maze.neighbour_edges = copy_edges(e, v)"""

#print("Finished initializing")

threads = []

for i in range(num_threads):
    thread = threading.Thread(target=runner, args=(i, mazes[i]))
    thread.start()
    threads.append(thread)

#all results are saved in the players of each maze in player_storage
#player storage has output array

for t in threads:
    t.join()
    

#write output into txt file
seconds = time.time()
path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"
#strategy has to be added at this point manually
#coop and non coop has to be added
#Format: maze_size, same_maze, num_it, (strategy), (coop), time
#bracket attributes have to be added
name = str(mazes[0].n_copy)+"_"+str(mazes[0].iterations * num_threads)+"_"+str(mazes[0].num_players_c)+"_"+str(seconds)+".txt"
name = path+name
file = open(name, "w")

output = {}     #maps player id and type to a list of results

for maze in mazes:
    for p in maze.player_storage:
        output["player: "+str(p.a_id)+" "+p.a_type+"\n"] = {}

for maze in mazes:
    for p in maze.player_storage:
        for i in p.output:
            output["player: "+str(p.a_id)+" "+p.a_type+"\n"][i] = 0

for maze in mazes:
    for p in maze.player_storage:
        for i in p.output:
            output["player: "+str(p.a_id)+" "+p.a_type+"\n"][i] += 1

for p_data in output:
    file.write(p_data)
    for x in output[p_data]:
        file.write(str(x)+" "+str(output[p_data][x])+"\n")

"""for maze in mazes:
    for p in maze.player_storage:
        file.write("player: "+str(p.a_id)+" "+p.a_type+"\n")
        for i in p.output:
            file.write(str(i)+" "+str(p.output[i])+"\n")"""


file.close()
