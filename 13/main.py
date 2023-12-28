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
        patterns = f.read().split('\n\n')
    return [[l.strip() for l in p.split('\n')] for p in patterns]

def transpose(pattern):
    new_pattern = []
    for i in range(len(pattern[0])):
        new_line = ''
        for j in range(len(pattern)):
            new_line += pattern[j][i]
        new_pattern.append(new_line)
    return new_pattern
       
def is_off_by_one(a, b):
    # Converts # to 1 and . to 0
    a_num = [[1 if x =='#' else 0 for x in line] for line in a]
    b_num = [[1 if x =='#' else 0 for x in line] for line in b]
    
    v = 0
    for i, x in enumerate(a_num):
        for j, y in enumerate(x):
            v += abs(y - b_num[i][j])
    return v == 1
    
def find_by_lines(pattern, use_off_by_one):

    all_pats = [pattern, pattern[::-1]]
    for x, p in enumerate(all_pats):
        for i in range(1, math.floor(len(p) / 2) + 1):
            
            top = p[:i]
            bot = p[i:i*2]
            bot.reverse()
            
            if (not use_off_by_one and top == bot) or (use_off_by_one and is_off_by_one(top, bot)):
                return len(p) - i if x else i
    return 0

def find_mirrors(patterns, off_by_one=False, output=False):

    v = 0
    h = 0
    for pattern in patterns:
        dh = find_by_lines(pattern, off_by_one)
        dv = find_by_lines(transpose(pattern), off_by_one)
        v += dv
        h += dh
        if output:
            for y, line in enumerate(pattern):
                if y == dh and dh > 0:
                    print('-' * len(line))
                for x, c in enumerate(line):
                    if x == dv and dv > 0:
                        print('|', end='')
                    print(c, end='')
                print()
            print()

    return (h * 100 + v)        

@timer
def part1(patterns):
    print(find_mirrors(patterns))
    
@timer  
def part2(patterns):
    print(find_mirrors(patterns, off_by_one=True))

def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()