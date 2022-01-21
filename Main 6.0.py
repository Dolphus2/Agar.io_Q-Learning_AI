#Import libraries
import numpy as np
import time
import pynput.mouse
import pynput.keyboard
from pynput.keyboard import Key, Listener
import random
from collections import defaultdict
from matplotlib import pyplot as plt

from Function_Click_Play import play
# from Function_Time_It import Time_It

from Function_Screenshot_MSS import ScreenShot
from Function_Center_of_Screen import CenterofScreen
from Function_ConfirmPlayer import ConfirmPlayer
from Function_Detect_Categorize_Circles import DetectCategorizeCircles
from Function_Affirm_Existence import Affirm_Existence
from Function_Closest_Point import Closest_Point
import Function_Defining_States as DS # this is not changed bcs variables have the same name as the functions (we could generally try to write variables starting with lower case )
from Function_Read_Score import read_score_G

# alternatively: from Variables_initialize import *
from Variables_initialize import *

import pytesseract
pytesseract.pytesseract.tesseract_cmd = tesspath
import ast
import time
import cv2

import os
import sys

deathcount2 = 0

print('Starting program...')
time.sleep(3)

def on_press(key):
    # print('{0} pressed'.format(key))
    pass

def on_release(key):
    if key == Key.esc:
        global dead
        global run
        run = False
        dead = True

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while run:

    #Tries to load txt-file with the saved dictionary from the previous game. If the file doesn't exist then it passes. 
    try:
        load = open(qtablePath, "r")
        contents = load.read()
        AgarQTable = ast.literal_eval(contents) #Converts back from string to dictionary

    except FileNotFoundError:
        print('FileNotFoundError')
        # AgarQTable = defaultdict(lambda: [0, 0, 0])
        AgarQTable = defaultdict(lambda: [120,120,120])
        AgarQTable[-1,-1,-1] = [0,0,0]
        if SelfSizeState:
            AgarQTable[-1,-1,-1,"small"] = [0,0,0]
            AgarQTable[-1,-1,-1,"medium"] = [0,0,0]
            AgarQTable[-1,-1,-1,"big"] = [0,0,0]
            
    #Initializes game
    StartImg = play(15)
    
    #Gets player position and dimensions of computer screen
    Center, ScreenDimensions = CenterofScreen(StartImg)

    #State of alive/dead:
    dead = False
    ColourSet = False

    mouse.position = (960,540)

    # Give the circles some time to appear
    time.sleep(1)


    Going = False
    
    # Initialise some variables needed for states and actions for the very first frame
    OSD = 0
    reward = 0
    score = 10
    print("reward reset", reward)
    #Loop that continues and trains AI until death

    t = time.time()
    while not dead:

    
        #Score and screenshot
        img = ScreenShot()

        
        if not ColourSet:
            
            Colour = ConfirmPlayer(img, ScreenDimensions)
            
            #If there's an disconnect screen
            if np.all(Colour == np.array([240,56,56])):
                print("Oh no. Red disconnect screen!")
                break
            
            if np.all(Colour == np.array([255, 255, 255])):
                print("Oh no. Disconnect screen! White!")
                break
            
            ColourSet = True


        # Categorize circles into arrays for food, enemyfood, enemies and the player.

        food, enemyfood, enemy, prevplayercirc = DetectCategorizeCircles(Colour, prevplayercirc,img, foodbound, enfoodbound, enbound, middleCheck, ScreenDimensions, imagescale)


        # Affirm what elements are on screen.
        FoodExists, EnemyFoodExists, EnemyExists = Affirm_Existence(food, enemyfood, enemy, Center)    
        
        # Our state consists of three values. The distance to nearest food, distance to edible cell and distance to dangerous cell.
        # State representations: Finds closest food/enemyfood/enemy
        CloseFood = Closest_Point(prevplayercirc[0,:2],np.copy(food)) if FoodExists else -1
        CloseEnemyFood = Closest_Point(prevplayercirc[0,:2],np.copy(enemyfood)) if EnemyFoodExists else -1
        CloseEnemy = Closest_Point(prevplayercirc[0,:2],np.copy(enemy)) if EnemyExists else -1
        
        
        # Determine the state from the distance to the closest food/ediblecell/enemy
        #If not represented in the image, the state-value will become -1
        FoodState = DS.FoodState(CloseFood, prevplayercirc) if FoodExists else -1
        EnemyFoodState = DS.EnemyFoodState(CloseEnemyFood, prevplayercirc) if EnemyFoodExists else -1
        EnemyState = DS.EnemyState(CloseEnemy, prevplayercirc) if EnemyExists else -1
        
        # Update Size State
        if prev_score <= 50: Size = "small"
        elif prev_score <= 110: Size = "medium"
        else: Size = "big"
            
       
        # Check whether our own colour is still in the center
        if np.all(Colour != ConfirmPlayer(img, ScreenDimensions)):
            print("Can't find colour")
            
            if np.all(img[1038,30] != np.array([254,254,254])):
                print("Can't find white score")
                
                mouse.position = Center
                time.sleep(3)
    
                img = ScreenShot()
    
                # Note: deathpixel has the structure: [row, col]  meaning [i,j] or [y,x]
                deathpixel = np.array([0.3*ScreenDimensions[0],0.5*ScreenDimensions[1]], dtype = int)


                if (img[deathpixel[0],deathpixel[1]] == np.array([255,255,255])).all():
                    print('Death iterations:' + str(deathcount))
                    deathcount += 1
                    dead = True
        
  
    
        #Checks if the saved dictionary contains required key. If not, it sets the def value to [0, 0, 0]
        if (FoodState, EnemyFoodState, EnemyState, Size) not in AgarQTable:
            
            # AgarQTable[FoodState, EnemyFoodState, EnemyState] = [0,0,0]
            
            # Optimistic initialisation
            AgarQTable[FoodState, EnemyFoodState, EnemyState, Size] = [120,120,120]
         
        # Now update our stateRewards to match our new state
        StateRewards = AgarQTable[FoodState, EnemyFoodState, EnemyState, Size]
        
        # 1. choose an action

        greedy = random.random()
        # print([FoodState, EnemyFoodState, EnemyState])
        #If one of the categorized cell types aren't present, that action will be omitted
        if -1 in [FoodState, EnemyFoodState, EnemyState, Size]:
            indices = []
            if FoodState != -1: indices.append(0)
            if EnemyFoodState != -1: indices.append(1)
            if EnemyState != -1: indices.append(2)
            # print(indices)

            #If none were detected
            if len(indices) == 0: 
                dead = True
                deathcount2 += 1

            if not dead:
                #Doesn't take a random action if greedy is under 0.9 (epsilon value)
                if greedy <= EpsilonGreedyBound:
                    ValidChoiceValues = np.array(AgarQTable[FoodState, EnemyFoodState, EnemyState, Size])[indices]
                    ShouldDo = np.random.choice(np.flatnonzero(ValidChoiceValues == ValidChoiceValues.max()))
                    # print("Not a random action: ", ShouldDo)
                #Does take a random action
                else:
                    ShouldDo = random.randint(0, len(indices) - 1)
                    print("Random action: ", actions[ShouldDo])

                #Corrects the index
                if 0 not in indices: ShouldDo += 1
                if 1 not in indices: ShouldDo += 1 
                if ShouldDo == 1:
                    if 0 in indices and 1 not in indices: 
                        ShouldDo -= 1
                # print("Printer efter udregninger: ", ShouldDo)
        else:
            indices = [0,1,2]
            #Doesn't take a random action if greedy is under 0.9 (epsilon value)
            if greedy <= EpsilonGreedyBound:
                ValidChoiceValues = np.array(AgarQTable[FoodState, EnemyFoodState, EnemyState, Size])[indices]
                ShouldDo = np.random.choice(np.flatnonzero(ValidChoiceValues == ValidChoiceValues.max()))
                # print("Not a random action: ", ShouldDo)
            #Does take a random action
            else:
                ShouldDo = random.randint(0, 2)
                print("Random action: ", actions[ShouldDo])

        
        # 2. step the environment
        if not dead:
            try:
                # Keep taking the old action with updated information, if less than 0.5 seconds have passed and that action is still available.
                if Chil == True and Going == True and time.time() - t < 0.5 and [FoodState, EnemyFoodState, EnemyState, Size][OSD] != -1:
                    action = actions[OSD]
                    # print('Chillin for a second')
                    Chillin = True
                else:
                    action = actions[ShouldDo]
                    t = time.time()
                    Chillin = False
                    # reset reward
                    # reward = 0
                    # print(action)
                
                if action == "Eat":
                    mouse.position = (CloseFood[0:2] + Center)
                elif action == "Chase":
                    mouse.position = (CloseEnemyFood[0:2] + Center)
                elif action == "Flee":
                    mouse.position = (- CloseEnemy[0:2] + Center)
            except Exception as e:
                print(ShouldDo)
                print(e)
                
                break
            
        if dead:
            Chillin = False
        
  
        if ReadScore:
    # =============================================================================
            if not dead:
                #read the score
                score, screenshot = read_score_G(img) # OBS forskellig

    
                # delete all non numbers
                numeric_filter = filter(str.isdigit, score)
                score = "".join(numeric_filter)
            else:
                score = str(prev_score)
                
    
            
            if len(score) != 0:
                score = int(score)
                if score in range(prev_score + 1, prev_score + 10):
                    reward += 1
                else:
                    if not (score > timesbiggerbound * prev_score or score + 10 < prev_score) and score > prev_score: # the + 10 is just a dummy thing, this will work very badly if we get very big and begin to shrink
                        reward += score - prev_score
                        print("big reward firing", reward)
                prev_score = score
                
            if UpdateTable or PrintStates:
                
                # Update reward
                if dead:
                    print("dead reward", reward, action)
                    if action == 'Flee':
                        reward -= 100
                    else:
                        reward -= 100
                    print("dead reward post", reward)
                else:
                    if Chillin == False:
                        reward += 1
                   
                if dead:
                    assert reward > -101
                else:
                    assert reward >= 0
                
            
                # 3. Update q-table, but with the updated state 
                
                # Update q-table as we now know our new state
                # print(reward)
                if Going == True and Chillin == False:
                    print([OFS, OEFS, OES, OS], AgarQTable[OFS, OEFS, OES, OS], OA, reward)
                    
                    if len(indices) == 0 or dead:
                        print("Dead update", reward)
                        if UpdateTable: OSR[OSD] = reward
                        
                        print([OFS, OEFS, OES, OS], AgarQTable[OFS, OEFS, OES, OS], OA, reward, "dead")
                        # print(indices)
        
                    
                    else:
                        if UpdateTable: OSR[OSD] = reward + gamma * np.max(np.array(AgarQTable[FoodState, EnemyFoodState, EnemyState, Size])[indices])
                        print([OFS, OEFS, OES, OS], AgarQTable[OFS, OEFS, OES, OS], OA, reward, "alive")
                    
                    if dead:
                        # print([OFS, OEFS, OES], AgarQTable[OFS, OEFS, OES], action, reward)
                        print([FoodState, EnemyFoodState, EnemyState, Size], AgarQTable[FoodState, EnemyFoodState, EnemyState, Size])
                    
                    # Reset reward after i has been chashed basically
                    reward = 0
                    
                Going = True
                
                if dead == False and Chillin == False:
                    OFS, OEFS, OES, OS = FoodState, EnemyFoodState, EnemyState, Size
                    OSR, OSD, OA = StateRewards, ShouldDo, action
                
                
                #When dead, all q-table states/rewards are converted again from string to dictionary
                if dead and UpdateTable:
                    #Overwrites the previous dictionary with an updated one as a string       
                    with open(qtablePath, "w") as file:
                        file.write(str(dict(AgarQTable)))
                    
            # =============================================================================
                
    time.sleep(3)
    
    board = ScreenShot()
    
    # Crops the screenshot to just the scoreboard. Needs to be calibrated to the display.
    board = board[182:381, 804:1116]
    
    # Save the images to a specific folder and number them. These paths of course need to be personalised.
    os.chdir(r'C:\Users\Gabriel\OneDrive - Danmarks Tekniske Universitet\Skrivebord\Agar.io Projekt\Score Screens 13.1.2022 2\Experiment {}'.format(Experiment))
    save_board = cv2.imwrite(r'C:\Users\Gabriel\OneDrive - Danmarks Tekniske Universitet\Skrivebord\Agar.io Projekt\Score Screens 13.1.2022 2\Experiment {}\run_{}.png'.format(Experiment, str(iteration)), board)
    print(save_board)
    
    if save_board:
        Pictures += 1
        print(Pictures)
        print(iteration)


    if ReadScore: ScoreList = np.append(ScoreList, score)

    # Exit full screen and close the tab
    time.sleep(1)
    keyboard = pynput.keyboard.Controller()
    
    keyboard.press(Key.f11)
    time.sleep(0.1) #Due to delay so the button isn't pressed and released almost simultaneously
    keyboard.release(Key.f11)
    
    
    # Deletes the current tab
    with keyboard.pressed(Key.ctrl):
        keyboard.press('w')
        keyboard.release('w')
        
    iteration += 1
        
with keyboard.pressed(Key.alt):
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
time.sleep(0.1)


time.sleep(0.5)


# plt.imshow(img, interpolation='nearest')
# plt.show()


