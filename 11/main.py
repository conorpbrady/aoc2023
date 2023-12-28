import functools
import time                                                
from tqdm import tqdm
from itertools import combinations

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
    
def expand_space(galaxy_map):
    expand_rows = [True] * len(galaxy_map)
    expand_cols = [True] * len(galaxy_map[0])
    
    for y, line in enumerate(galaxy_map):
        for x, c in enumerate(line):
            if c == '#':
                expand_cols[x] = False
                expand_rows[y] = False
    r_indexes = [i for i, expand in enumerate(expand_rows) if expand]
    c_indexes = [i for i, expand in enumerate(expand_cols) if expand]
    #print(r_indexes)
    #print(c_indexes)
    new_map = []
    for y, line in enumerate(galaxy_map):
        new_line = ''
        for x, c in enumerate(line):
            new_line += c
            if x in c_indexes:
                new_line += '.'
            
        new_map.append(new_line)
        if y in r_indexes:
            new_map.append(new_line)
    return new_map

def expand_rows_cols(galaxy_map):
    expand_rows = [True] * len(galaxy_map)
    expand_cols = [True] * len(galaxy_map[0])
    
    for y, line in enumerate(galaxy_map):
        for x, c in enumerate(line):
            if c == '#':
                expand_cols[x] = False
                expand_rows[y] = False
    r_indexes = [i for i, expand in enumerate(expand_rows) if expand]
    c_indexes = [i for i, expand in enumerate(expand_cols) if expand]
    return r_indexes, c_indexes
    
def find_galaxies(galaxy_map):
    galaxies = []
    for y, line in enumerate(galaxy_map):
        for x, c in enumerate(line): 
            if c == '#':
                galaxies.append((x, y))
    return galaxies


@timer
def part1(galaxy_map):

    galaxy_map = expand_space(galaxy_map)
    galaxies = find_galaxies(galaxy_map)
    galaxy_pairs = list(combinations(galaxies, 2))
    print(len(galaxy_pairs))
    s = 0
    for g1, g2 in galaxy_pairs:
        s += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    print(s)
        
@timer  
def part2(galaxy_map):
    expanded_rows, expanded_cols = expand_rows_cols(galaxy_map)
    galaxies = find_galaxies(galaxy_map)
    galaxy_pairs = list(combinations(galaxies, 2))
    #print(expanded_cols, expanded_rows)
    s = 0
    expand_factor = 1000000
    for g1, g2 in galaxy_pairs:
        e_col_count = 0
        e_row_count = 0
        for r in expanded_rows:
            if (r > g1[1] and r < g2[1]) or (r > g2[1] and r < g1[1]):
                #print(r, g1, g2)
                e_row_count += 1
        for c in expanded_cols:
            if (c > g1[0] and c < g2[0]) or (c > g2[0] and c < g1[0]):
                e_col_count += 1
        #print(g1, g2, e_col_count, e_row_count)
        #print(g1, g2, abs(g1[0] - g2[0]) + (e_col_count * expand_factor) + abs(g1[1] - g2[1]) + (e_row_count * expand_factor))
        s += abs(g1[0] - g2[0]) + (e_col_count * (expand_factor-1)) + abs(g1[1] - g2[1]) + (e_row_count * (expand_factor-1)) 
    print(s)

def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()