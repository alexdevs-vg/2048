__author__= 'Alex Pagnozzi'

import argparse
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

SYSTEM = os.name
if SYSTEM == 'posix':
    os.chdir('/home/pag06h/Dev/smages/2048/')
elif SYSTEM == 'nt':
    os.chdir('D:\\Dev\\2048\\')

# index for number tile on tile palette
NUMBERS = {'2.0': 0, '4.0': 1, '8.0': 2,
           '16.0': 3, '32.0': 4, '64.0': 5,
           '128.0': 6, '256.0': 7, '512.0': 8,
           '1024.0': 9, '2048.0': 10}
# score increase based on sequence
FIBONNACI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

def randomise(game, DIFFICULTY):
    if DIFFICULTY == 'Easy':
        num2add = 1
    elif DIFFICULTY == 'Medium':
        num2add = 1 + 1*(np.random.rand(1)>0.5)
    elif DIFFICULTY == 'Hard':
        num2add = 2 + 1*(np.random.rand(1)>0.4)

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

def put_to_screen(game, NUMBERS, score, MAXSCORE, game_size, power):
    # display image
    # background = Image.open("template.png")
    if game_size == 3:
        # todo new image
        background = cv2.imread("template.png")
        gridXY = [148,80]
        WIDTH = 108
        SPACE = 12
    elif game_size == 4:
        background = cv2.imread("template.png")
        gridXY = [148, 80]
        WIDTH = 108
        SPACE = 12
    elif game_size == 5:
        # todo new image
        background = cv2.imread("template.png")
        gridXY = [148, 80]
        WIDTH = 108
        SPACE = 12

    # add number tiles
    tiles = cv2.imread("resources.png")  # 108 wide, 0-107, 108-215 etc...
    for x in range(0, game_size):
        for y in range(0, game_size):
            if game[x,y] > 0:
                ind = NUMBERS[str(game[x,y])]
                number = tiles[:,ind*WIDTH:((ind+1)*WIDTH)]
                tilepos = [gridXY[0]+x*(SPACE+WIDTH), gridXY[1]+y*(SPACE+WIDTH)]
                background[tilepos[0]:(tilepos[0]+WIDTH),tilepos[1]:(tilepos[1]+WIDTH)] = number

    # add power
    if power > 0:
        powerbar = cv2.imread("loadingbar.png")
        height, width, channels = powerbar.shape
        barwidth = int((power / 100) * width)
        print(barwidth)
        background[148:456, 148:(148+barwidth)] = powerbar[:,0:barwidth]

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

def move_up(game, score, game_size, power):
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

    numofcombs = int(np.sum(just_merged))
    power += FIBONNACI[numofcombs]

    return game, score, power

def move_down(game, score, game_size, power):
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

    numofcombs = int(np.sum(just_merged))
    power += FIBONNACI[numofcombs]

    return game, score, power

def move_left(game, score, game_size, power):
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

    numofcombs = int(np.sum(just_merged))
    power += FIBONNACI[numofcombs]

    return game, score, power

def move_right(game, score, game_size, power):
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

    numofcombs = int(np.sum(just_merged))
    power += FIBONNACI[numofcombs]

    return game, score, power

######################## HELP #####################################################################
# overlay images using PIL
# https://moonbooks.org/Articles/How-to-overlay--superimpose-two-images-using-python-and-pillow-/
# or opencv
# https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

def main(args):
    # set difficulty
    DIFFICULTY = args.difficulty  # Easy, Medium, Hard
    if DIFFICULTY == 'Easy':
        game_size = 3
    elif DIFFICULTY == 'Medium':
        game_size = 4
    elif DIFFICULTY == 'Hard':
        game_size = 5
    else:
        DIFFICULTY = 'Medium'
        game_size = 4

    # load old MAX SCORE
    with open('MAXSCORE.json') as score_file:
        score = json.load(score_file)
        for key, value in score.items():
            if key == 'MAXSCORE':
                MAXSCORE = value

    GAMESTART = True
    CANUNDO = True

    # initialise game
    print('Game start!!')
    score = 0
    power = 0
    game = np.zeros((game_size,game_size))
    game = randomise(game, DIFFICULTY)
    put_to_screen(game, NUMBERS, score, MAXSCORE, game_size, power)
    print(game)
    print('score = ', score)

    # initialise undo (i.e. last turn)
    old_score = 0
    old_power = 0
    old_game = np.zeros((game_size,game_size))

    while GAMESTART is True:
        KEYPRESSED = False
        if (keyboard.read_key() == "w"):
            [game, score, power] = move_up(game, score, game_size, power)
            KEYPRESSED = True
        if (keyboard.read_key() == "a"):
            [game, score, power] = move_left(game, score, game_size, power)
            KEYPRESSED = True
        if (keyboard.read_key() == "s"):
            [game, score, power] = move_down(game, score, game_size, power)
            KEYPRESSED = True
        if (keyboard.read_key() == "d"):
            [game, score, power] = move_right(game, score, game_size, power)
            KEYPRESSED = True

        power = int(np.max([100, power])) #max 100%

        # if keyboard.is_pressed('p'):    # power!
        #todo how does power work???
        #     print('to be put in')

        if (keyboard.read_key() == "r"):    # restart (new game)
            print('NEW GAME!')
            game = np.zeros((game_size,game_size))
            score = 0
            power = 0
            game = randomise(game, DIFFICULTY)
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
            old_power = copy.deepcopy(power)

            # update game board
            game = randomise(game, DIFFICULTY)
            print(game)
            print('score = ', score, '\tmaxscore = ', MAXSCORE)
            put_to_screen(game, NUMBERS, score, MAXSCORE, game_size, power)
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
                power = old_power
                put_to_screen(game, NUMBERS, score, MAXSCORE, game_size, power)
                CANUNDO = False
            else:
                print('Can\'t undo!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""\n
    2048!\n
    \n
    The game 2048, with a bit extra.\n
    \n
    Examples of usage:\n
            python 2048.py --difficulty 'Medium'\n
    \n
    Author: Alex Pagnozzi\n
    \n
    """)

    parser.add_argument('--difficulty', type=str, help='Game difficulty, choose:\n\'Easy\' 3x3\n\'Medium\' 4x4\n\'Hard\' 5x5', default='Medium')

    args = parser.parse_args()
    main(args)