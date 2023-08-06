def menu(list):
    print('Which league are you in?')
    c = 1
    for league in list[1:]:
        print(f'{c} - {league}')
        c += 1
    ans = int(input('Chosen option: '))
    return ans