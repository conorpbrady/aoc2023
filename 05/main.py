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
    

MAP_KEYS = ['seed-to-soil map', 'soil-to-fertilizer map', 'fertilizer-to-water map', 'water-to-light map', 'light-to-temperature map', 'temperature-to-humidity map', 'humidity-to-location map']

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    
    maps = {k: [] for k in MAP_KEYS}
    seeds = [int(i) for i in lines.pop(0).split(':')[1].strip().split(' ')]
    key = ''
    for line in lines:

        if line == '':
            continue
        if ':' in line:
            key = line.split(':')[0]
        else:
            maps[key].append([int(i) for i in line.split(' ')])
    return seeds, maps

@timer
def part1():
    seeds, maps = parse_input('input.txt')
    locations = []
    
    for seed in seeds:
        source = seed
        dest = source
        for key in MAP_KEYS:
            #print(key)
            for mapping in maps[key]:
                dest_range_start, source_range_start, range_length = mapping
                if source >= source_range_start and source <= source_range_start + range_length:
                    dest = source + (dest_range_start - source_range_start)
                    break
            #print(f'{source} {dest}\n', end='')
            source = dest
            
        #print()
        locations.append(dest)
    #print(locations)
    print(min(locations))

def find_min_location(start, length, step_size, maps):
    min_location = 100000000000000
    for source in tqdm(range(start, start+length, step_size)):
        dest = find_location(source)
        min_location = min(min_location, dest)
    return min_location

def find_location(value, maps):
    dest = value
    for key in MAP_KEYS:
        #print(key)
        for mapping in maps[key]:
            dest_range_start, source_range_start, range_length = mapping
            if value >= source_range_start and value <= source_range_start + range_length:
                dest = value + (dest_range_start - source_range_start)
                break
        #print(f'{source} {dest}\n', end='')
        value = dest
    return dest
    
def part2():
    seeds, maps = parse_input('test.txt')
    thread_length = int(len(seeds) / 2)
    threads = [None] * thread_length
    results = [None] * thread_length
    for i in range(thread_length):
        threads[i] = Thread(target=find_min_location, args=(seeds[(i*2)], seeds[(i*2)+1], maps, results, i))
        threads[i].start()
    for i in range(thread_length):
        threads[i].join()
        
    print(min(results))

def part2_alt():
    seeds, maps = parse_input('test.txt')
    step_size = 1000
    range_with_min = 20
    
    while step_size >=10:
        if range_with_min > 10:
            range_mins = []
            for i in range(0, len(seeds), 2):
                m = find_min_location(seeds[i], seeds[i+1], step_size, maps)
                range_mins.append(m)
            lowest = min(range_mins)
            range_with_min = range_mins.index(lowest)
        else:
            step_size = 1
   
            m = find_min_location(seeds[range_with_min], seeds[range_with_min+1], step_size, maps)
            lowest = min(lowest, m)
    print(lowest)
            
def part2_alt2():
    seeds, maps = parse_input('input.txt')
    ranges = list(zip(seeds[0::2], seeds[1::2]))
    min_loc = sys.maxsize
    while len(ranges) > 0:
        r = ranges.pop(0)
        step = int(math.sqrt(r[1]))
        if step == 0:
            continue

        for value in range(r[0], r[0]+r[1], step):
            loc = find_location(value - int(step / 2), maps)
            if loc < min_loc:
                new_range = (value - int(step / 2), int(step / 2))

                ranges.append(new_range)
                min_loc = loc
    print(min_loc)

def is_valid_seed(value, seeds):
    for s in seeds:
        #print(s[0], value, s[0]+s[1])
        if value >= s[0] and value < (s[0] + s[1]):
            return True
    return False

@timer
def part2_alt3():
    seeds, maps = parse_input('input.txt')
    seeds = list(zip(seeds[::2], seeds[1::2]))
    MAP_KEYS.reverse()
    location = 0
    while True:
        dest = location
        source = dest
        for key in MAP_KEYS:
            for mapping in maps[key]:
                dest_range_start, source_range_start, range_length = mapping
                if dest_range_start <= dest < dest_range_start + range_length:
                    source = dest + (source_range_start - dest_range_start)
                    
                    break
            dest = source
        if is_valid_seed(source, seeds):
            print(location, source)
            return
        location += 1

def split_ranges(ranges, conversions):
    output = []
    for seed_start, seed_length in ranges:
        while seed_length > 0:
            for conversion in conversions:
                dst, src, lgth = conversion
                #print(f'({seed_start}, {seed_length}) : {dst}, {src}, {lgth}')
                if seed_start >= src and seed_start < src + lgth:
                    
                    if seed_start + seed_length > src + lgth: # See if we need to split range into two
                        new_length = (src + lgth) - seed_start
                        new_start = seed_start + new_length
                    else:
                        new_length = seed_length
                        new_start = seed_start
                        
                    output.append((seed_start + (dst - src), new_length))
                    
                    seed_start = new_start
                    seed_length -= new_length
                    break
                
            else: # For/Else clause - this only runs if the for loop was not broken out of
                output.append((seed_start, seed_length))
                break # Breaks out of while loop if seed_length is not consumed
    return output

@timer
def part2_alt4():
    seeds, maps = parse_input('input.txt')
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))

    #print(seed_ranges)
    for m in maps.values():
        seed_ranges = split_ranges(seed_ranges, m)
        #print(seed_ranges)
    print(min(seed_ranges)[0])
    
def main():
    part1()
    #part2()
    #part2_alt()
    #part2_alt2()
    #part2_alt3()
    part2_alt4()
    
if __name__ == '__main__':
    main()