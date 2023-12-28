import re
from colorama import Fore, Back, Style, init
init(convert=True)
with open('input.txt') as f:
    lines = [line.strip() for line in f.readlines()]


def is_symbol_adjacent(x_span, y_pos):
    
    for y in range(y_pos - 1, y_pos + 2):
        
        if y < 0 or y >= len(lines):
            continue
        for x in range(x_span[0] - 1, x_span[1] + 1):
            if x < 0 or x >= len(lines[y]):
                continue
            
            try:
                #print(f'{y}\t{x}: {lines[y][x]}')
                if lines[y][x] != '.' and lines[y][x] not in '1234567890':
                    #print(f'Found: {lines[y][x]}')
                    return True
            except IndexError:
                pass
                
    return False

def adjacent_gear(x_span, y_pos):
    
    for y in range(y_pos - 1, y_pos + 2):
        
        if y < 0 or y >= len(lines):
            continue
        for x in range(x_span[0] - 1, x_span[1] + 1):
            if x < 0 or x >= len(lines[y]):
                continue
            
            try:
                #print(f'{y}\t{x}: {lines[y][x]}')
                if lines[y][x] == '*':
                    #print(f'Found: {lines[y][x]}')
                    return (y, x)
            except IndexError:
                pass
                
    return None
    
def part1():
    s1 = 0
    gears = {}
    for index, line in enumerate(lines):
        for i, c in enumerate(line):
            if c == '*':
                gears[(index, i)] = []
                
    for index, line in enumerate(lines):
        line_sum = 0
        highlight_start = []
        highlight_end = []
        p = re.compile("\d+")
        matches = p.finditer(line)
        for match in matches:
            #print(match.group())
            gear = adjacent_gear(match.span(), index)
            if gear is not None:
                gears[gear].append(int(match.group()))
            if is_symbol_adjacent(match.span(), index):
                #print(f'{match.group()},')
                s1 += int(match.group())
                line_sum += int(match.group())
                highlight_start.append(match.span()[0])
                highlight_end.append(match.span()[1])
        
        # for i, c in enumerate(line):
        
            # if i in highlight_start:
                # print(Fore.GREEN, end='')
                # #print(Back.GREEN, end='')
            # if i in highlight_end:
                # print(Style.RESET_ALL, end='')
            # if c in '+-)(*&^%$#@=!/':
                # print(Back.YELLOW, end='')
                # print(c, end='')
                # print(Style.RESET_ALL, end='')
            # else:
                # print(c, end='')
        # print(Style.RESET_ALL+f'\t{line_sum}')
            
        
    print(f'Part 1: {s1}')
    s2 = 0
    for k, gs in gears.items():
        if len(gs) > 1:

            sg = 1
            for g in gs:
                sg *= g
            s2 += sg
    print(f'Part 2: {s2}')

def main():
    part1()
    
if __name__ == '__main__':
    main()
		