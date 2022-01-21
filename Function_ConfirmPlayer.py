# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:25:17 2022

@author: gabri
"""
import numpy as np

def ConfirmPlayer(img, ScreenDimensions):
    

    Colour = img[ScreenDimensions[0]//2,int(np.round(ScreenDimensions[1]//2))]
    
    return Colour



# imgT = np.transpose(img,(1,0,2))

# ShotTemplate = np.zeros((40,40,3))

# PlayerShot = img[520:560,940:980,0:3]

# Remove white bit with numbers

# PlayerShot = PlayerShot[0:20,0:22,0:3] = 0





# from matplotlib import pyplot as plt
# plt.imshow(img, interpolation='nearest')
# plt.show()



# np.shape(A)
# Out[68]: (1080, 1920, 3)

# np.shape(A[0])
# Out[69]: (1920, 3)

# np.shape(np.transpose(A,(1,0,2)))
# Out[70]: (1920, 1080, 3)

# B = np.shape(np.transpose(A,(1,0,2)))

# B
# Out[72]: (1920, 1080, 3)