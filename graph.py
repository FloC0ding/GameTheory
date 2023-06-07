import random as rand
import agents as agent

class Vertex:       #x and y are positions in maze
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def __hash__(self):
        return hash((self.pos_x, self.pos_y))
    def __eq__(self, other):
        return (self.pos_x, self.pos_y) == (other.pos_x, other.pos_y)
    def __ne__(self, other): return not (self == other)

class Edge:     
    def __init__(self, x, y, weight):
        self.u = x
        self.v = y
        self.w = weight


#checks if neighbour v is inside the grid and if yes add it to the edges
def add_neighbour(n, u, v, G):
    if (0 <= v.pos_x < n and 0 <= v.pos_y < n):
        w =  rand.random()      #random number between 0 and 1 (float)      (don't change random numbers to any negative numbers)
        #check that symmetric vertices aren't added
        for e in G.edges:
            u1, v1 = e.u, e.v
            if same_vertex(v, u1) and same_vertex(u, v1): return
            if same_vertex(v, v1) and same_vertex(u, u1): return
        G.edges.append(Edge(v, u, w))


def notSame_zhk(u, v, F):
    return helper2(u, F) != helper2(v, F)



def same_vertex(u, v):
    return (u.pos_x, u.pos_y) == (v.pos_x, v.pos_y)

def helper1(u, v, F):
    for i in F:
        for k in F[i]:
            if u == k: 
                for j in F[i]:
                    F[v].append(j)
                F[i] = []
                return

def helper2(v, F):
    for i in F:
        for k in F[i]:
            if v == k:
                return i

class Graph:
    vertices = set()
    edges = []

    #maps verticex a to an array of vertices that are neighbours vertex a
    neighbour_edges = {}
    
    #maybe add edges in format where each vertex saves it's neighbours (dictionary)

    def __init__(self, n):
        if n <= 0: print("ERROR")
        for i in range(0, n):
            for j in range(0, n):
                current_v = Vertex(i, j)
                self.vertices.add(current_v)
                t, l, r, b = Vertex(i, j-1), Vertex(i-1, j), Vertex(i+1, j), Vertex(i, j+1)
                add_neighbour(n, current_v, t, self)
                add_neighbour(n, current_v, l, self)
                add_neighbour(n, current_v, r, self)
                add_neighbour(n, current_v, b, self)
                
        #compute MST on Graph self via Kruskal
                

        mst_edges = []
        F = {}
        
        for v in self.vertices:
            F[v] = [v]


        #add boundary of labyrinth and select exit at random
        (x, y) = (-1, -1)
        r = rand.random()
        if r < 0.25:
            y = 0
        elif r < 0.5:
            x = n-1
        elif r < 0.75:
            y = n-1
        else: x = 0


        #maybe safe exit as attribute of Graph
        exit = Edge(Vertex(-1, -1), Vertex(-1, -1), -1)

        r = rand.randint(0, n-2)+0.5
        if x < 0: 
            x = r
            exit = Edge(Vertex(x-0.5, y), Vertex(x+0.5, y), 1)
        else: 
            y = r
            exit = Edge(Vertex(x, y-0.5), Vertex(x, y+0.5), 1)

        #change weight of border edges except for exit as -1 such that they will always get selected by Kruskal
        for e in self.edges:
            u, v, w = e.u, e.v, e.w
            if(u.pos_x, v.pos_x) == (0, 0) or (u.pos_y, v.pos_y) == (0, 0) or (u.pos_x, v.pos_x) == (n-1, n-1) or (u.pos_y, v.pos_y) == (n-1, n-1):
                if not ((u == exit.u and v == exit.v) or (u == exit.v and v == exit.u)) : #border edge can't be exit
                    e.w = -1 
    

        #sort edges after weight
        e_sorted = sorted(self.edges, key=lambda edge: edge.w)

        for e in e_sorted:
            u, v, w = e.u, e.v, e.w
            #if not(u in F[v]):
            #check if one vertex contains all other vertices
            
            if notSame_zhk(u, v, F):
                

                #delete u and merge into v
                mst_edges.append(Edge(u, v, w))
                #adding symmetric edges not necessary to draw maze      (maybe remove for efficiency)
                mst_edges.append(Edge(v, u, w))    

                zhk_v = helper2(v, F)
                              
                helper1(u, zhk_v, F)

        self.edges = mst_edges

        #implement neighbour edges 
        for v in self.vertices:
            self.neighbour_edges[v] = []

        for e in mst_edges:
            u, v, w = e.u, e.v, e.w
            if not(v in self.neighbour_edges[u]): self.neighbour_edges[u].append(v)
            if not(u in self.neighbour_edges[v]): self.neighbour_edges[v].append(u)

        """for v in self.neighbour_edges:
            s = ""
            for u in self.neighbour_edges[v]:
                s = s+"("+str(u.pos_x)+", "+str(u.pos_y)+"), "
            print("("+str(v.pos_x)+", "+str(v.pos_y)+"): "+s)"""
        

    #returns boolean array with four entries [top, right, bottom, left] each entry tells if there's a wall in this direciton
    #true: no wall, false: wall
    def check_edge(self, agent):      
        
        a = []
        u, v = Vertex(int(agent.pos_x-0.5), int(agent.pos_y+0.5)), Vertex(int(agent.pos_x+0.5), int(agent.pos_y+0.5))
        a.append(self.check_edge_help(u, v))
        u, v = Vertex(int(agent.pos_x+0.5), int(agent.pos_y+0.5)), Vertex(int(agent.pos_x+0.5), int(agent.pos_y-0.5))
        a.append(self.check_edge_help(u, v))
        u, v = Vertex(int(agent.pos_x+0.5), int(agent.pos_y-0.5)), Vertex(int(agent.pos_x-0.5), int(agent.pos_y-0.5))
        a.append(self.check_edge_help(u, v))
        u, v = Vertex(int(agent.pos_x-0.5), int(agent.pos_y+0.5)), Vertex(int(agent.pos_x-0.5), int(agent.pos_y-0.5))
        a.append(self.check_edge_help(u, v))
        return a

    def check_edge_help(self, u, v):
        for k in self.neighbour_edges[v]:
            if k == u: return False
        return True

#printing functions
"""for k in F:
                    print("Vertices in ("+str(k.pos_x)+", "+str(k.pos_y)+"): ")
                    s = ""
                    for m in F[k]:
                        s += "("+str(m.pos_x)+", "+str(m.pos_y)+")"
                    print("     "+s)
                print("______________")"""  
#for e in mst_edges:
                #    u, v, w = e.u, e.v, e.w
                #    print("edge from: ("+str(v.pos_x)+", "+str(v.pos_y)+") , to: ("+str(u.pos_x)+", "+str(u.pos_y)+")")
                #print("Vertex u: ("+str(u.pos_x)+", "+str(u.pos_y)+"), vertex v ("+str(v.pos_x)+", "+str(v.pos_y)+")")                   
    

        


