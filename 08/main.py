import functools
import time                                                
from tqdm import tqdm
from math import lcm

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
def part1(directions, nodes):
    current_node = 'AAA'
    direction_counter = 0
    steps = 0
    while current_node != 'ZZZ':
        if directions[direction_counter] == 'R':
            current_node = nodes[current_node]['right']
        else:
            current_node = nodes[current_node]['left']
        direction_counter += 1
        steps += 1
        if direction_counter >= len(directions):
            direction_counter = 0
    print(steps)

@timer  
def part2(directions, nodes):
    current_nodes = [node for node in nodes.keys() if node[2] == 'A']
    
    direction_counter = 0
    steps = 0
    steps_to_z = [0] * len(current_nodes)
    #all_z_nodes = False
    while 0 in steps_to_z:
        i = 0
        for i in range(len(current_nodes)):
            if current_nodes[i][2] == 'Z':
                continue
            #print(current_nodes[i])
            #print(i, len(current_nodes))
            if directions[direction_counter] == 'R':
                current_nodes[i] = nodes[current_nodes[i]]['right']
            else:
                current_nodes[i] = nodes[current_nodes[i]]['left']
            if current_nodes[i][2] == 'Z':
                steps_to_z[i] = steps+1
                #print(steps_to_z)
                #i = i - 1
        #all_z_nodes = check_z_nodes(current_nodes)
            i += 1
        direction_counter += 1
        steps += 1
        if direction_counter >= len(directions):
            direction_counter = 0
        #if steps % 10000 == 0:
            #print(steps)
    print(steps_to_z)
    print(lcm(*steps_to_z))
    print(functools.reduce(lambda x, y: x*y, steps_to_z))
            

def main():
    data = parse_input('input.txt')
    directions = data[0]
    nodes = {node[:3]: {'left': node[7:10], 'right': node[12:15]} for node in data[2:]}

    
    #part1(directions, nodes)
    part2(directions, nodes)
    
if __name__ == '__main__':
    main()