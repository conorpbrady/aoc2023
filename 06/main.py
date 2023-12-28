import functools
import time                                                
from tqdm import tqdm
from threading import Thread
import sys
import math

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), round(run_time, 4)))
        return value

    return wrapper

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    times = [int(item) for item in lines[0].split(':')[1].split(' ') if item]
    distances = [int(item) for item in lines[1].split(':')[1].split(' ') if item]
    return list(zip(times, distances))

@timer
def part1(races):
    s = 1
    for r in races:
        race_wins = 0
        for charge in range(r[0]):
            if charge * (r[0] - charge) > r[1]:
                #print(r, charge)
                race_wins += 1
        s *= race_wins       
    print(s)


    
def part2():
    pass

    
def main():
    races = parse_input('input.txt')
    
    part1(races)
    races = parse_input('input2.txt')
    print(races)
    part1(races)
    
if __name__ == '__main__':
    main()