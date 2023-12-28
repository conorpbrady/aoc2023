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
    
def fill_known(s, indicies):
    
    str_as_list = list(s)
    
    for i in indicies:
        str_as_list[i] = '#'
    
    s = ''.join(str_as_list)
    
    dots = [pos for pos, char in enumerate(s) if char == '?']
    for i in dots:
        str_as_list[i] = '.'
    return ''.join(str_as_list)
        
    
def get_all_combos(s):
    combos = []
    qs = [pos for pos, char in enumerate(s) if char == '?']
    for i in range(len(qs)+1):
        combos += list(combinations(qs, i))
    return combos

def satisfies_grouping(s, grouping):
    in_group = False
    count = 0
    #print(s)
    for c in s:
        #print(c, grouping)
        if c == '.':
            in_group = False
            if count > 0:
                if len(grouping) == 0:
                    return False
                if count != grouping.pop(0):
                    #print(count) 
                    return False
            count = 0
        else:
            in_group = True
            count += 1
    else:
        if count > 0:
            if len(grouping) == 0:
                return False
            if count != grouping.pop(0):
                return False
    return len(grouping) == 0
    return True
    
@timer
def part1(lines):
    arrs = 0
    for line in tqdm(lines):
        springs, counts = line.split(' ')
        counts = [int(i) for i in counts.split(',')]      
        for c in get_all_combos(springs):
            if satisfies_grouping(fill_known(springs, c), counts[:]):
                arrs += 1
        #print(line, s_arrs)
    print(arrs)

@functools.cache  
def is_possible_arrangement(springs, count):
    #print('--', springs, count)
    if count > len(springs): # Not enough springs to match count
        return False
    if '.' in springs[:count]: # . in remaining springs
        return False
    #print(count, springs)
    if not (count == len(springs) or springs[count] != '#'): # If springs length doesn't match count or if springs contain other than '#'
        return False
    return True
    
@functools.cache      
def find_arrangement(springs, counts, l):

    # If end of string, and no more groups, that is a valid arrangement
    if not springs:
        if len(counts) == 0:
            return 1
        return 0
    # If no more groups, and there is no more '#' present, that is a valid arrangement
    if len(counts) == 0:
        if '#' not in springs:
            return 1
        return 0

    s = springs[0]
    arrangements = 0
    
    if s in '.?': # Treat ? as .
        arrangements += find_arrangement(springs[1:], counts, l+1)
    if s in '?#': # Treat ? as #
        if is_possible_arrangement(springs, counts[0]):
            # everything in counts[0] is a possible #, advance to next grouping
            arrangements += find_arrangement(springs[counts[0]+1:], counts[1:], l+1)

    return arrangements

@timer  
def part2(lines):
    s = 0
    for line in tqdm(lines):
        springs, counts = line.split(' ')
        counts = tuple(int(i) for i in counts.split(',')) * 5
        springs = '?'.join([springs] * 5)
        t = find_arrangement(springs, counts, 0)
        s += t
        #print(t, line)
    print(s)
    
    
def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()