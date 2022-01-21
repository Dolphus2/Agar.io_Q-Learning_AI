# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 11:11:32 2022

@author: gabri
"""

import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\gabri\anaconda3\Library\bin\tesseract.exe'
from matplotlib import pyplot as plt

def read_score_G(img):
    #Snip screenshot so it only displays score
    img = np.asarray(img)

    #Snip screenshot so it only displays score
    screenshot = img[1030:1060, 100:160]
    


    #Apply custom configurations
    config='--psm 6 outputbase digits --oem 3 -c page_separator='' '

    #Only gray-scaling and thresholding the image
    shot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    shot = cv2.threshold(shot, thresh = 0, maxval = 255, type = cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    
    
    # plt.imshow(shot, interpolation='nearest')
    # plt.show()

    #Apply custom configurations and read the digits
    score = pytesseract.image_to_string(shot, config=config)

    return score , shot