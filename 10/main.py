import functools
import time                                                
from tqdm import tqdm

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines
    
UP = (0, -1)
DN = (0, 1)
LT = (-1, 0)
RT = (1, 0)
MAP = parse_input('input.txt')

STEPS = [UP, DN, LT, RT]

PIPES = {
    '|': [(0, -1), (0, 1)],
    '-': [(1, 0), (-1, 0)],
    'F': [(1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(-1, 0), (0, 1)],
    'L': [(1, 0), (0, -1)],
    '.': [],
    'S': []
    }

VERT_PIPES = list('|LJS')
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

def is_valid_step(x, y, step):
    if y + step[1] < 0 or x + step[1] < 0:
        return False
    if y + step[1] > len(MAP) or x + step[0] > len(MAP[0]):
        return False
    next_pipe = MAP[y+step[1]][x+step[0]]
    return (step[0] * -1, step[1] * -1) in PIPES[next_pipe]

def starting_point():
    for y, line in enumerate(MAP):
        for x, c in enumerate(line):
            if c == 'S':
                return (x, y)
                
@timer
def part1():
    current_positions = [(starting_point(), STEPS, 0)]
    steps_taken = {}
    i = 0
    
    while len(current_positions) > 0:
        (x, y), next_steps, num_steps = current_positions.pop(0)
        steps_taken[(x, y)] = num_steps
        #i += 1
        #if i % 1000 == 0:
            #print(i)
        for step in next_steps:
            #print(x, y, step)
            if is_valid_step(x, y, step):
                new_pos = (x+step[0], y+step[1])
                new_pipe = MAP[new_pos[1]][new_pos[0]]
                inflow = PIPES[new_pipe][:]
                inflow.remove((step[0] * -1, step[1] * -1))
                
                if new_pos in steps_taken.keys():
                    max_pos = max(steps_taken, key = steps_taken.get)
                    print(max_pos, steps_taken[max_pos])
                    #print(new_pos, steps_taken[new_pos])
                    return steps_taken
                
                current_positions.append((new_pos, inflow, num_steps+1))
        #print(current_positions)

@timer  
def part2():
    main_loop = part1()
    #print(main_loop.keys())
    inside_points = []
    for y, line in enumerate(MAP):
        for x, c in enumerate(line):
            if (x, y) in main_loop:
                #print(MAP[y][x], end='')
                continue
            verts = 0
            for i in range(x, 0, -1):
                if MAP[y][x-i] in VERT_PIPES and (x-i, y) in main_loop:
                    #print((x, y)
                    #print((y, x-i))
                    verts += 1
            if verts % 2 == 1:
                #print('I', end='')
                inside_points.append((x, y))
            else:
                #print(MAP[y][x], end='')
                pass
                
        #print()
    #print(inside_points)
    print(len(inside_points))
 
def main():

    #part1()
    part2()
    
if __name__ == '__main__':
    main()