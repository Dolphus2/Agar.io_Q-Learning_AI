# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:46:58 2022

@author: gabri
"""
import numpy as np

# Takes a screenshot as an array and returns the coordinates for the screen center.
def CenterofScreen(img):
    
    #1080 x 1920
    # Pull dimensions and center as a backup player position
    ScreenDimensions = np.shape(img)
    Center = np.array([ScreenDimensions[1]//2,ScreenDimensions[0]//2])
    # [960, 540]
    return Center, ScreenDimensions