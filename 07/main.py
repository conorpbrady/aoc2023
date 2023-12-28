import functools
import time                                                
from tqdm import tqdm
from collections import defaultdict

FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0
    
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

def convert_base_14(hand, jokers_wild=False):
    j = 11
    if jokers_wild:
        j = 1
    face_cards = {'A': 14, 'K': 13, 'Q': 12, 'J': j, 'T': 10}
    b = 0
    #print(hand)
    for i, c in enumerate(hand):
        factor = 14 ** (len(hand) - i)
        #print(c, factor)
        if c in face_cards:
            
            b += face_cards[c] * factor
        else:
            b+= int(c) * factor
    return b * -1
        
# Determine if hand is five-of-a-kind, full house, etc and assign point value
# For part 2 modify this so that we can get the count of jokers and non-jokers
# Then use that to calc the best hand
def score_hand(hand):

    card_count = defaultdict(int)
    for c in hand:
        card_count[c] += 1

    matched_three = False
    matched_two = False
    for i in card_count.values():        
        if i == 5:
            return FIVE_OF_A_KIND
        if i == 4:
            return FOUR_OF_A_KIND
        if i == 3:
            if matched_two:
                return FULL_HOUSE
            matched_three = True
        if i == 2:
            if matched_two:
                return TWO_PAIR
            if matched_three:
                return FULL_HOUSE
            matched_two = True
    if matched_three:
        return THREE_OF_A_KIND
    if matched_two:
        return ONE_PAIR
    return HIGH_CARD

def make_best_hand(hand):
    cards = hand.replace('J','')
    wilds = 5 - len(cards)
    non_wild_score = score_hand(cards)
    
    if wilds == 5 or wilds == 4:
        return FIVE_OF_A_KIND
    if wilds == 3:
        if non_wild_score == ONE_PAIR:
            return FIVE_OF_A_KIND
        if non_wild_score == HIGH_CARD:
            return FOUR_OF_A_KIND
    if wilds == 2:
        if non_wild_score == THREE_OF_A_KIND:
            return FIVE_OF_A_KIND
        if non_wild_score == ONE_PAIR:
            return FOUR_OF_A_KIND
        if non_wild_score == HIGH_CARD:
            return THREE_OF_A_KIND
    if wilds == 1:
        if non_wild_score == TWO_PAIR:
            return FULL_HOUSE
        if non_wild_score == THREE_OF_A_KIND:
            return FOUR_OF_A_KIND
        if non_wild_score == ONE_PAIR:
            return THREE_OF_A_KIND
        if non_wild_score == FOUR_OF_A_KIND:
            return FIVE_OF_A_KIND
        return ONE_PAIR
    return score_hand(hand)
        

@timer
def part1(hands):
    hand_type = {hand: (score_hand(hand[:5]), convert_base_14(hand[:5])) for hand in hands}
    ranked = {k: v for k, v in sorted(hand_type.items(), key=lambda item: (item[1][0], -item[1][1]))}
    
    #winnings = sum([int(hand.split(' ')[1]) * (rank+1) for rank, hand in enumerate(ranked.keys())])
    winnings = 0
    #print(len(ranked))
    for rank, hand in enumerate(ranked.keys()):
        bid = int(hand.split(' ')[1])
       
        #print(hand, ranked[hand], rank+1, bid)
        winnings += bid * (rank+1)
        
    print(winnings)
    
@timer  
def part2(hands):
    hand_type = {hand: (make_best_hand(hand[:5]), convert_base_14(hand[:5], jokers_wild=True)) for hand in hands}
    ranked = {k: v for k, v in sorted(hand_type.items(), key=lambda item: (item[1][0], -item[1][1]))}
    
    #winnings = sum([int(hand.split(' ')[1]) * (rank+1) for rank, hand in enumerate(ranked.keys())])
    winnings = 0
    for rank, hand in enumerate(ranked.keys()):
        bid = int(hand.split(' ')[1])
       
        #print(hand, ranked[hand], rank+1, bid)
        winnings += bid * (rank+1)
    print(winnings)
    
def main():
    data = parse_input('input.txt')
    
    part1(data)
    part2(data)
    
if __name__ == '__main__':
    main()