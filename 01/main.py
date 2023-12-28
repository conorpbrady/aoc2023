import regex as re

NUMS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9
    }
    
def main():

    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    
    s1 = 0
    s2 = 0
    for line in lines:
        matches = re.findall('\d', line)
        if len(matches) > 0:
            n1 = int(matches[0]) * 10 + int(matches[-1])
            s1 += n1
        
        
        pattern = '|'.join(NUMS.keys())
        matches = re.findall(pattern, line, overlapped=True)
  
        n2 = NUMS[matches[0]] * 10 + NUMS[matches[-1]]

        s2 += n2
        
    print(f'Part 1: {s1}')
    print(f'Part 2: {s2}')
    
    
    
            

if __name__ == '__main__':
    main()
		