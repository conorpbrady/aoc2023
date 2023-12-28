import functools
import time                                                
from tqdm import tqdm

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
L = (1, 0)
R = (-1, 0)
DS = [U, D, L, R]


@timer
def part1(m, s, rocks, steps):
    mx = len(m[0])
    my = len(m)
    possible = [s]
    
    for i in range(steps):
        #print(f'Step {i}:')
        #draw(m, rocks, possible)
        #input()
        current_locations = possible[:]
        possible = []
        while current_locations:
            loc = current_locations.pop()

            for d in DS:
                nx = loc[0] + d[0]
                ny = loc[1] + d[1]
                if (nx, ny) not in rocks and nx >= 0 and nx < mx and ny >=0 and ny < my:
                    if (nx, ny) not in possible:
                        possible.append((nx, ny))
                
    return set(possible)

def draw(m, rocks, possible):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if (x, y) in rocks: 
                print('#', end='')
            elif (x, y) in possible:
                print('O', end='')
            else:
                print('.', end='')
        print()
@timer  
def part2(m, s, rocks):
    m = data
    pass


def main():
    data = parse_input('input.txt')
    rocks = []
    start = ()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                rocks.append((x, y))
            if c == 'S':
                start = (x, y)
    print(len(part1(data, start, rocks, 64)))
    #part2(data)
    
if __name__ == '__main__':
    main()