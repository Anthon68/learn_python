from small_text_game.src.camera import Camera
from small_text_game.src.event import *
from small_text_game.src.event_manager import EventManager
from small_text_game.src.map import Map
from small_text_game.src.monster import Monster
from small_text_game.src.user import User
from small_text_game.src.options import *


class GameOverException(Exception):
    pass


class Game:
    def __init__(self):
        self.messages = []
        self.camera = Camera()
        self.map = Map()
        self.user = User('Name')
        self.monsters = [
            Monster(f'Ork{i}') for i in range(MAX_MONSTERS)
        ]
        EventManager.getInstance().bind(MessageEvent.name, self, 'new_message')

    def generate_map(self, width, height, empty_char):
        self.map.generate(width, height, empty_char)

    def place_on_map(self, quantity, char):
        self.map.place(quantity, char)

    def run(self):
        self.generate_map(MAP_WIDTH, MAP_HEIGHT, EMPTY)
        self.place_on_map(MAX_TREES, TREE)
        self.place_on_map(MAX_STONES, STONE)
        self.place_on_map(MAX_LETTERS, LETTER)
        self.place_on_map(MAX_TREASURES, TREASURE)
        self.user.place_on(self.map)
        for monster in self.monsters:
            monster.place_on(self.map)
        while True:
            self.turn()

    def turn(self):
        self.camera.show(self.map, self.user, SMOG_RADIUS)
        self.show_messages()
        self.user.turn(self.map)
        if self.is_over():
            raise GameOverException()
        for monster in self.monsters:
            if monster.is_dead():
                monster.killed(self.map)
                self.monsters.remove(monster)
            else:
                monster.turn(self.map)

    def is_over(self):
        return self.user.is_dead() or self.user.has(MAX_TREASURES, TREASURE)

    def new_message(self, event):
        self.messages += event.data

    def show_messages(self):
        if len(self.messages) > 0:
            for message in self.messages:
                print(message)
        self.messages = []
