import pickle
import os
from clear import clear
import logging


VERSION = 1.0

cups = {}


def save(file_name: str, item: any):
    with open(f'save/{file_name}.pickle', 'wb') as f:
        pickle.dump(item, f)
        f.close()


def load(file_name: str):
    with open(f'save/{file_name}.pickle', 'rb') as f:
        return pickle.load(f)


def add_spaces(num: int):
    return ' ' * num


def cup_collection():
    clear()
    cup_list = []
    for c in cups:
        cup = cups[c]
        print(f'{cup.display_name}:')
        print(f'\tOwned: [{cup.owned}]\tPower: [{cup.power}]')
        cup_list.append(cup)

    input('>> ')


class Cup:
    def __init__(self, name: str, power: int | float):
        self.name = name
        self.display_name = name.capitalize()
        self.power = power
        self.owned = False
        cups[name] = self

    def __repr__(self):
        return self.display_name


class Player:
    def __init__(self, cup: Cup):
        self.cup = cup
        self.power = 1 + self.cup.power
        self.coins = 0

    def change_cup(self, cup: Cup):
        if cup.owned:
            self.cup = cup
            self.power = 1 + self.cup.power
            return f'Changed players cup to {cup}'
        else:
            return f'You dont own {cup}'

    def beg(self):
        self.coins = self.coins + self.power

    def show_stats(self):
        return f"Coins: [{self.coins}]{add_spaces(10)} Power: [{self.power}]{add_spaces(10)} Cup: [{self.cup}]{add_spaces(10)}"

    def change_cup_menu(self):
        clear()
        cup_list = []
        print('Select a cup')
        for index, c in enumerate(cups):
            cup = cups[c]
            if cup.owned:
                print(f'[{index}] {cup.display_name}')
                cup_list.append(cup)

        cup_inp = input('>> ')

        try:
            if type(cup_list[int(cup_inp)]) == Cup:
                print(self.change_cup(cup_list[int(cup_inp)]))
        except IndexError:
            print('Please pick a valid option')
        except ValueError:
            print('Please pick a integer')


cup1 = Cup('cup', 1)
cup1.owned = True
cup2 = Cup('cup 2', 2)

player = Player(cup1)

if os.path.exists('save'):
    try:
        load_cups = load('cups')
        cup1 = load_cups['cup']
        cup2 = load_cups['cup 2']
        player = load('player')
    except FileNotFoundError:
        logging.warning('one or more files could not be loaded')
else:
    os.mkdir('save')

options = """
Options:
[1] Beg for money
[2] Change Cup
[3] Collection
"""


def save_all():
    save('cups', cups)
    save('player', player)


while __name__ == '__main__':

    save_all()

    clear()

    print(player.show_stats())

    print(options)

    inp = input('>> ')

    if inp == 'beg' or inp == '1':
        player.beg()
    elif inp == 'change cup' or inp == '2':
        player.change_cup_menu()
    elif inp == 'collection' or inp == '3':
        cup_collection()
