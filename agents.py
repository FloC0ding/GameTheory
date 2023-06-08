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
        self.stack = []
        self.visited = []
        self.visited_collab = []
        self.stack_collab = []
        
        
        #change position x, y attribute to an vertex attribute and maybe add old position into the agent!!!
            
            
    def get_position (self):
        return [self.pos_x, self.pos_y]
        
    def pass_message(self, agent):
        self.visited_collab.append(self.visited)
        self.stack_collab.append(self.stack)    
    