__author__= 'Alex Pagnozzi'

import numpy as np
import os
#from PIL import Image
import keyboard
import json
#import cv2
#import cv2.cv as cv

os.chdir('D:\\Dev\\2048\\')

GAMESTART = True
DIFFICULTY = 'Medium' #todo, Easy, Medium, Hard
NUMBERS = {'2': 'path2image', '4': '', '8': '',
           '16': 'path2image', '32': '', '64': '',
           '128': 'path2image', '256': '', '512': '',
           '1024': 'path2image', '2048': ''}

with open('MAXSCORE.json') as score_file:
    score = json.load(score_file)
    for key, value in score.items():
        if key == 'MAXSCORE':
            MAXSCORE = value
score = 0

def randomise(game, DIFFICULTY, game_size):
    if DIFFICULTY == 'Easy':
        num2add = 1
    elif DIFFICULTY == 'Medium':
        num2add = 1 + 1*(np.random.rand(1)>0.5)
    elif DIFFICULTY == 'Hard':
        num2add = 2 + 1*(np.random.rand(1)>0.5)

    for i in range(0, int(num2add)):
        r = int(np.floor(np.random.rand(1)*game_size))
        c = int(np.floor(np.random.rand(1)*game_size))
        while game[r,c] != 0:
            r = int(np.floor(np.random.rand(1) * game_size))
            c = int(np.floor(np.random.rand(1) * game_size))
        game[r,c] = 2 + 2*((np.random.rand(1))>(0.5+ num2add/10))
    return game

def move_up(game, score, game_size):
    just_merged = np.zeros((game_size,game_size))  # need to trigger just merged so 2nd merge doesnt happen in the same turn!
    for x in range(1, game_size):
        for y in range(0, game_size):
            if game[x,y] != 0:
                hitedge = False
                x2 = x - 1
                while game[x2,y] == 0:
                    # search upwards
                    x2 -= 1
                    if x2 < 0:
                        # hit boundary
                        hitedge = True
                        break
                if hitedge:
                    # put number at edge
                    game[0,y] = game[x,y]
                    game[x,y] = 0
                else:
                    # if numbers same and not merged that turn, then merge
                    if (game[x,y] == game[x2,y]) and (just_merged[x2,y] == 0) and (just_merged[x,y] == 0):
                        game[x2,y] *= 2
                        game[x,y] = 0
                        score += game[x2,y]
                        just_merged[x2,y] = 1
                    elif (x - 1) != x2:
                        # else put adjacent if not already
                        game[x2+1,y] = game[x,y]
                        game[x,y] = 0

    return game, score

def move_down(game, score, game_size):
    just_merged = np.zeros((game_size,game_size))  # need to trigger just merged so 2nd merge doesnt happen in the same turn!
    for x in range(game_size-2, -1, -1):
        for y in range(0, game_size):
            if game[x,y] != 0:
                hitedge = False
                x2 = x + 1
                while game[x2,y] == 0:
                    # search upwards
                    x2 += 1
                    if x2 >= game_size:
                        # hit boundary
                        hitedge = True
                        break
                if hitedge:
                    # put number at edge
                    game[game_size-1,y] = game[x,y]
                    game[x,y] = 0
                else:
                    # if numbers same and not merged that turn, then merge
                    if (game[x,y] == game[x2,y]) and (just_merged[x2,y] == 0) and (just_merged[x,y] == 0):
                        game[x2,y] *= 2
                        game[x,y] = 0
                        score += game[x2,y]
                        just_merged[x2,y] = 1
                    elif (x + 1) != x2:
                        # else put adjacent if not already
                        game[x2-1,y] = game[x,y]
                        game[x,y] = 0

    return game, score

