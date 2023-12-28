import functools
import time                                                
from tqdm import tqdm
from copy import deepcopy
from itertools import combinations
from math import prod

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
        lines = f.read()
    #print(lines.split('\n\n'))
    return lines.split('\n\n')


class Part:
    def __init__(self, line):
        #s = {x=787,m=2655,a=1222,s=2876}
        values = line[1:-1] # Drop brackets
        values = values.split(',')
        self.v = {}
        for v in values:
            c, i = v.split('=')
            self.v[c] = int(i)
    
    def sum_values(self):
        return sum(self.v.values())
    def process(self, instruct_set):
        for instruct in instruct_set.split(','):
            if ':' not in instruct:
                return instruct
            else:
                c = instruct[0]
                op = instruct[1]
                sep = instruct.find(':')
                value = int(instruct[2:sep])
                result = instruct[sep+1:]
                if op == '>':
                    if self.v[c] > value:
                        return result
                if op == '<':
                    if self.v[c] < value:
                        return result
                
                
    def __str__(self):
        return f'values: {self.v}'
 
INSTRUCTS = {}
i, p = parse_input('input.txt')
i = i.split('\n')
for inst in i:
        name, sets = inst.split('{')
        INSTRUCTS[name] = sets[:-1]
combos = []
def split_ranges_by_instruction(ranges, i_name, l):
    #print(l, i_name, ranges)
    #input()
    instruct_set = INSTRUCTS[i_name]
    new_ranges = deepcopy(ranges)
    for instruct in instruct_set.split(','):
        if ':' not in instruct:
            if instruct == 'A':
                #print(f'{l} {i_name} {instruct} accepting {ranges}')
                combos.append((i_name, ranges))
            elif instruct == 'R':
                pass
            else:
                split_ranges_by_instruction(ranges, instruct, l+1)
        else:
            c = instruct[0]
            op = instruct[1]
            sep = instruct.find(':')
            value = int(instruct[2:sep])
            result = instruct[sep+1:]
            new_ranges = deepcopy(ranges)
            if op == '>':
               
                matching_range = [value + 1, ranges[c][1]]
                no_match_range = [ranges[c][0], value]
                new_ranges[c] = matching_range
                ranges[c] = no_match_range
                
            if op == '<':

                matching_range = [ranges[c][0], value - 1]
                no_match_range = [value , ranges[c][1]]
                new_ranges[c] = matching_range
                ranges[c] = no_match_range

            if result == 'A':
                #print(f'{l} {i_name} {result} accepting {new_ranges}')
                combos.append((i_name, new_ranges))
            elif result == 'R':
                pass
            else:
                split_ranges_by_instruction(new_ranges, result, l+1)
                
                # Seems like its not running the non-matched ranges?
                #split_ranges_by_instruction(ranges, result, l+1)
@timer
def part1(insts, parts):
    all_parts = [Part(part) for part in parts]
    instructs = {}
    s = 0
    for inst in insts:
        name, sets = inst.split('{')
        instructs[name] = sets[:-1]
        
    for part in all_parts:
        result = 'in'
        while result != 'A' and result != 'R':
            result = part.process(instructs[result])
            #print(result)
            #input()
        if result == 'A':
            s += part.sum_values()
    print(s)

@timer  
def part2():
    ranges = {
        'x': [1, 4000],
        'm': [1, 4000],
        'a': [1, 4000],
        's': [1, 4000]
        }
    
    
    split_ranges_by_instruction(ranges, 'in', 0)
    s = 0
    for combo in combos:
        #print(combo)
        diffs = [v[1] - v[0] + 1 for v in combo[1].values()]
        #print(diffs)
        #print(prod(diffs))
        s += prod(diffs)
            
    print(s)
        
        

def main():
    instructions, parts = parse_input('input.txt')
    instructions = instructions.split('\n')
    parts = parts.split('\n')
    
    part1(instructions, parts)
    part2()
    
if __name__ == '__main__':
    main()