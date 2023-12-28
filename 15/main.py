import functools
import time                                                
from tqdm import tqdm
from collections import defaultdict
import re

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

def hash_alg(s):
    cv = 0
    for c in s:
        cv += ord(c)
        cv *= 17
        cv = cv % 256
    return cv
    
def focus_power(boxes):
    s = 0
    for n, box in boxes.items():
        box_total = 0
        b = (1 + n)
        for i, k in enumerate(box.keys()):
            slot = i + 1
            fl = box[k]
            box_total += b * slot * fl
        s += box_total
    return s
    
@timer
def part1(lines):
    steps = lines[0].split(',')
    s = 0
    for step in steps:
        v = hash_alg(step)
        #print(step, v)
        s += v
    print(s)
        
        
@timer  
def part2(lines):
    boxes = defaultdict(dict)
    # { 0: [{'rn': 1}, {'cm': 2}] }
    
    steps = lines[0].split(',')
    for step in steps:
        f = step.find('-')
        if f == -1:
            f = step.find('=')
            n = int(step.split('=')[1])
            s = step.split('=')[0]
            box = hash_alg(s)
            boxes[box].update({s: n})
        else:
            s = step.split('-')[0]
            box = hash_alg(s)
            boxes[box].pop(s, None)
            
    print(focus_power(boxes))
        
        
        
        
def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()