def move_left(game, score, game_size):
    just_merged = np.zeros((game_size,game_size))  # need to trigger just merged so 2nd merge doesnt happen in the same turn!
    for x in range(0, game_size):
        for y in range(1, game_size):
            if game[x,y] != 0:
                hitedge = False
                y2 = y - 1
                while game[x,y2] == 0:
                    # search upwards
                    y2 -= 1
                    if y2 < 0:
                        # hit boundary
                        hitedge = True
                        break
                if hitedge:
                    # put number at edge
                    game[x,0] = game[x,y]
                    game[x,y] = 0
                else:
                    # if numbers same and not merged that turn, then merge
                    if (game[x,y] == game[x,y2]) and (just_merged[x,y2] == 0) and (just_merged[x,y] == 0):
                        game[x,y2] *= 2
                        game[x,y] = 0
                        score += game[x,y2]
                        just_merged[x,y2] = 1
                    elif (y - 1) != y2:
                        # else put adjacent if not already
                        game[x,y2+1] = game[x,y]
                        game[x,y] = 0

    return game, score

def move_right(game, score, game_size):
    just_merged = np.zeros((game_size,game_size))  # need to trigger just merged so 2nd merge doesnt happen in the same turn!
    for x in range(0, game_size):
        for y in range(game_size-2, -1, -1):
            if game[x,y] != 0:
                hitedge = False
                y2 = y + 1
                while game[x,y2] == 0:
                    # search upwards
                    y2 += 1
                    if y2 >= game_size:
                        # hit boundary
                        hitedge = True
                        break
                if hitedge:
                    # put number at edge
                    game[x,game_size-1] = game[x,y]
                    game[x,y] = 0
                else:
                    # if numbers same and not merged that turn, then merge
                    if (game[x,y] == game[x,y2]) and (just_merged[x,y2] == 0) and (just_merged[x,y] == 0):
                        game[x,y2] *= 2
                        game[x,y] = 0
                        score += game[x,y2]
                        just_merged[x,y2] = 1
                    elif (y + 1) != y2:
                        # else put adjacent if not already
                        game[x,y2-1] = game[x,y]
                        game[x,y] = 0

    return game, score

# overlay images using PIL
# https://moonbooks.org/Articles/How-to-overlay--superimpose-two-images-using-python-and-pillow-/
# or opencv
# https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

if DIFFICULTY == 'Easy':
    game_size = 3
elif DIFFICULTY == 'Medium':
    game_size = 4
elif DIFFICULTY == 'Hard':
    game_size = 5

game = np.zeros((game_size,game_size))
# background = cv2.imread("template.png")
# cv2.imshow('image window', image)
# cv2.waitKey(0)
# tiles = cv2.imread("resources.png") #108 wide, 0-107, 108-215 etc...
game = randomise(game, DIFFICULTY, game_size)
GAMESTART = True
print('Game start!!')
print(game)
print('score = ', score)

while GAMESTART is True:
    KEYPRESSED = False
    if (keyboard.read_key() == "w"):
        [game, score] = move_up(game, score, game_size)
        KEYPRESSED = True
    if (keyboard.read_key() == "a"):
        [game, score] = move_left(game, score, game_size)
        KEYPRESSED = True
    if (keyboard.read_key() == "s"):
        [game, score] = move_down(game, score, game_size)
        KEYPRESSED = True
    if (keyboard.read_key() == "d"):
        [game, score] = move_right(game, score, game_size)
        KEYPRESSED = True
    # if keyboard.is_pressed('p'):    # power!
    #     print('to be put in')
    if (keyboard.read_key() == "r"):    # restart (new game)
        print('NEW GAME!')
        game = np.zeros((game_size,game_size))
        score = 0
        game = randomise(game, DIFFICULTY, game_size)
    # if keyboard.is_pressed('u'):    # undo
    #     print('not implemented, too bad!')
    if (keyboard.read_key() == "x"):    # close everything
        #cv2.destroyAllWindows()
        quit()

    if KEYPRESSED:
        game = randomise(game, DIFFICULTY, game_size)
        print(game)
        print('score = ', score)
        # put_to_screen(game, background, tiles, NUMBERS)
        KEYPRESSED = False

    # check if won, then exit
    if np.max(game) == 2048:
        print('YOU WINNER!')
        GAMESTART = False
        if score > MAXSCORE:
            MAXSCORE = score
            # todo save to file!

    #todo check if no moves available
    if np.min(game) > 0:
        # ie no space, and no adjacent tiles with same number!
        print('YOU LOST!')

    #todo increase score, by the sum of the merge
    #todo increase power gauge (not just pre turn, but with number of merges!!)


def put_to_screen(game, background, tiles, NUMBERS):
    a=5
    return
