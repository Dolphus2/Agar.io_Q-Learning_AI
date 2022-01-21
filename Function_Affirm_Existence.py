# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:25:19 2022

@author: gabri
"""

import numpy as np

def Affirm_Existence(food, enemyfood, enemy, Center):

    # Affirm what elements are on screen 
    FoodExists = True if len(food)>0 else False
    EnemyFoodExists = True if len(enemyfood)>0 else False
    EnemyExists = True if len(enemy)>0 else False
    
    # # Affirm what elements are on screen 
    # FoodExists = True if np.shape(food)[1] != 0 else False
    # EnemyFoodExists = True if np.shape(enemyfood)[1] != 0 else False
    # EnemyExists = True if np.shape(enemy)[1] != 0 else False
    
    # # Affirm our own coordinates and delete ourselves from enemyfood
    # if EnemyFoodExists == True:
    #     EF = np.copy(enemyfood)[:,0:2]-Center
        
    #     EucDist = np.linalg.norm(EF[:,0:2],axis=1)
    #     # Update our position
    #     # enemyfood[EucDist < 60]
        
    #     enemyfood = enemyfood[EucDist > 60]
        
    # # Affirm if there is still enemyfood
    
    # EnemyFoodExists = True if len(enemyfood)>0 else False
    
    return FoodExists, EnemyFoodExists, EnemyExists