import graph as G

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



size = 4       #35 still reasonably fast
n = size-1      #number of fields of the labyrinth per row or line

width = Window.size[0]
height = Window.size[1]

wall_x = width/(size-1)
wall_y = height/(size-1)

maze = G.Graph(size)

#player
p_size = 10


class SimGame(Widget):
    pass

class Maze(Widget):
    #p1
    p1 = (n*wall_x/2, n*wall_y/2)

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

        #input keyboard 
        """super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)"""
        #input keyboard
    
    
    def update(self, dt):
        print("boop")


    def pc_player(self, dt):
        with self.canvas:
            Color(0, 0, 1)
            if size % 2 == 1: Rectangle(pos=(size * wall_x/2 - p_size/2, size* wall_y/2 - p_size/2), size=(p_size, p_size))    
            else : Rectangle(pos=((size-1) * wall_x/2 - p_size/2, (size-1)* wall_y/2 - p_size/2), size=(p_size, p_size)) 

class MazeApp(App):
    def build(self):
        simulation = Maze()
        Clock.schedule_interval(simulation.pc_player, 2)
        return simulation


if __name__ == '__main__':
    MazeApp().run()





