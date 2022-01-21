# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 16:13:18 2022

@author: gabri
"""

import cv2
import numpy as np

import time
import webbrowser 
import pynput.mouse
from pynput.mouse import Button
import pynput.keyboard
from pynput.keyboard import Key
import math
import os
from Function_Screenshot_MSS import ScreenShot

def play(t = 15):
    
    #Start the game:
    
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()
    
    #Open browser to play agari.io
    webbrowser.open_new("https://agar.io")
    
    #Waits until browser has loaded
    time.sleep(t)
    
    #%%
    #Move mouse position to "play" button
    
    img = ScreenShot()
    
    # Flip the RGB informatino, så it actually corresponds to RGB.
    
    # img = np.flip(img,2)
    # print(img[380,960])
    
    ScreenDimensions = np.shape(img)
    # (1080, 1920, 3) for me.
    # PlayPosition is about (ScreenDimensions[1]/2, ScreenDimensions[0]/3)
    
    # It is the only green thing in the center of the screen.
    imgVert = img[:,ScreenDimensions[1]//2,:]
    Green = np.array([])
    for i, e in enumerate(imgVert):
        if np.all(e == [84, 200, 0]):
            Green = np.append(Green, i)
            mouse.position = (ScreenDimensions[1]//2, i+10)
            break


    # print(imgVert[350])
    #%%
    
    
    #click to start the game
    mouse.press(Button.left)
    time.sleep(0.1) #Due to delay so the button isn't pressed and released almost simultaneously
    mouse.release(Button.left)
    
    time.sleep(1)
    
    #Enters full-screen mode
    # with keyboard.pressed(Key.shift):
    #     keyboard.press(Key.cmd)
    #     keyboard.press('f') 
    
    keyboard.press(Key.f11)
    time.sleep(0.1) #Due to delay so the button isn't pressed and released almost simultaneously
    keyboard.release(Key.f11)
    
    return img