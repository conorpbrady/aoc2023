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
    
@timer
def part1(races):
    pass

@timer  
def part2():
    pass

def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()