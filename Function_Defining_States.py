# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:50:10 2022

@author: gabri
"""

import numpy as np

# Lige nu laver den de her udregninger hver gang. Jeg kunne også lave
# en anden function til at udregne dem, så vi gør det i starten af Main, og
# så få denne function til bare at udlede staten.

def FoodState(CloseFood, prevplayercirc):

    StartingPoint = 100
    GrowthRate = 1.8
    
    States = np.array([])
    for e in range(3):
        States = np.append(States,StartingPoint*GrowthRate**e)
        
    
    
    State = np.argsort(np.argsort(np.append(States,np.linalg.norm(CloseFood[0:2])-CloseFood[2]-prevplayercirc[0,2])))[3]
    
    return State

def EnemyFoodState(CloseEnemyFood, prevplayercirc):

    Start = 150
    Stop = 600
    States = 3
    
    States = np.linspace(Start,Stop,States-2)
    
    State = np.argsort(np.argsort(np.append(States,np.linalg.norm(CloseEnemyFood[0:2])-CloseEnemyFood[2]-prevplayercirc[0,2])))[1]
    
    return State


def EnemyState(CloseEnemy, prevplayercirc):

    Start = 180
    Stop = 1000
    States = 6
    
    States = np.linspace(Start,Stop,States-2)
    
    State = np.argsort(np.argsort(np.append(States,np.linalg.norm(CloseEnemy[0:2])-CloseEnemy[2]-prevplayercirc[0,2])))[4]
    
    return State




# print(CloseFood)
# print(CloseEnemyFood)
# print(CloseEnemy)


