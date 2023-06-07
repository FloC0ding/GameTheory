import graph as G
import agents as A

from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.clock import *
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector

import random as rand



size = 10       #35 still reasonably fast
n = size-1      #number of fields of the labyrinth per row or line

width = Window.size[0]
height = Window.size[1]

wall_x = width/(n)
wall_y = height/(n)

maze = G.Graph(size)

#player
p_size = 10




class SimGame(Widget):
    pass

class Maze(Widget):

    start = False
    old_pos = G.Vertex(-1, -1)
    p1 = A.Agent(-1, -1, 0, 0, 0, 0, 0)

    def __init__(self, **kwargs):
        super(Maze, self).__init__(**kwargs)
        with self.canvas: 

            Color(1, 0, 0)
            for e in maze.edges:
                u, v, w = e.u, e.v, e.w
                if(rand.randint(0, 100) < 50): Color(w+4, 0, 0)
                else: Color(0, w+4, 0)
                
                Line(points=(u.pos_x*wall_x, u.pos_y*wall_y, v.pos_x*wall_x, v.pos_y*wall_y), width = 4)

        with self.canvas.before:
            pass
        with self.canvas.after:
            pass

        #initialize p1 position
        if n % 2 == 0:
            self.p1.pos_x = (n+1)/2
            self.p1.pos_y = (n+1)/2
        else :
            self.p1.pos_x = n/2
            self.p1.pos_y = n/2

        print

        a = maze.check_edge(self.p1)
        """print(a)
        print(self.p1.pos_x)
        print(self.p1.pos_y)"""
        
        #self.player = Agent(rand.randint(0,size), rand.randint(0,size), 0, 0, 0)

    
    
    def update(self, dt):
        print("boop")


    def pc_player(self, dt):
        with self.canvas:

            Color(0, 0, 1)
            self.draw_player()

            print("_____________")
            print(self.p1.pos_x)
            print(self.p1.pos_y)

            #trying out movement with check_edge function for random player with no memory
            a = maze.check_edge(self.p1)

            print("directions: ")
            print(a)

            directions = []     #saves possible current directions  0 = up, 1 = right, 2 = bottom, 3 = left
            for i in range(0, 4):
                if a[i]: directions.append(i)
            
            r = rand.randint(0, len(directions)-1)
            if directions[r] == 0: self.p1.pos_y+=1
            elif directions[r] == 1: self.p1.pos_x+=1
            elif directions[r] == 2: self.p1.pos_y-=1
            else: self.p1.pos_x-=1




    #draws p1 at his current position, can be changed to accept an Agent object and draw this object
    def draw_player(self):
        with self.canvas:
            Rectangle(pos=((self.p1.pos_x) * wall_x - p_size/2, (self.p1.pos_y) * wall_y- p_size/2), size=(p_size, p_size))


class MazeApp(App):
    def build(self):
        simulation = Maze()
        Clock.schedule_interval(simulation.pc_player, 0.1)
        return simulation


if __name__ == '__main__':
    MazeApp().run()





