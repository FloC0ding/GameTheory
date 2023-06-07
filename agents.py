import graph as G

class Agent:
    def __init__(self, pos_x, pos_y, old_x, old_y, collab_prob, speed, sight, memory, lab):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.old_x = old_x
        self.old_y = old_y
        self.speed = speed
        self.sight = sight
        self.memory = memory
        self.collab_prob = collab_prob
        self.lab = lab
        
        #change position x, y attribute to an vertex attribute and maybe add old position into the agent!!!
        
    def move_x (self, value, min_x, max_x):
        if value > 0:
            while value > 0 and self.pos_x <= max_x:
                if(not self.lab.check_edge([self.pos_x, self.pos_y], [self.pos_x + 1, self.pos_y])) :
                    self.pos_x += 1
                    value -= 1
                else:
                    break
        else:
            while value < 0 and self.pos_x >= min_x:
                if(not self.lab.check_edge([self.pos_x, self.pos_y], [self.pos_x - 1, self.pos_y])) :
                    self.pos_x -= 1
                    value += 1
                else:
                    break
        
            
    
    def move_y (self, value, min_y, max_y):
        if value > 0:
            while value > 0 and self.pos_y <= max_y:
                if(not self.lab.check_edge([self.pos_x, self.pos_y], [self.pos_x, self.pos_y + 1])) :
                    self.pos_y += 1
                    value -= 1
                else:
                    break
        else:
            while value < 0 and self.pos_x >= min_y:
                if(not self.lab.check_edge([self.pos_x, self.pos_y], [self.pos_x, self.pos_y - 1])) :
                    self.pos_y -= 1
                    value += 1
                else:
                    break
            
            
    def get_position (self):
        return [self.pos_x, self.pos_y]
        
        
    