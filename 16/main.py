import functools
import time                                                
from tqdm import tqdm


U = (0, -1)
L = (-1, 0)
D = (0, 1)
R = (1, 0)

DIRS = [U, L, D, R]

REFLECT = {
    '/': {
        U: False,
        D: False,
        L: True,
        R: True
        },
    '\\': {
        U: True,
        D: True,
        L: False,
        R: False
        }
        }
        
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

def rotate(d, clockwise):
    i = DIRS.index(d)
    if clockwise:
        return DIRS[(i+1) % 4]
    else:
        return DIRS[(i-1) % 4]
        
def path_print(path):
    n = []
    for p in path:
        x, y, d = p
        c = ''
        if d == (0, -1):
            c = 'U'
        if d == (1, 0):
            c = 'R'
        if d == (0, 1):
            c = 'D'
        if d == (-1, 0):
            c = 'L'
        n.append((x, y, c))
    return n

def count_points(points):
    unique_points = []
    for p in points:
        unique_points.append((p[0], p[1]))
    return len(set(unique_points))
    
#@timer
def part1(start):
    traveled = []
    paths = [start]
    mx = len(MAP[0])
    my = len(MAP)
    
    while len(paths) > 0:
        #print(len(paths))
        path = paths.pop(0)
        #print('Path')
        #print(path)
        while path[-1] not in traveled:
            x, y, d = path[-1]
            traveled.append(path[-1])
            #print(x, y, d)
            c = MAP[y][x]
            if c == '\\' or c == '/':

                clockwise = REFLECT[c][d]
                d = rotate(d, clockwise)
                if y + d[1] < my and y + d[1] >= 0 and x + d[0] < mx and x + d[0] >= 0:
                    path.append((x + d[0], y + d[1], d))
                
            
            elif c == '-' and (d == U or d == D):

                # Left
                if x + L[0] < mx and x + L[0] >= 0:
                    l_path = path + [(x + L[0], y, L)]
                    paths.append(l_path)
                    
                # Right
                if x + R[0] < mx and x + R[0] >= 0:
                    r_path = path + [(x + R[0], y, R)]
                    paths.append(r_path)

                break
            elif c == '|' and (d == L or d == R):

                # Up
                if y + U[1] < my and y + U[1] >= 0:
                    u_path = path + [(x, y+U[1], U)]
                    paths.append(u_path)
                    
                # Down
                if y + D[1] < my and y + D[1] >= 0:
                    d_path = path + [(x, y+D[1], D)]
                    paths.append(d_path)

                break
            else:
                # Continue
                if y + d[1] < my and y + d[1] >= 0 and x + d[0] < mx and x + d[0] >= 0:
                    path.append((x + d[0], y + d[1], d))
    
        for p in paths:
            #traveled += p
            #print(path_print(p))
            pass
        #print('---')
    #print(traveled)
    return count_points(traveled)
    

@timer  
def part2():
    num_energized = []
    mx = len(MAP[0])
    my = len(MAP)
    for x in range(mx):
        print(x)
        num_energized.append(part1([(x, 0, D)]))
        num_energized.append(part1([(x, my-1, U)]))
    print('Up/Down complete')
    for y in range(my):
        print(y)
        num_energized.append(part1([(0, y, R)]))
        num_energized.append(part1([(mx-1, y, L)]))
    print(max(num_energized))
    
def main():
    
    
    s = part1([(0, 0, R)])
    print(s)
    
    part2()
    
if __name__ == '__main__':
    main()