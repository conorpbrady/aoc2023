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



# Modules
#
# Button (not in input)
# There is one. When pressed sends a single LOW pulse to broadcaster
#
# Broadcaster
# Sends same input pulse to all output modules
# 
#
# Flip flop
# Two states on/off
# If receives HIGH, ignore
# If LOW and off - turns on, sends HIGH pulse
# If LOW and on - turns off, sends LOW pulse
#
# Conjunction
# Remembers the most recent pulse from EACH of its inputs - defaults to LOW
# Receives a pulse, updates its memory with that pulse first
# Then, if most recent pulse on every input was HIGH, sends LOW
# Else, sends HIGH
    
LOW = 0
HIGH = 1

def push_button(modules, stop_at_node=None):
    highs = 0
    lows = 0
    processing_queue = [('bcast', LOW, 'button')]
    while processing_queue:
        cm, pulse, pm = processing_queue.pop(0)
        #print(pm, pulse, cm)

        if pulse == HIGH:
            highs += 1
        else:
            lows += 1
            
        if cm not in modules:
            continue
        if cm == 'bcast':
            # LOW to all inputs
            processing_queue += [(m, LOW, cm) for m in modules[cm]['outputs']]
            continue
        if modules[cm]['con']: #Conjunction modules
            # Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; 
            # they initially default to remembering a low pulse for each input.
            # When a pulse is received, the conjunction module first updates its memory for that input. 
            # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            
            # Update input
            modules[cm]['inputs'][pm] = pulse
            #print(cm, modules[cm]['inputs'].values(), all(modules[cm]['inputs'].values()))
            # If all inputs are HIGH, send LOW to all outputs
            if all(modules[cm]['inputs'].values()): # All inputs are HIGH, send LOW to all outputs
                if stop_at_node is not None and cm == stop_at_node and pulse == LOW:
                    print('hi')
                    return lows, highs, True 
                processing_queue += [(m, LOW, cm) for m in modules[cm]['outputs']]
            else: # Send HIGH to all outputs if any inputs are LOW            
                processing_queue += [(m, HIGH, cm) for m in modules[cm]['outputs']]
        else: # Flip Flop Module
            # If HIGH pulse, ignore
            if pulse == HIGH:
                continue
            
            if modules[cm]['is_on']: #Send LOW pulse if on
                processing_queue += [(m, LOW, cm) for m in modules[cm]['outputs']]
            else: # Send HIGH pulse if off
                processing_queue += [(m, HIGH, cm) for m in modules[cm]['outputs']]
            # Received a LOW pulse, turn off if on, turn on if off
            modules[cm]['is_on'] = not modules[cm]['is_on']
    return lows, highs, False

def load_modules():
    lines = parse_input('input.txt')
    modules = {
        'bcast': [],
        }
    for line in lines:
        im, oms = line.split(' -> ')
        if im == 'broadcaster':
            modules['bcast'] = {'outputs': oms.split(', ')}
            continue
        if im[0] == '%':
            modules[im[1:]] = {'con': False, 'outputs': oms.split(', '), 'is_on': False}
        if im[0] == '&':
            modules[im[1:]] = {'con': True, 'outputs': oms.split(', '), 'inputs': {}}
    for line in lines:
        im, oms = line.split(' -> ')
        oms = oms.split(', ')
        for om in oms:
            for k, v in modules.items():
                if k!= 'bcast' and not modules[k]['con']:
                    continue
                if om == k:
                    modules[k]['inputs'][im[1:]] = LOW
    return modules

@timer
def part1():

    m = load_modules()
    h = 0
    l = 0
    for i in range(1000):
        
        nh, nl, searching = push_button(m)
        h += nh
        l += nl
        #print(i+1, nl, nh)
    print(l, h, h * l)

@timer  
def part2():

    # rx is the output of a conjuction module with 4 inputs, each a conjunction module with further inputs
    #               rx
    #               rg
    #       kd  zf  gs  vg
    #       |   |   |   |
    #       tq  pf  rj  kx
    #       |   |   |   |
    #       9x  7x  7x  9x
    #   Gonna need to figure out at what button press each of the pre-req conjuction modules inputs will all be HIGH and do a LCM on it or something
    #   Map these all out and put them on tiers maybe? Figure out when tq, pf, rj, and kx all send HIGH and calc it from there?
    #   Disregard the above, keeping it for posterity
    #
    # Each of the multiple that feed into tq, pf, rh, kx, are working on a cycle. Need to find when those cycles line up and all send a HIGH pulse into the conjuction modules that feed into rx

    #Brute force ain't gonna work
    #return
    m = load_modules()
    found = False
    i = 1
    mod = 'tq'
    while not found:
 
        nh, nl, found = push_button(m, mod)
        if i % 100000 == 0:
            print(i)
        i += 1
    print(f'{mod} sends LOW after {i} presses')
def main():
    
    
    part1()
    part2()
    
if __name__ == '__main__':
    main()