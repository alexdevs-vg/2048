__author__= 'Alex Pagnozzi'

import numpy as np
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import keyboard
import json
import cv2
# import cv2.cv as cv
import matplotlib.pyplot as plt
import copy

os.chdir('D:\\Dev\\2048\\')

GAMESTART = True
CANUNDO = True
DIFFICULTY = 'Medium' #todo, Easy, Medium, Hard
NUMBERS = {'2.0': 0, '4.0': 1, '8.0': 2,
           '16.0': 3, '32.0': 4, '64.0': 5,
           '128.0': 6, '256.0': 7, '512.0': 8,
           '1024.0': 9, '2048.0': 10}

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

    zeros = np.argwhere(game == 0)
    num2add = np.min([num2add, len(zeros)])
    for i in range(0, int(num2add)):
        if len(zeros) < 1:
            break

        ind = int(np.random.rand(1) * len(zeros))
        [r,c] = zeros[ind]
        np.delete(zeros,ind)
        game[r,c] = 2 + 2*((np.random.rand(1))>(0.5+ num2add/10))
    return game

def put_to_screen(game, NUMBERS, score, MAXSCORE, game_size):
    # display image
    # background = Image.open("template.png")
    background = cv2.imread("template.png")

    # add number tiles
    tiles = cv2.imread("resources.png")  # 108 wide, 0-107, 108-215 etc...
    WIDTH = 108
    for x in range(0, game_size):
        for y in range(0, game_size):
            if game[x,y] > 0:
                ind = NUMBERS[str(game[x,y])]
                number = tiles[:,ind*WIDTH:((ind+1)*WIDTH)]
                tilepos = [148+x*(12+WIDTH), 80+y*(12+WIDTH)]
                background[tilepos[0]:(tilepos[0]+WIDTH),tilepos[1]:(tilepos[1]+WIDTH)] = number

    # add score text
    # draw = ImageDraw.Draw(background)
    # draw.text((333,88), str(score), (255, 255, 255))
    # draw.text((462,88), str(MAXSCORE), (255, 255, 255))
    font = cv2.FONT_HERSHEY_SIMPLEX     # https://www.oreilly.com/library/view/mastering-opencv-4/9781789344912/16b55e96-1027-4765-85d8-ced8fa071473.xhtml
    scoreText = (333, 88)
    maxscoreText = (462, 88)
    fontScale = 1.2
    fontColor = (255, 255, 255)
    lineType = 2
    cv2.putText(background, str(int(score)), scoreText, font, fontScale, fontColor, lineType)
    cv2.putText(background, str(int(MAXSCORE)), maxscoreText, font, fontScale, fontColor, lineType)

    cv2.imshow('2048! by Alex Pagnozzi', background)
    cv2.waitKey(250)
    return

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

game = randomise(game, DIFFICULTY, game_size)
put_to_screen(game, NUMBERS, score, MAXSCORE, game_size)

GAMESTART = True
print('Game start!!')
print(game)
print('score = ', score)

# undo
old_score = 0
old_game = np.zeros((game_size,game_size))

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
        # undo
        old_score = 0
        old_game = np.zeros((game_size, game_size))
        print(game)
        print('score = ', score, '\tmaxscore = ', MAXSCORE)
    if (keyboard.read_key() == "x"):    # close everything
        cv2.destroyAllWindows()
        quit()

    # update top score
    if score > MAXSCORE:
        MAXSCORE = score
        with open('MAXSCORE.json', 'w', encoding='utf8') as json_file:
            json.dump({'MAXSCORE': MAXSCORE}, json_file, allow_nan=False)

    if KEYPRESSED:
        # store old game/score
        old_game = copy.deepcopy(game)
        old_score = copy.deepcopy(score)

        # update game board
        game = randomise(game, DIFFICULTY, game_size)
        print(game)
        print('score = ', score, '\tmaxscore = ', MAXSCORE)
        put_to_screen(game, NUMBERS, score, MAXSCORE, game_size)
        KEYPRESSED = False
        CANUNDO = True

    # check if won, then exit
    if np.max(game) == 2048:
        print('YOU WINNER!')
        GAMESTART = False
        if score > MAXSCORE:
            MAXSCORE = score

    #todo check if no moves available
    if np.min(game) > 0:
        # ie no space, and no adjacent tiles with same number!
        NOADJACENT = True
        for x in range(0, game_size):
            for y in range(0, game_size):
                if x > 0:
                    if game[x-1,y] == game[x,y]:
                        NOADJACENT = False
                if y > 0:
                    if game[x,y-1] == game[x,y]:
                        NOADJACENT = False
        if NOADJACENT:
            print('YOU LOST!')

    # undo if possible
    if (keyboard.read_key() == "u"):    # undo
        if CANUNDO:
            print('Undoing!')
            print(score, old_score)
            print(game, old_game)
            score = old_score
            game = old_game
            put_to_screen(game, NUMBERS, score, MAXSCORE, game_size)
            CANUNDO = False
        else:
            print('Can\'t undo!')

    #todo increase score, by the sum of the merge
    #todo increase power gauge (not just pre turn, but with number of merges!!)
