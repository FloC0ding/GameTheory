#imports from own files
import graph as G
import agents as A

#import from matplotlib and kivy
#import matplotlib.pyplot as plt
#from collections import Counter

from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.clock import *
#from kivy.properties import (
#    NumericProperty, ReferenceListProperty, ObjectProperty
#)
from kivy.vector import Vector

#python imports
import random as rand
import time
import getpass


size = 21        #35 still reasonably fast(creating maze)
n = size-1      #number of fields of the labyrinth per row or line

width = Window.size[0]
height = Window.size[1]

wall_x = width/(n)
wall_y = height/(n)


#player
p_size = 5

#simulation settings
update_speed = 0.5  #number of seconds for which the update function is called
num_it = 100
iterations = num_it
c_temp = []
new_maze_perIt = False
gui = True

#counts the minimal number of steps to escape works only for same_maze
solve_maze_step = 0
#cooperative parameters
num_players = 1
p_outofbound = 0


class SimGame(Widget):
    pass

class Maze(Widget):



    def __init__(self, **kwargs):
        super(Maze, self).__init__(**kwargs)

        #initialize variables
        self.maze = G.Graph(size) 
        self.start = False
        self.finished = False
        self.draw_maze()
        #initialize variables non_coop
        self.count = 0
        self.p1 = A.Agent(-1, -1, -1, -1, 0, 0, [], 0, 0)
        self.visited = []
        self.stack = []
        
        self.initialize_player(self.p1)

        #implement cooperative game mode
        self.players = []
        id = 0
        for i in range(0, num_players):
            p = A.Agent(-1, -1, -1, -1, 0, 0, [], 0, 0)
            p.a_id = id
            id += 1
            self.players.append(p)
            self.initialize_player_random(p)
            


    def initialize_player(self, p):
         #initialize p1 position
        if n % 2 == 0:
            p.pos_x = (n+1)/2
            p.pos_y = (n+1)/2
        else :
            p.pos_x = n/2
            p.pos_y = n/2
    
    def initialize_player_random(self, p):
        p.pos_x = rand.randint(0, n-1) + 0.5
        p.pos_y = rand.randint(0, n-1) + 0.5


    def pc_cooperative(self, dt):
        global num_it
        global p_outofbound

        if self.finished: 
            return

        #update old position of players and overdraw them if necessary
        if self.start:
            with self.canvas:
                Color(0, 0, 0)
            if gui:
                for p in self.players:
                    self.draw_player(G.Vertex(p.old_x, p.old_y))
                    p.old_x, p.old_y = p.pos_x, p.pos_y
        else: 
            self.start = True
            for p in self.players:
                p.old_x, p.old_y = p.pos_x, p.pos_y

        #draw fields of visited, stack and dead branches here
        """if gui: 
            for p in self.players:
                with self.canvas:   Color(0, 1, 1)  #Turqoise
                for v in p.visited:
                    self.draw_field(v)
                for v in p.stack:
                    with self.canvas: Color(0, 1, 0)    #Green
                    self.draw_field(v)
                for v in p.dead_ends:
                    with self.canvas: Color(0.5, 0.5, 1)    #Purple
                    self.draw_field(v)"""

        #draw players
        if gui: 
            with self.canvas:
                #add distinct colour for each player
                r, g, b = rand.uniform(0.5, 1), rand.uniform(0.5, 1), rand.uniform(0.5, 1)
                Color(r, g, b)
            for p in self.players:
                self.draw_player(p)

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
                p_outofbound += 1
                c_temp.append(p.count)
                p.visited.clear()
                p.stack.clear()

                self.players.remove(p)
                



        

        
        #check if the game is over and all players escaped
        if p_outofbound == num_players: 
            #print("FINISHED")
            
            #usefull when programm runs long
            if num_it % 100 == 0:
                    print(num_it)
            num_it -= 1
            if num_it > 0:
                #reset all variables and objects
                p_outofbound = 0
                self.start = False
                #no need to delete players from gui (already deleted)
                #reinstantiate all players
                id = 0
                for i in range(0, num_players):
                    p = A.Agent(-1, -1, -1, -1, 0, 0, [], 0, 0)
                    p.a_id = id
                    id += 1
                    self.players.append(p)
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

    def pc_player(self, dt):
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
                else: solve_maze_step =len(self.stack)

    def player_out_of_bound(self, p):
        return not(0 <= p.pos_x < n and 0 <= p.pos_y < n)


        
    
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
            print("test")
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

    def draw_field(self, p):
        with self.canvas:
            Rectangle(pos=((p.pos_x-0.5)*wall_x+4, (p.pos_y-0.5)*wall_y+4), size=(wall_x-8, wall_y-8))

    #draws p1 at his current position, needs to be changed to accept an Agent object and draw this object
    def draw_maze(self):
        with self.canvas:
            for e in self.maze.edges:
                    u, v, w = e.u, e.v, e.w
                    Color(1, 0, 0)
                    #Gui draw instruction
                    if gui: Line(points=(u.pos_x*wall_x, u.pos_y*wall_y, v.pos_x*wall_x, v.pos_y*wall_y), width = 4)

    def draw_player(self):
        with self.canvas:
            Rectangle(pos=((self.p1.pos_x) * wall_x - p_size/2, (self.p1.pos_y) * wall_y- p_size/2), size=(p_size, p_size))

    def draw_player(self, v):
        with self.canvas:
            Rectangle(pos=((v.pos_x) * wall_x - p_size/2, (v.pos_y) * wall_y- p_size/2), size=(p_size, p_size))

class MazeApp(App):
    def build(self):
        simulation = Maze()
        Clock.schedule_interval(simulation.pc_cooperative, update_speed)        
        #Clock.schedule_interval(simulation.pc_player, update_speed)
        return simulation

if __name__ == '__main__':
    MazeApp().run()


#IO write c_temp into text file
#
output = {}
for i in c_temp:
    if i not in output: output[i] = 1
    else: output[i] += 1


seconds = time.time()
path = "C:/Users/"+getpass.getuser()+"/git/Game Theory/Maze_Measuring_Data/"
#strategy has to be added at this point manually
#coop and non coop has to be added
#Format: maze_size, same_maze, num_it, (strategy), (coop), time
#bracket attributes have to be added
name = str(n)+"_"+str(new_maze_perIt)+"_"+str(iterations-num_it)+"_"+str(num_players)+"_"+str(seconds)+".txt"
name = path+name
file = open(name, "w")

for i in output:
    file.write(str(i)+" "+str(output[i])+"\n")


file.close()

#


"""counter = Counter(c_temp)
values = list(counter.keys())
frequencies = list(counter.values())

# Set up the bar graph
plt.bar(values, frequencies)

# Customize x-axis tick labels
x_ticks = [f'{i}' for i in range(min(values), max(values) + 1, 5)]
plt.xticks(range(min(values), max(values) + 1, 5), x_ticks)

# Add labels and title
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Value Frequency Bar Graph')

# Display the bar graph
plt.show()   """



