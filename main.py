import pickle
import os
from clear import clear
import logging
from typing import Any
from colorama import Fore

L_RED: str = Fore.LIGHTRED_EX
L_GREEN: str = Fore.LIGHTGREEN_EX
L_YELLOW: str = Fore.LIGHTYELLOW_EX
L_CYAN: str = Fore.LIGHTCYAN_EX
CYAN: str = Fore.CYAN
RESET: str = Fore.RESET

VERSION: float = 1.0

cups: dict = {}

logging.basicConfig(level=logging.WARNING)


def save(file_name: str, item: Any) -> None:
    with open(f'save/{file_name}.pickle', 'wb') as f:
        pickle.dump(item, f)
        f.close()


def load(file_name: str) -> Any:
    with open(f'save/{file_name}.pickle', 'rb') as f:
        return pickle.load(f)


def add_spaces(num: int) -> str:
    return ' ' * num


def cup_collection() -> str:
    clear()
    return_val = 'Collection:\n\n'
    for c in cups:
        cup = cups[c]
        return_val += f'{cup.display_name}:\n'
        if cup.owned:
            return_val += f'\tOwned: [{L_GREEN}{cup.owned}{RESET}]\tPower: [{L_YELLOW}{cup.power}{RESET}]\tPrice: [{CYAN}{cup.price}{RESET}]\n'
        else:
            return_val += f'\tOwned: [{L_RED}{cup.owned}{RESET}]\tPower: [{L_YELLOW}{cup.power}{RESET}]\tPrice: [{CYAN}{cup.price}{RESET}]\n'
    return return_val


def cup_shop() -> str:
    return ''


class Cup:
    def __init__(self, name: str, power: int | float, price: int | float) -> None:
        self.name = name
        self.display_name = name.capitalize()
        self.power = power
        self.owned = False
        self.price = price
        cups[name] = self

    def __repr__(self) -> str:
        return self.display_name


class Player:
    def __init__(self, cup: Cup) -> None:
        self.cup = cup
        self.power = 1 + self.cup.power
        self.coins = 0

    def change_cup(self, cup: Cup) -> str:
        if cup.owned:
            self.cup = cup
            self.power = 1 + self.cup.power
            return f'Changed players cup to {cup}'
        else:
            return f'You dont own {cup}'

    def buy_cup(self, cup: Cup) -> str:
        if cup.owned:
            return f'You already own {cup}'
        if self.coins < cup.price:
            return f'You dont have enough money to buy {cup}'
        if self.coins >= cup.price:
            self.coins -= cup.price
            cup.owned = True
            if self.cup.power <= cup.power:
                self.change_cup(cup)
            return f'Bought {cup}'

    def beg(self) -> None:
        self.coins = self.coins + self.power

    def show_stats(self) -> str:
        return f"Coins: [{L_YELLOW}{self.coins}{RESET}]{add_spaces(10)} Power: [{L_YELLOW}{self.power}{RESET}]{add_spaces(10)} Cup: [{L_YELLOW}{self.cup}{RESET}]{add_spaces(10)}"

    def change_cup_menu(self) -> None:
        clear()
        cup_list = []
        print('Select a cup')
        for index, c in enumerate(cups):
            cup = cups[c]
            if cup.owned:
                print(f'[{L_YELLOW}{index}{RESET}] {cup.display_name}')
                cup_list.append(cup)

        cup_inp = input('>> ')

        try:
            if type(cup_list[int(cup_inp)]) == Cup:
                print(self.change_cup(cup_list[int(cup_inp)]))
        except IndexError:
            print('Please pick a valid option')
        except ValueError:
            print('Please pick a integer')


cup1 = Cup('cup', 1, 0)
cup1.owned = True
cup2 = Cup('cup 2', 2, 20)

player = Player(cup1)

load_list: list[str] = ['cups', 'player']

if os.path.exists('save'):
    for lo in load_list:
        try:
            loaded_object = load(lo)
        except FileNotFoundError as e:
            logging.warning(f'[{e.filename}] could not be loaded')
        except pickle.UnpicklingError as e:
            logging.warning(f'{e}, one of the .pickle files is not formatted properly')
else:
    os.mkdir('save')

options = f"""
Options:
[{L_YELLOW}1{RESET}] Beg for money
[{L_YELLOW}2{RESET}] Change Cup
[{L_YELLOW}3{RESET}] Collection
"""


def save_all():
    save('cups', cups)
    save('player', player)


logging.debug('Running..')

while __name__ == '__main__':

    save_all()

    print(player.show_stats())

    print(options)

    inp = input('>> ')

    if inp == 'beg' or inp == '1':
        player.beg()
    elif inp == 'change cup' or inp == '2':
        player.change_cup_menu()
    elif inp == 'collection' or inp == '3':
        print(cup_collection())
        input('>> ')

    clear()
