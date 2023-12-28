import functools
import time                                                
from tqdm import tqdm
from colorama import Fore, Back, Style, init
init(convert=True)
import sys
from heapq import heappop, heappush

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
        lines = [[int(x) for x in line.strip()] for line in f.readlines()]
    return lines

MAP = parse_input('input.txt')

U = (0, -1)
D = (0, 1)
L = (-1, 0)
R = (1, 0)
DS = {U: 'U', D: 'D', L: 'L', R: 'R'}
        

def find_path(minl, maxl):
    
    # Node
    # cost, x, y, dir
    
    # Add starting point to queue
    queue = [(0, 0, 0, R, 1, ''), (0, 0, 0, D, 1, '')]
    end = (len(MAP[0]) - 1, len(MAP) - 1)
    # Create set of visited points
    visited = set()
    # Create dict of costs
    
    # While queue
    while len(queue) > 0:
        # Pop
        cost, x, y, d, dc, dh = heappop(queue)
        #print(cost, x, y, DS[d], dc, dh)
        #input()
        #for q in queue:
        #    print(q)
        #input()
        # if visited point, drop
        if (x, y, d, dc) in visited:
            #print('visited already')
            continue
        # add to visited points
        visited.add((x, y, d, dc))
        
        nx = x + d[0]
        ny = y + d[1]
        # Drop if path is out of map bounds
        if ny not in range(len(MAP)) or nx not in range(len(MAP[0])):
            #print('oob')
            continue
        
        ncost = cost + MAP[ny][nx]
        # if reached goal, return cost
        if (nx, ny) == end:
            return ncost, dh
        
        # get directions, add valid directions to queue
        for nd in [U, D, L, R]:
            # don't go back
            
            if d[0] + nd[0] == 0 and d[1] + nd[1] == 0:
                #print('reverse')
                continue
            if nd != d and dc < minl: # Must go min of tiles in one direction
                continue
            if nd == d and dc >= maxl: # Don't exceed max in one direction
                #print('have to turn')
                continue
            if nd == d:
                ndc = dc + 1
            else:
                ndc = 1

            heappush(queue, (ncost, nx, ny, nd, ndc, dh+DS[nd]))
        
        
    
@timer
def part1():
    print(find_path(1, 3))
@timer
def part2():
    print(find_path(4, 10))
def main():    

    print(part1())
    print(part2())
    
if __name__ == '__main__':
    main()