import graph as G

from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
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


size = 20      #35 still reasonably fast

width = Window.size[0]
height = Window.size[1]

wall_x = width/(size-1)
wall_y = height/(size-1)

maze = G.Graph(size)


class SimGame(Widget):
    pass

class Maze(Widget):

    p1 = (x, y) = (-1, -1)

    def __init__(self, **kwargs):
        super(Maze, self).__init__(**kwargs)
        with self.canvas: 

            #for v in maze.vertices:
                #print(str(v.pos_x) +", "+ str(v.pos_y))
            #    Line(points=(v.pos_x*wall_x, v.pos_y*wall_y, v.pos_x*wall_x, v.pos_y*wall_y), width =2)
            #print all edges from Graph maze
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

        #input keyboard 
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        #input keyboard
    
    
    
    def update(self, dt):
        print("boop")


    def pc_player(self):
        pass
    

class MazeApp(App):
    def build(self):
        simulation = Maze()
        Clock.schedule_interval(simulation.update, 5)
        return simulation


if __name__ == '__main__':
    MazeApp().run()





