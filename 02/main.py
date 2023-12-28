
MAX = {
    'red': 12,
    'blue': 14,
    'green': 13
    }

def is_valid_game(history):
    pulls = history.strip().split(';')
    for pull in pulls:
        colors = pull.strip().split(',')
        for color in colors:
            qty, clr = color.strip().split(' ')
            if int(qty) > MAX[clr]:
                return False
    return True
    
def calc_color_product(history):
    max_colors = {'red': 0, 'green': 0, 'blue': 0}
    pulls = history.strip().split(';')
    for pull in pulls:
        colors = pull.strip().split(',')
        for color in colors:
            qty, clr = color.strip().split(' ')
            max_colors[clr] = max(max_colors[clr], int(qty))
    
    product = 1
    for qty in max_colors.values():
        product *= qty
    return product
def main():

    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    s1 = 0
    s2 = 0
    for line in lines:
        game, history = line.split(':')
        _, game_id = game.split(' ')
        game_id = int(game_id)
    
        if is_valid_game(history):
            s1 += game_id
        s2 += calc_color_product(history)
        
    print(s1)
    print(s2)

    
    
            

if __name__ == '__main__':
    main()
		