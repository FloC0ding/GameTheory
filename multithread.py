import main_multithread as Maze
import threading
import time
import getpass

num_threads = 20

def runner(thread_num, maze):
    while not maze.finished:
        maze.pc_cooperative()
        time.sleep(0.0001)

mazes = []
for _ in range(num_threads):
    mazes.append(Maze.Maze())
m = mazes[0]
for i in mazes: i = m 


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
name = str(mazes[0].n_copy)+"_"+str(mazes[0].iterations)+"_"+str(mazes[0].num_players_c)+"_"+str(seconds)+".txt"
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
