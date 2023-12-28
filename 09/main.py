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

def calc_diff(hist_list, backwards=False):
    if len(set(hist_list)) == 1: # If All values are the same
        return hist_list[0]
    else:
        diffs = [j-i for i, j in zip(hist_list[:-1], hist_list[1:])]
        #print(diffs)
        if backwards:
            new_value = hist_list[0] - calc_diff(diffs, backwards=True)
        else:
            new_value = hist_list[-1] + calc_diff(diffs)
        #print(new_value, hist_list)
        return new_value
        
@timer
def part1(histories):

    histories = list(map(lambda x: x.split(' '), histories))
    histories = list(map(lambda x: list(map(lambda i: int(i), x)), histories))
    s = 0
    for h in histories:
        s += calc_diff(h)
    print(s)
    
    #print(histories)
    
    
@timer  
def part2(histories):
    histories = list(map(lambda x: x.split(' '), histories))
    histories = list(map(lambda x: list(map(lambda i: int(i), x)), histories))
    s = 0
    for h in histories:
        s += calc_diff(h, backwards=True)
    print(s)

def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()