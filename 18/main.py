import functools
import time                                                
from tqdm import tqdm
from operator import itemgetter
from itertools import *

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

U = (0, -1)
D = (0, 1)
L = (-1, 0)
R = (1, 0)
DS = {U: 'U', D: 'D', L: 'L', R: 'R'}
DI = {'U': U, 'D': D, 'L': L, 'R': R}
DRAW = False

def draw(lb, ub, rb, db, points):
    for y in range(ub, db+1):
        for x in range(lb, rb+1):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()

def verticals(values, y, points):
    return [v for v in values if (v, y-1) in points]
        
def count_inside(lb, ub, rb, db, points):
    count = 0
    inside = []
    debug = False
    line_debug = False
    for y in range(ub-1, db+2):
        x_values = [x for x, ty in points if ty == y]
        x_values.sort()
        verts = verticals(x_values, y, points)
        # counts = []
        # for v in range(int(len(verts) / 2)):
            # counts += range(verts[v], verts[v+1])
        # count += sum(counts)
        # if DRAW:
            # [inside.append(x, y) for x in counts]
        
        if line_debug:
            if (y - ub) == 33 - 1:
               debug = True
            else:
                debug = False
    
        if debug:
            print(x_values)
            print(y, verts)
        passed_verts = 0
        for x in range(lb, rb+1):
            if x in x_values:
                count += 1
                if verts and x > verts[0]:
                    passed_verts += 1
                    verts.pop(0)
            else:
                if len(verts) == 0:
                    break
                if x > verts[0]:
                    passed_verts += 1
                    verts.pop(0)
                    
                
 
                x_odd = passed_verts % 2 == 1 and (len(verts) % 2) == 1
                if debug:
                    print(x, y, passed_verts, len(verts), x_odd, verts[0], x > verts[0])
                if x_odd:
                    count += 1
                    #if DRAW:
                    #inside.append((x, y))
                   


    return count, inside
        
@timer
def part1(lines):
    trench_points = [(0,0)]
    for line in lines:
        d, l, color = line.split(' ')
        l = int(l)
        x, y = trench_points[-1]
        trench_points += [(x + DI[d][0] * i, y + DI[d][1] * i) for i in range(1, l+1)]
    #print(trench_points)
    lb = min([x[0] for x in trench_points])
    ub = min([x[1] for x in trench_points])
    rb = max([x[0] for x in trench_points])
    db = max([x[1] for x in trench_points])
    c, inside = count_inside(lb, ub, rb, db, list(set(trench_points)))
    if DRAW:
        draw(lb, ub, rb, db, trench_points + inside)
    print(len(trench_points + inside))
    print(c)
    
    
        
        

@timer  
def part2(lines):
    vertices = [(0,0)]
    for line in lines:
        d, l, color = line.split(' ')
        #part1
        #l = int(l)
        #d = DI[d]
        #part2
        l = int(color[2:7], 16)
        d = [R, D, L, U][int(color[7])]
        x, y = vertices[-1]
        vertices.append((x + d[0] * l, y + d[1] * l))
    #print(vertices)
    area = 0
    p = 0
    for v in range(len(vertices)-1):
        
        x1, y1 = vertices[v]
        x2, y2 = vertices[v+1]
        p += abs(x2 - x1) + abs(y2 - y1)
        a = (x1 * y2) - (x2 * y1)
        #print(a, p, (x1, y1), (x2, y2))
        area += a
    #print(area / 2, p / 2  )
    print(int((area / 2) + (p / 2) + 1))
    
        


def main():
    data = parse_input('input.txt')
    
    # 121583 too high
    # 137960
    # 137490
    # Too low 108844
    # TOo low 108855
    part1(data)
    

    part2(data)
    
if __name__ == '__main__':
    main()