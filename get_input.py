from datetime import datetime
import requests
from dotenv import load_dotenv
import os
load_dotenv()

def calc_day():
    d = datetime.today() - datetime.strptime('2023-12-01', '%Y-%m-%d')
    return d.days + 1

def main():
    d = calc_day()
    filename = f'{d:02}\\input.txt'
    try: 
        with open(filename) as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
        r = requests.get(f'https://adventofcode.com/2023/day/{d}/input', headers=headers, cookies = {'session': os.environ.get('SESSION')}, verify=False)
        with open(filename, 'w') as f:
            f.write(r.text)
            
if __name__ == '__main__':
    main()