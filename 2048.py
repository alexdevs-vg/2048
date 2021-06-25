__author__= 'Alex Pagnozzi'

import numpy as np
import os
from PIL import Image
import keyboard

GAMESTART = True
DIFFICULTY = 'Medium' #todo, Easy, Medium, Hard
NUMBERS = {'2': 'path2image', '4': '', '8': '',
           '16': 'path2image', '32': '', '64': '',
           '128': 'path2image', '256': '', '512': '',
           '1024': 'path2image', '2048': ''}

if DIFFICULTY == 'Easy':
    game_size = 3
elif DIFFICULTY == 'Easy':
    game_size = 4
elif DIFFICULTY == 'Easy':
    game_size = 5
game = np.zeros(game_size)


while GAMESTART is True:
    if keyboard.is_pressed("w"):
    if keyboard.is_pressed("a"):
    if keyboard.is_pressed("s"):
    if keyboard.is_pressed("d"):
    if keyboard.is_pressed("p"):    # power!


def randomise():
