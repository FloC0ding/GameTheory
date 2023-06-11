import graph as G

class Agent:
    def __init__(self, pos_x, pos_y, old_x, old_y, collab_prob, speed, sight, memory, lab):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.old_x = old_x
        self.old_y = old_y

        self.a_id = 0

        self.count = 0          #each agent counts its own steps

        """self.speed = speed
        self.sight = sight
        self.memory = memory"""

        self.collab_prob = collab_prob  #optional

        self.lab = lab
        self.stack = []
        self.visited = []        
        self.dead_ends = set()
        
            
            
    def get_position (self):
        return [self.pos_x, self.pos_y]
        
    def pass_message(self, agent):
        self.visited_collab.extend(self.visited)
        self.stack_collab.extend(self.stack)    
    