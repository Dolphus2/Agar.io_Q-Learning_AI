import numpy as np
from collections import defaultdict
import pynput.mouse

#Whether pc is a mac or not
macPC = False

# tesseract path
tesspath = r'C:\Users\Gabriel\anaconda3\envs\Agar.ioProjekt\Library\bin\tesseract.exe'

# This is not a realistic initialization - although the scenario where this matters should be incredibly rare if not impossible if there's no problem with going into the game 
prevplayercirc = np.array([[960,540,50]])

# AgarQTable = defaultdict(lambda: [0,0,0])

# optimistic initialisation
AgarQTable = defaultdict(lambda: [120,120,120])

prev_score = 10
ScoreList = np.array([])

mouse = pynput.mouse.Controller()

deathcount = 0
Pictures = 0

run = True


#Detect Categorize variables
foodbound = 4
enfoodbound = -0.25
enbound = 0.25
middleCheck = 0.10
imagescale = 2

# q-learning variables
gamma = 0.99
actions = ['Eat','Chase','Flee']
timesbiggerbound = 9


qtablePath = r'C:/Users/Gabriel/OneDrive - Danmarks Tekniske Universitet/Lokale Filer/Vigtige Mapper fra Omen 15/DTU/Efterår 2021/Introduktion til Intelligente Systemer/Eksamensprojekt Januar/Things that run/11.01.2022 Run/Q table/QTable.txt'

iteration = 29
Experiment = '18'

Chil = True

ReadScore = False
UpdateTable = False
PrintStates = True

# Not Random = 2
# Only Random = -1
EpsilonGreedyBound = 2

SelfSizeState = True
# Size = "small"

