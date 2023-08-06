from chests import *
from menu import *

leagues = list(chancesPerLeague.keys())
qty = int(input('How many chests will you simulate? '))

while True:
    ans = menu(leagues)
    if 0 < ans < 6:
        league = select_league(ans)
        print(f'The selected league was {league}.')
        c = 1
        while qty > 0:
            print(f'{open_chests(qty, league)[0]:^15}', end='')
            if c % 5 == 0:
                print('')
            c += 1
            qty -= 1
        break
    print('Invalid option! Choose a valid option between 1 and 5.')