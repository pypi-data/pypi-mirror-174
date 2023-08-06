from random import choices

chancesPerLeague = {
    'League': {'%': ['Crystals', 'Card', 'Potion', 'Soul']},
    'Bronze': {'%': [33.33, 33.33, 33.33, 0.005]},
    'Silver': {'%': [33, 38, 28.25, 0.75]},
    'Gold': {'%': [32, 43, 23, 2]},
    'Diamond': {'%': [31.5, 48, 18, 2.5]},
    'Champion': {'%': [31, 53, 12.5, 3.5]}
    }


def get_data_set(g1, g2):
    return chancesPerLeague.get(g1).get(g2)


def select_league(ans):
    return list(chancesPerLeague.keys())[ans]


def open_chests(qtd, sel_league):
    return choices(
        get_data_set('League', '%'),
        get_data_set(sel_league, '%'),
        k=qtd)