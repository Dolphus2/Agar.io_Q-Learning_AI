import mss
import numpy as np
import cv2


def ScreenShot():
    '''
    Take a screenshot and return it as a numpy array
    '''
    with mss.mss() as sct:
        # get screen size of monitor 1 (can be changed to 2 if browser is opened on a second monitor)
        monitor = sct.monitors[1] 

        # Take the screenshot
        img = np.array(sct.grab(monitor))
        
        # Slice the alpha value away, woosh, gone with it!
        img = img[:,:,0:3]
        
        # Flip BGR to RGB
        img = np.flip(img,2)
        
    return img