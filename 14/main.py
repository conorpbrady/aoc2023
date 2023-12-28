import functools
import time                                                
from tqdm import tqdm
import re
import math

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
        lines = [l.strip() for l in f.readlines()]
    return lines

def transpose(pattern):
    new_pattern = []
    for i in range(len(pattern[0])):
        new_line = ''
        for j in range(len(pattern)):
            new_line += pattern[j][i]
        new_pattern.append(new_line)
    return new_pattern
       
@timer
def part1(patterns):
    rounds = []
    cubes = []
    for y, line in enumerate(patterns):
        for x, c in enumerate(line):
            if c == 'O':
                rounds.append((x, y))
            if c == '#':
                cubes.append((x, y))
    
    total = 0
    
    for x in range(len(patterns[0])):
        nearest_cube = (0, -1)
        round_count = 0
        load = 0
        for y in range(len(patterns)):
            if (x, y) in cubes:
                top_value = len(patterns) - nearest_cube[1] - 1
                load_values = [i for i in range(top_value, top_value - round_count, -1)]
                load  = sum(load_values)
                total += load
                #if load_values:
                    #print((x, y), nearest_cube, load_values)
                nearest_cube = (x, y)
                round_count = 0
            if (x, y) in rounds:
                round_count += 1
        
        top_value = len(patterns) - nearest_cube[1] - 1
        load_values = [i for i in range(top_value, top_value - round_count, -1)]
        #if load_values:
            #print((x, y), nearest_cube, load_values)
        load  = sum(load_values)
        total += load
            
        #print()   
    print(total)
            
            
N = (0, 1)
S = (0, -1)
W = (1, 0)
E = (-1, 0)

CYCLE = [N, W, S, E]

def calc_load(rounds, max_y):
    s = 0
    for r in rounds:
        s += max_y - r[1]
    return s
def print_rocks(cubes, rounds, mx, my):

    for y in range(my):
        for x in range(mx):
            if (x, y) in rounds:
                print('O', end='')
            elif (x, y) in cubes:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

@functools.cache  
def shift(cubes, rounds, max_y, max_x, d):

    if d == N:
        edge = -1
        step = 1
        start = 0
        end = max_y
    if d == S:
        edge = max_y
        step = -1
        start = max_y
        end = -1
    if d == W:
        edge = -1
        step = 1
        start = 0
        end = max_x
    if d == E:
        edge = max_x
        step = -1
        start = max_x
        end = -1
    
    new_rounds = []
    
    if d == E or d == W:
        for y in range(max_y):
            nearest_cube = edge
            round_count = 0
            for x in range(start, end, step):
                if (x, y) in cubes:
                    #print(y, x, nearest_cube+d[0], nearest_cube+d[0]+(round_count * d[0]))
                    new_rounds += [(i, y) for i in range(nearest_cube+d[0], nearest_cube+d[0]+(round_count * d[0]), step)]
                    #print(new_rounds)
                    nearest_cube = x
                    round_count = 0
                if (x, y) in rounds:
                    round_count += 1    
            #print(y, x, nearest_cube+d[0], nearest_cube+d[0]+(round_count * d[0]))
            new_rounds += [(i, y) for i in range(nearest_cube+d[0], nearest_cube+d[0]+(round_count * d[0]), step)]
            #print(new_rounds)
            
    if d == S or d == N:
        for x in range(max_x):
            nearest_cube = edge
            round_count = 0
            for y in range(start, end, step):
                if (x, y) in cubes:
                    #print(x, nearest_cube+d[1], nearest_cube+d[1]+(round_count * d[1]))
                    new_rounds += [(x, i) for i in range(nearest_cube+d[1], nearest_cube+d[1]+(round_count * d[1]), step)]
                    #print(new_rounds)
                    nearest_cube = y
                    round_count = 0
                if (x, y) in rounds:
                    round_count += 1    
            #print(x, nearest_cube+d[1], nearest_cube+d[1]+(round_count * d[1]))
            new_rounds += [(x, i) for i in range(nearest_cube+d[1], nearest_cube+d[1]+(round_count * d[1]), step)]
            #print(new_rounds)
    #print(d, len(rounds), len(new_rounds))
    #print('before')
    #print_rocks(cubes, rounds, max_x, max_y)
    #print('after')
    #print_rocks(cubes, new_rounds, max_x, max_y)
    return tuple(new_rounds)

#Searches for repeating sequence in list
def find_seq(l):
    max_len = len(l)
    for i in range(0, max_len):
        for j in range(2, max_len):
            print(l[j:i+j], l[i+j:j+i*2])
            if l[j:i+j] == l[i+j:j+i*2]:
                return j
    return 1

def hm(rounds, mx, my):
    hm = ''
    for y in range(my):
        line = ''
        for x in range(mx):
            if (x, y) in rounds:
                line += 'O'
            else:
                line += '.'
        hm += line + '\n'
    return hm
            
    
@timer  
def part2(patterns):
    rounds = []
    cubes = []
    rounds_hist = {}
    for y, line in enumerate(patterns):
        for x, c in enumerate(line):
            if c == 'O':
                rounds.append((x, y))
            if c == '#':
                cubes.append((x, y))
    rounds = tuple(rounds)
    cubes = tuple(cubes)
    output = False
    max_cycles = 1000000000
    my = len(patterns)
    mx = len(patterns[0])
    for i in range(1, max_cycles+1):
        if i % 10 == 0:
            print(i)
        for c in CYCLE:
            rounds = shift(cubes, rounds, len(patterns), len(patterns[0]), c)
        if output:
            print(f'After cycle {i+1}')
            print_rocks(cubes, rounds, len(patterns[0]), len(patterns))
        #print(i, calc_load(rounds, len(patterns)), rounds)
        curr_hm = hm(rounds, mx, my)
        if curr_hm in rounds_hist:
            #print(i, calc_load(rounds, len(patterns)))
            break           
        else:
            #print(i, calc_load(rounds, len(patterns)))
            rounds_hist[curr_hm] = calc_load(rounds, my)
    

    cycle_start =  list(rounds_hist.keys()).index(hm(rounds, mx, my))+1
    cycle_length = i - cycle_start
    at_max = ((max_cycles+cycle_start) % cycle_length)
    #print(cycle_start, cycle_length, at_max)
    #load_at_max = calc_load(rounds_hist[cycle_start + at_max+1], len(patterns))

    print(rounds_hist[list(rounds_hist.keys())[cycle_start + at_max-1]])
    print(rounds_hist[list(rounds_hist.keys())[cycle_start + at_max]])
    print(rounds_hist[list(rounds_hist.keys())[cycle_start + at_max+1]])
def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()