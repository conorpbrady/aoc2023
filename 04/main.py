import regex as re
import functools
import time                                                


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

def num_of_wins(card_no, line):
   
    card, numbers = line.split(':')
    winning, selected = numbers.strip().split('|')
    winning = [item for item in winning.strip().split(' ') if item]
    selected = [item for item in selected.strip().split(' ') if item]
    
    points = 0
    for num in selected:
        if num in winning:
            points += 1
    return points

def main():
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    
    part1(lines)
    #part2(lines)
    part2_optimized(lines)

@timer
def part1(lines):
    s = 0
    for i, line in enumerate(lines):
        num_wins = num_of_wins(i+1, line)
        points = 0
        
        for j in range(1, num_wins+1):
            if points == 0:
                points = 1
            else:
                points *= 2
        s += points

    print(f'Part 1: {s}')

@timer
def part2(lines):
    num_cards = 0
    cards = [i+1 for i in range(len(lines))]
    while len(cards) > 0:
        card_no = cards.pop(0)
        num_cards += 1
        num_wins = num_of_wins(card_no, lines[card_no - 1])
        cards += [i for i in range(card_no+1, num_wins + card_no + 1)]

    print(f'Part 2: {num_cards}')

@timer
def part2_optimized(lines):
    copies = {k+1: 1 for k in range(len(lines))}
    for i, line in enumerate(lines):
        num_wins = num_of_wins(i+1, line)        
        for k in range(i+2, i+2+num_wins):
            copies[k] += copies[i+1]

    print(f'Part 2 (optimized): {sum(copies.values())}')
        
if __name__ == '__main__':
    main()