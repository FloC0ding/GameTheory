import main_multithread as Maze
import graph

import threading
import time
import getpass

num_threads = 20


def runner(thread_num, maze):
    while not maze.finished:
        maze.pc_cooperative()
        #time.sleep(0.0000000001)

def run_simulation(n, num_players, num_it, p1, p2, p3, n1, n2, n3): 
    mazes = []
    for _ in range(num_threads):
        mazes.append(Maze.Maze(n, num_players, num_it, p1, p2, p3, n1, n2, n3))



    k = graph.Graph(mazes[0].n+1)

    #copy differently such that no reference happens
    for m in mazes:
        m.maze = k

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

    # path for Flo's One Drive
    #path = "C:/Users/Florian/OneDrive/Game_Theory/Data/"
    
    path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"
    #strategy has to be added at this point manually
    #coop and non coop has to be added
    #Format: maze_size, same_maze, num_it, (strategy), (coop), time
    #bracket attributes have to be added
    name = str(mazes[0].n)+"_"+str(mazes[0].iterations * num_threads)+"_"+str(mazes[0].num_players)+"_"+str(seconds)+".txt"
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
                output["player: "+str(p.a_id)+" "+p.a_type+"\n"][i] += p.output[i]


    output_rank = {}
    #rank implementation
    for maze in mazes:
        for p in maze.player_storage:
            output_rank["player: "+str(p.a_id)+" "+p.a_type+"\n"] = {}

    for maze in mazes:
        for p in maze.player_storage:
            for i in p.output_rank:
                output_rank["player: "+str(p.a_id)+" "+p.a_type+"\n"][i] = 0


    for maze in mazes:
        for p in maze.player_storage:
            for i in p.output_rank:
                output_rank["player: "+str(p.a_id)+" "+p.a_type+"\n"][i] += p.output_rank[i]

    """for p_data in output_rank:
        for x in output_rank[p_data]:
            print("rank: "+str(x)+" times:"+str(output_rank[p_data][x])+"\n")"""

    for p_data in output:
        file.write(p_data)
        for x in output[p_data]:
            #print(str(x)+" "+str(output[p_data][x]))
            # steps | number of achieved steps | rank | number of achieved rank
            file.write(str(x)+" "+str(output[p_data][x])+"\n")

    for p_data in output_rank:
        file.write("rank "+p_data)
        for x in output_rank[p_data]:
            file.write(str(x)+" "+str(output_rank[p_data][x])+"\n")


    """for p_data in output:
        file.write(p_data)
        for x in output[p_data]:
            #print(str(x)+" "+str(output[p_data][x]))
            # steps | number of achieved steps | rank | number of achieved rank
            file.write(str(x)+" "+str(output[p_data][x])+"\n")"""

    file.close()


file = open("input.txt", "r")

c = 0

while True:

    line = file.readline()
    if not line: break


    line = line.split(" ")
    if line[0] == "#":
        pass
    else: 
        num_threads = int(line[0])
        n, p, num_it = int(line[1]), int(line[2]), int(line[3])
        p1, p2, p3 = float(line[4]), float(line[5]), float(line[6])
        n1, n2, n3 = int(line[7]), int(line[8]), int(line[9].split("\n")[0])
    
        #print(p)
        #run simulation and file writing function
        run_simulation(n, p, num_it, p1, p2, p3, n1, n2, n3)
        c += 1
        print("completed simulation nr: "+str(c))
