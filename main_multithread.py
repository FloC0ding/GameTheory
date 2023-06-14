#imports from own files
import graph as G
import agents as A

#import from matplotlib and kivy
#import matplotlib.pyplot as plt
#from collections import Counter


#from kivy.properties import (
#    NumericProperty, ReferenceListProperty, ObjectProperty
#)

#python imports
import random as rand
import time
import getpass

import threading


n = 20              #number of fields of the labyrinth per row or line






#player
p_size = 5

#simulation settings
update_speed = 0.000005  #number of seconds for which the update function is called
#num_it = 10
#iterations = num_it
c_temp = []
new_maze_perIt = False
gui = False

#counts the minimal number of steps to escape works only for same_maze
solve_maze_step = 0
#cooperative parameters
num_players = 5

player_type = {
    "Altruist": 0.001,
    "Individualist": 0.02,
    "Competitive":  0.05
}

#player_storage = {}     #lock this list maps thread_id to a list of players
#thread_id -> []


class Maze():



    def __init__(self):  #, **kwargs): 
        #super(Maze, self).__init__(**kwargs)

        #initialize multithreading variables
        #player_storage[threading.get_ident()] = []
        self.player_storage = []
        self.n = 0
        self.num_players_c = num_players

        self.num_it = 100
        self.iterations = self.num_it

        #initialize variables
        self.maze = G.Graph() 
        #self.maze = G.Graph()
        self.start = False
        self.finished = False
        self.p_outofbound = 0
        #initialize variables non_coop
        self.count = 0
        self.p1 = A.Agent(-1, -1, -1, -1, 1, "Altruist", [], 0, 0)
        self.visited = []
        self.stack = []
        
        self.initialize_player(self.p1)

        #implement cooperative game mode
        #choose the amount of different players
        num_alt = num_players/3
        num_ind = num_players/3
        num_comp = num_players - num_ind - num_alt


        self.players = []
        id = 0
        for _ in range(0, num_players):
            #types = list(player_type.keys())
            #p = A.Agent(-1, -1, -1, -1, 1, types[rand.randint(0, len(types)-1)], [], 0, 0)        #types[rand.randint(0, 2)]
            type = ""
            if num_alt > 0:
                num_alt -= 1
                type = "Altruist"
            elif num_ind > 0:
                num_ind -= 1
                type = "Individualist"
            elif num_comp > 0:
                num_comp -= 1
                type = "Competitive"
            p = A.Agent(-1, -1, -1, -1, 1, type, [], 0, 0)        #types[rand.randint(0, 2)]
            p.a_id = id
            id += 1
            self.players.append(p)
            self.initialize_player_random(p)
            #self.initialize_player(p)
            
    def initialize_n(self, n):
        self.n = n

    def initialize_player(self, p):
         #initialize p1 position
        if self.n % 2 == 0:
            p.pos_x = (self.n+1)/2
            p.pos_y = (self.n+1)/2
        else :
            p.pos_x = self.n/2
            p.pos_y = self.n/2
    
    def initialize_player_random(self, p):
        p.pos_x = rand.randint(0, self.n-1) + 0.5
        p.pos_y = rand.randint(0, self.n-1) + 0.5


    def pc_cooperative(self):

        if self.finished: 
            return


        #check if players have met each other and if yes if they collaborate
        #do this in pc_cooperative_dfs_random_walk
        #TODO
        #mistake where dead branches influence the stack
        for p in self.players:
            a = self.maze.check_edge(p)
            collabs = self.find_collaborator(p, a)
            for p2 in collabs:
                #add visited from p to p2 and vice versa if p2 not equal p
                if p.a_id != p2.a_id and p.collab_cooldown == 0 and p2.collab_cooldown == 0:
                    p.collab_cooldown = 0   #num_players-5
                    p.collab_cooldown = 0   #num_players-5
                    #pass informaiton between collaboraters
                    if(self.will_collab(p, p2)):
                        p.pass_message(p2)
                        p2.pass_message(p)
                        p.update_probability(player_type[p.a_type])     #maybe change probability after iterating through all players
                        p2.update_probability(player_type[p2.a_type])

                    

        #print the stack of each player to debug
        """for p in self.players:
            s = ""
            for v in p.stack:
                s += "("+str(v.pos_x)+", "+str(v.pos_y)+"), "
            print(str(p.a_id)+":  ")
            print(s)
            print("__________")"""


        #update player positions
        for p in self.players:
            self.pc_coop_walk(p)
            if p.collab_cooldown > 0: p.collab_cooldown -= 1
            p.count += 1
            #self.pc_dfs_random_walk(p)
            #add any player that finished the game just now to p_outofbound
            #and remove those players from self.players
            if self.player_out_of_bound(p):
                self.p_outofbound += 1
                c_temp.append(p.count)
                if p.count not in p.output:
                    p.output[p.count] = 1
                else: p.output[p.count] += 1

                p.visited.clear()
                p.stack.clear()
                p.dead_ends.clear()

                #print("Thread: "+str(threading.get_ident())+", player finished maze")

                self.player_storage.append(p)
                #player_storage[threading.get_ident()].append(p) 
                self.players.remove(p)
                



        

        
        #check if the game is over and all players escaped
        if self.p_outofbound == num_players: 
            #print("FINISHED")
            
            #usefull when programm runs long
            if self.num_it % 20 == 0:
                    print(self.num_it)
            self.num_it -= 1
            if self.num_it > 0:
                #reset all variables and objects
                self.p_outofbound = 0
                self.start = False
                #no need to delete players from gui (already deleted)
                #reinstantiate all players
                self.players.extend(self.player_storage)
                self.player_storage.clear()

                for p in self.players:
                    p.count = 0
                    
                    self.initialize_player_random(p)
                """if gui: 
                    with self.canvas: 
                        Color(0, 0, 0)
                        Rectangle(pos=(0, 0), size=(width, height))
                    self.draw_maze()"""

            else: 
                self.finished = True
                print("done")

    #returns whether two players collaborate
    def will_collab (self, p1, p2):
        rand_num = rand.random()  # Generate a random number between 0 and 1
        return rand_num <= p1.collab_prob * p2.collab_prob    

    """def pc_player(self, dt):
        with self.canvas:
            global num_it
            global solve_maze_step


            if self.finished: return    #maze was finished stop execution
            #overwriting old position with blank
            if not self.start:
                self.start = True
                self.p1.old_x, self.p1.old_y = self.p1.pos_x, self.p1.pos_y
            else:
                Color(0, 0, 0)
                #Gui draw instruction
                if gui: self.draw_player(G.Vertex(self.p1.old_x, self.p1.old_y))
                self.p1.old_x, self.p1.old_y = self.p1.pos_x, self.p1.pos_y


            Color(0, 0, 1)
            #Gui draw instruction
            if gui: self.draw_player(G.Vertex(self.p1.pos_x, self.p1.pos_y))
            
            #call walk function
            self.pc_dfs_random_walk(self.p1)
            #self.pc_dfs_walk (self.p1)

            #draw visited fields


            self.count += 1

            #check if maze was finished
            if self.player_out_of_bound(self.p1):
                self.finished = True
                #print(self.count)
                c_temp.append(self.count)
                
                if num_it % 20 == 0:
                    print(num_it)

                num_it -= 1
                if num_it > 0:
                    #reset some variables
                    self.count = 0
                    self.start = False
                    self.finished = False

                    self.visited.clear()
                    self.stack.clear()                    

                    #create a new maze
                    if new_maze_perIt: 
                        self.maze = G.Graph(size)
                        Color(0, 0, 0)
                        with self.canvas:
                            #Gui draw instruction
                            if gui: Rectangle(points=(0, 0), size=(width, height))
                        self.draw_maze()
                    #Gui draw instruction
                    if gui: self.draw_player(self.p1)
                    #initialze player again to starting position
                    self.initialize_player(self.p1)
                    #self.initialize_player_random(self.p1)
                else: solve_maze_step =len(self.stack)"""

    def player_out_of_bound(self, p):
        return not(0 <= p.pos_x < self.n and 0 <= p.pos_y < self.n)


        
    
    def pc_random_walk (self):
        #trying out movement with check_edge function for random player with no memory
        a = self.maze.check_edge(self.p1)
        
        directions = []     #saves possible current directions  0 = up, 1 = right, 2 = bottom, 3 = left
        for i in range(0, 4):
            if a[i]: directions.append(i)
        
        r = rand.randint(0, len(directions)-1)
        if directions[r] == 0: self.p1.pos_y+=1
        elif directions[r] == 1: self.p1.pos_x+=1
        elif directions[r] == 2: self.p1.pos_y-=1
        else: self.p1.pos_x-=1
    


    #players will always cooperate with each other when they meet each other
    # they will share which places in the maze are 100% dead ends 
    def pc_coop_walk (self, p):
        
        a = self.maze.check_edge(p)
        p.visited.append(G.Vertex(p.pos_x, p.pos_y))

        neighbours = []
        
        neighbours.append(G.Vertex(p.pos_x, p.pos_y + 1))
        neighbours.append(G.Vertex(p.pos_x + 1, p.pos_y))
        neighbours.append(G.Vertex(p.pos_x, p.pos_y - 1))       
        neighbours.append(G.Vertex(p.pos_x - 1, p.pos_y))
        
        directions = []     #saves possible current directions  0 = up, 1 = right, 2 = bottom, 3 = left
        for i in range(0, 4):
            if a[i] and neighbours[i] not in p.visited and neighbours[i] not in p.dead_ends:
                directions.append(i)

        if len(directions) == 0: 
            for i in range(0, 4):
                if a[i] and neighbours[i] not in p.visited:     
                    directions.append(i)
            #if len(p.stack) == 0: return
            if len(directions) == 0: 
                pos = p.stack.pop()
                p.dead_ends.add(G.Vertex(p.pos_x, p.pos_y))
                p.pos_x = pos.pos_x
                p.pos_y = pos.pos_y
                return
        

        r = rand.randint(0, len(directions) - 1)
        if directions[r] == 0:
            p.stack.append(G.Vertex(p.pos_x, p.pos_y))
            p.pos_y+=1
        elif directions[r] == 1: 
            p.stack.append(G.Vertex(p.pos_x, p.pos_y))
            p.pos_x+=1
        elif directions[r] == 2: 
            p.stack.append(G.Vertex(p.pos_x, p.pos_y))
            p.pos_y-=1
        elif directions[r] == 3: 
            p.stack.append(G.Vertex(p.pos_x, p.pos_y))
            p.pos_x-=1
        else: 
            pos = p.stack.pop()
            p.dead_ends.add(G.Vertex(p.pos_x, p.pos_y))
            p.pos_x = pos.pos_x
            p.pos_y = pos.pos_y
      

    #traversing labyrinth in dfs fashion
    def pc_dfs_walk (self, p) :
        a = self.maze.check_edge(p)
        
        self.visited.append([p.pos_x, p.pos_y])
        top_neighbor = [p.pos_x, p.pos_y + 1]
        right_neighbor = [p.pos_x + 1, p.pos_y]
        bottom_neighbor = [p.pos_x, p.pos_y - 1]       
        left_neighbor = [p.pos_x - 1, p.pos_y]
        
        if a[0] and top_neighbor not in self.visited:
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_y+=1
        elif a[1] and right_neighbor not in self.visited:
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_x+=1
        elif a[2] and bottom_neighbor not in self.visited:
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_y-=1
        elif a[3] and left_neighbor not in self.visited:
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_x-=1
        else:
            pos = self.stack.pop()
            p.pos_x = pos[0]
            p.pos_y = pos[1]
    
    def pc_dfs_random_walk(self, p):
        a = self.maze.check_edge(p)
        p.visited.append([p.pos_x, p.pos_y])

        neighbours = []
        
        neighbours.append([p.pos_x, p.pos_y + 1])
        neighbours.append([p.pos_x + 1, p.pos_y])
        neighbours.append([p.pos_x, p.pos_y - 1])       
        neighbours.append([p.pos_x - 1, p.pos_y])
        
        directions = []     #saves possible current directions  0 = up, 1 = right, 2 = bottom, 3 = left
        for i in range(0, 4):
            if a[i] and neighbours[i] not in p.visited: directions.append(i)


        if len(directions) == 0: 
            pos = p.stack.pop()
            p.pos_x = pos[0]
            p.pos_y = pos[1]
            return

        r = rand.randint(0, len(directions) - 1)
        if directions[r] == 0:
            p.stack.append([p.pos_x, p.pos_y])
            p.pos_y+=1
        elif directions[r] == 1: 
            p.stack.append([p.pos_x, p.pos_y])
            p.pos_x+=1
        elif directions[r] == 2: 
            p.stack.append([p.pos_x, p.pos_y])
            p.pos_y-=1
        elif directions[r] == 3: 
            p.stack.append([p.pos_x, p.pos_y])
            p.pos_x-=1
        else: 
            pos = p.stack.pop()
            p.pos_x = pos[0]
            p.pos_y = pos[1]
    
    def player_located (self, pos):
        for p in self.players:
            if [p.pos_x, p.pos_y] == pos:
                return p
        return None    
    
    def pc_cooperative_dfs_random_walk(self, p):
        
        a = self.maze.check_edge(p)
        self.visited.append([p.pos_x, p.pos_y])

        neighbours = []
        
        neighbours.append([p.pos_x, p.pos_y + 1])
        neighbours.append([p.pos_x + 1, p.pos_y])
        neighbours.append([p.pos_x, p.pos_y - 1])       
        neighbours.append([p.pos_x - 1, p.pos_y])
        
        directions = []     #saves possible current directions  0 = up, 1 = right, 2 = bottom, 3 = left
        for i in range(0, 4):
            if a[i] and neighbours[i] not in self.visited: directions.append(i)
            
        if directions[0] and self.player_located([p.pos_x, p.pos_y+1]):
            p.pass_message(self.player_located([p.pos_x, p.pos_y+1]))
        if directions[1] and self.player_located([p.pos_x+1, p.pos_y]):
            p.pass_message(self.player_located([p.pos_x+1, p.pos_y]))
        if directions[0] and self.player_located([p.pos_x, p.pos_y-1]):
            p.pass_message(self.player_located([p.pos_x, p.pos_y-1]))
        if directions[0] and self.player_located([p.pos_x-1, p.pos_y]):
            p.pass_message(self.player_located([p.pos_x-1, p.pos_y]))


        if len(directions) == 0: 
            pos = self.stack.pop()
            p.pos_x = pos[0]
            p.pos_y = pos[1]
            return

        r = rand.randint(0, len(directions) - 1)
        if directions[r] == 0:
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_y+=1
        elif directions[r] == 1: 
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_x+=1
        elif directions[r] == 2: 
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_y-=1
        elif directions[r] == 3: 
            self.stack.append([p.pos_x, p.pos_y])
            p.pos_x-=1
        else: 
            pos = self.stack.pop()
            p.pos_x = pos[0]
            p.pos_y = pos[1]

    #if no collaborator found or if the players don't want to collaborate then the p itself is returned
    def find_collaborator(self, p, a):     
        collaborators = []
        for p2 in self.players:
            if p2.a_id != p.a_id:
                for i in range(0, 4):
                    if a[i] == 0 and p.pos_x == p2.pos_x and p.pos_y+1 == p2.pos_y:
                        #collab possible now check if it actually happens
                        collaborators.append(p2)
                    elif a[i] == 1 and p.pos_x+1 == p2.pos_x and p.pos_y == p2.pos_y:
                        collaborators.append(p2)
                    elif a[i] == 2 and p.pos_x == p2.pos_x and p.pos_y-1 == p2.pos_y:
                        collaborators.append(p2)
                    elif a[i] == 3 and p.pos_x-1 == p2.pos_x and p.pos_y == p2.pos_y:
                        collaborators.append(p2)
                    elif p.a_id != p2.a_id and p.pos_x == p2.pos_x and p.pos_y == p2.pos_y:
                        collaborators.append(p2)
        return collaborators






#IO write c_temp into text file
#
"""output = {}
for i in c_temp:
    if i not in output: output[i] = 1
    else: output[i] += 1"""



"""seconds = time.time()
path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"
#strategy has to be added at this point manually
#coop and non coop has to be added
#Format: maze_size, same_maze, num_it, (strategy), (coop), time
#bracket attributes have to be added
name = str(n)+"_"+str(new_maze_perIt)+"_"+str(iterations-num_it)+"_"+str(num_players)+"_"+str(seconds)+".txt"
name = path+name
file = open(name, "w")

print("terminated")

for p in player_storage:
    file.write("player: "+str(p.a_id)+" "+p.a_type+"\n")
    for i in p.output:
        file.write(str(i)+" "+str(p.output[i])+"\n")


file.close()"""

#





