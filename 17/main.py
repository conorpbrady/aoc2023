import functools
import time                                                
from tqdm import tqdm
from colorama import Fore, Back, Style, init
init(convert=True)
import sys
from heapq import heappop, heappush

    
U = (0, -1)
D = (0, 1)
L = (-1, 0)
R = (1, 0)

def draw(path):

    print('--------------------------------')
    print(f'Current Cost: {path[-1].current}')
    ps = [p.position for p in path]
    for y, line in enumerate(MAP):
        for x, c in enumerate(line):
            if (x, y) in ps:
                print(Back.YELLOW, end='')
            print(c, end='')
            print(Style.RESET_ALL, end='')
        print()


#class Block:
#
#    def __init__(self, position, 

class Node:

    def __init__(self, start, direction_history, current=0, estimate=0):
        end_x = len(MAP[0]) - 1
        end_y = len(MAP) - 1
        self.position = start
        self.dh = direction_history
        self.current = current
        self.estimate = (end_x - start[0]) + (end_y - start[1])
        
    def __eq__(self, other):
        return self.current == other.current
    def __gt__(self, other):
        return self.current > other.current
    def __lt__(self, other):
        return self.current < other.current
    def __gte__(self, other):
        return self.current >= other.current
    def __lte__(self, other):
        return self.current <= other.current
        
    def available_directions(self):
        ds = []
        if self.position[0] > 0 and self.dh[-1] != R and self.dh != [L,L,L]:
            ds.append(L)
        if self.position[0] < len(MAP[0])-1 and self.dh[-1] != L and self.dh != [R,R,R]:
            ds.append(R)
        if self.position[1] > 0 and self.dh[-1] != D and self.dh != [U,U,U]:
            ds.append(U)
        if self.position[1] < len(MAP)-1 and self.dh[-1] != U and self.dh != [D,D,D]:
            ds.append(D)
        return ds
    
    @classmethod
    def from_previous(cls, node, direction):
        x = node.position[0] + direction[0]
        y = node.position[1] + direction[1]
        position = (x, y)
        dh = node.dh[1:] + [direction]

        current = node.current + int(MAP[y][x]) 

        return cls(position, dh, current=current)
    
    def ds(self):
        return Node.d_str(self.dh)
        
    @classmethod
    def d_str(self, dh):
        d_str = []
        for d in dh:
            if d == (0, -1):
                d_str.append('U')
            if d == (1, 0):
                d_str.append('R')
            if d == (0, 1):
                d_str.append('D')
            if d == (-1, 0):
                d_str.append('L')
            if d is None:
                d_str += ' '
        return ':'.join(d_str)
                
        
    def __str__(self):
        return f'{self.position} | {self.current} | {Node.d_str(self.dh)}'  
    def __repr__(self):
        return f'{self.position} | {self.current} | {Node.d_str(self.dh)}'       

    


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Finished {repr(func.__name__)} in {round(run_time, 4)} secs')
        return value

    return wrapper

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines

MAP = parse_input('input.txt')

def is_suboptimal_path(path, lowest_cost):
    # Drop path if it contains a position with a path that has been minimized another way
    for p in path:
        if p.position in lowest_cost and p.cost > lowest_cost[p.position]:
            #print(f'dropping path {path}')
            ##print(f'{p.position} | {lowest_cost[p.position]}')
            return True
    return False
def gold_path():
    return [
    (1,0),
    (2,0),
    (2,1),
    (3,1),
    (4,1),
    (5,1),
    (5,0),
    (6,0),
    (7,0),
    (8,0),
    (8,1),
    (8,2),
    (9,2),
    (10,2),
    (10,3),
    (10,4),
    (11,4),
    (11,5),
    (11,6),
    (11,7),
    (12,7),
    (12,8),
    (12,9),
    (12,10),
    (11,10),
    (11,11),
    (11,12),
    (12,12)    
    ]
@timer
def part1():
    start = Node((0,0), [None]*3)
    lowest_cost = {}
    min_path = []
    paths = [[start]]
    all_paths = []
    end = (len(MAP[0])-1, len(MAP)-1)
    #print(end)
    #end = (2, 2)
    debug = True
    while len(paths) > 0:
        path = heappop(paths)
        if (4, 1) in [p.position for p in path]:
            #debug = True
            pass
        else:
            debug = False
        #print('------------')
        #for p in paths:
            #print(p)
        #    pass
        node = path[-1]
        
        if node.position == end:
            all_paths.append(path)
            
            if (end, node.ds()) not in lowest_cost or path[-1].current <= lowest_cost[(end, node.ds())]:
                min_path = path
            
        
        ad = path[-1].available_directions()
        if debug:
            print(f'    {path[-1].position}\t{Node.d_str(ad)}')
        for d in ad:
            new_node = Node.from_previous(path[-1], d)
            if new_node.position in [p.position for p in path]:
                continue
            if (new_node.position, new_node.ds()) in lowest_cost:
                # Factor in estimate / distance to this instead of a flat 30
                if new_node.current >= lowest_cost[(new_node.position, new_node.ds())]:
                    if debug:
                        print(f'      trying to go {Node.d_str([d])} ending path at {new_node.position}, {new_node.current}')
                    continue
            if debug:
                print(f'      marking {new_node.position} current at {new_node.current}')
            #if new_node.position == (5, 0):
                #debug = True
            lowest_cost[(new_node.position, new_node.ds())] = new_node.current
            new_path = path + [new_node]
            #print(path)
            #draw(new_path)
            #input()
            heappush(paths, path + [new_node])
    
    #print(sum([v for k, v in lowest_cost.items() if k[0] == end]))
    mink = ()
    minv = sys.maxsize
    for k, v in lowest_cost.items():
        if k[0] == end:
            if v < minv:
                minv = v
                mink = k
    print(mink, minv)
    for ap in all_paths:
        if mink == (ap[-1].position, ap[-1].ds()) and ap[-1].current == minv:
            draw(ap)
    
    
@timer  
def part2():
    s = 0
    start = Node((0,0), [None]*3)
    gp = gold_path()
    path = [start]
    end = (12,12)
    while path[-1].position != end:
        node = path[-1]
        i = len(path) - 1
        dx = gp[i][0] - node.position[0]
        dy = gp[i][1] - node.position[1]
        new_node = Node.from_previous(node, (dx, dy))
        path.append(new_node)
        
    draw(path)
def main():
    data = parse_input('input.txt')
    
    part1()
    #part2()
    
if __name__ == '__main__':
    main()