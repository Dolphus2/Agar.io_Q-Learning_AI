import numpy as np
from skimage.measure import label, regionprops
import cv2
import time
import math




def DetectCategorizeCircles(Colour, prevplayercirc,img, foodbound = 4, enfoodbound = -0.25, enbound = 0.25, middleCheck=0.10, ScreenDimensions = (1080, 1920, 3), imagescale = 2):
    img = cv2.resize(img, (0, 0), fx=imagescale**-1, fy=imagescale**-1)
    
    prevplayercirc = prevplayercirc*(imagescale**-1)
    '''
    Function that categorizes and identifies the objects on a screenshot-input (img)

    preplayercirc: previous playerposition + centercoord
    img: screenshot-input
    foodbound: foodtolerance, how many pixels longer can the radius of the circle be than the smallest food-circle to be considered a food circle's radius
    enfoodbound: percentage (of area) the player has to be bigger than an object for the object to be considered eatable
    enbound: same as enfoodbound, but this time it's how much bigger than the player an object is, for it to be considered enemy that can eat us
    middleCheck: how big of an area we'll check for the circle (+/- percentage of picture size from the center)

    '''

    # Get the screen dimensions
    ScreenDimensions = np.array(np.shape(img))
    
    # Every pixel with a cell or food as at least RGB value set to 255. We can use this to identify them
    # Create a matix of the same size with 255 in all positions
    FullColour = np.full(ScreenDimensions,255)
    
    # Compare it to our matrix with 255 everywhere to make a binary matrix of where circles are present.
    CirclesTrue = np.any(img == FullColour, axis = 2)
    
    
    # Get the screen dimensions
    ScreenDimensions = ScreenDimensions[0:2]           
    


    # ignore the score as potential detected objects
    scorebounds = np.array(np.array([0.96,0.076]) * ScreenDimensions, dtype=int)
    CirclesTrue[scorebounds[0]:,:scorebounds[1]] = False
    

    # Create labels over the binary array, seperating each area of 0
    newimg = label(CirclesTrue)


    # Make labels into regions with information about the regions
    props = regionprops(newimg)

    # get the centroid coordinates of the circle and radius.
    det_circ = np.empty((0,3))
    for prop in props:
        det_circ = np.vstack((det_circ, [prop.centroid[1],prop.centroid[0],0.5*prop.major_axis_length])) # we're selecting major axis
    det_circ = det_circ.astype(int)
    

    TotCirc = len(det_circ)
    assert det_circ.ndim == 2
    
    # Do not consider tiny circles, as these are almost always a mistake
    
    TinyRad = 7/imagescale
    
    NotTiny = np.full(TotCirc, TinyRad) < det_circ[:,2]
    det_circ = det_circ[NotTiny]
    
    # Reset the circle count
    TotCirc = len(det_circ)
    assert det_circ.ndim == 2
    
    # Do not consider circles with centers in the outer borders of the screen
    # as these are most likely not fully in view. This corrosponds to a border of about 30 pixels.
    
    
    VBoundProportion, HBoundProportion = 0.0278, 0.0157
    
    # TopBound, BotBound, LeftBound, RightBound
    ScreenBounds = np.array([VBoundProportion*ScreenDimensions[0], (1-VBoundProportion)*ScreenDimensions[0], HBoundProportion*ScreenDimensions[1], (1-HBoundProportion)*ScreenDimensions[1]], dtype = int)
    
    # Compare bounds against detected circles
    TopLeft = np.vstack((np.full(TotCirc, ScreenBounds[2]), np.full(TotCirc, ScreenBounds[0]))).T
    BotRight = np.vstack((np.full(TotCirc, ScreenBounds[3]), np.full(TotCirc, ScreenBounds[1]))).T
    
    # Seperate out detected circles on the edge
    BorderCirc = np.all(np.hstack((TopLeft < det_circ[:,:2], det_circ[:,:2] < BotRight)), axis = 1)
    
    det_circ = det_circ[BorderCirc]
    
    # Reset the circle count
    TotCirc = len(det_circ)
    assert det_circ.ndim == 2

    # find center of image
    center = ScreenDimensions // 2

    #bordcent structure: [lowest i, highest i, lowest j, highest j]
    lowestmid = center - center * middleCheck
    highestmid = center + center * middleCheck

    lowestmid = lowestmid.astype(int)
    highestmid = highestmid.astype(int)
    
    # Turn them into arrays to vectorize the comparisons
    Lowmid = np.vstack((np.full(TotCirc, lowestmid[1]), np.full(TotCirc, lowestmid[0]))).T
    Highmid = np.vstack((np.full(TotCirc, highestmid[1]), np.full(TotCirc, highestmid[0]))).T


    # Lowmid < A[:,:2] & A[:,:2] < Highmid
    
    # find which circles are in search center-area and seperate them out
    midcirc = np.all(np.hstack((Lowmid < det_circ[:,:2], det_circ[:,:2] < Highmid)), axis = 1)
    
    CheckList, det_circ = det_circ[midcirc], det_circ[~midcirc]
    
    # Reset the circle count
    TotCirc = len(det_circ)
    assert det_circ.ndim == 2
    
    # Make sure the circle has our colour
    CheckList = CheckList[np.all(img[CheckList[:,1], CheckList[:, 0]] == np.full((len(CheckList),3), Colour), axis = 1)]    

    usedprevious = False
    if np.shape(CheckList)[0] == 1:
        playercirc = CheckList
        prevplayercirc = playercirc
        
    elif len(CheckList) == 0:
        playercirc = prevplayercirc # If no player was spotted. This is no implemented yet, as the error should be (almost) impossible to get, and I decided to be a bit lazy
        # The only thing that has to change if we implement this is to initialize a realistic prevplayercirc in the main script
        usedprevious = True
    else:
        # If there are multiple circles, just take the closest one
        dists = np.linalg.norm(CheckList[:,0:2]-center,axis = 1)
        playercirc = np.expand_dims(CheckList[np.argmin(dists)], axis=0)
        prevplayercirc = playercirc
    
    # playercirc should be a 2-dimensional array with one circle in it
    
    assert det_circ.ndim == 2



    enfoodbound = int(math.sqrt(( playercirc[:,2][0]**2 ) * (1 + enfoodbound)))
    enbound = int(math.sqrt( (playercirc[:,2][0]**2)*(1 + enbound)))
    # Categorize circles into arrays for food, enemyfood and enemies.
    if len(det_circ) == 0:
        # If there weren't any circles detected
        food = np.array([])
        enemyfood = np.array([])
        enemy = np.array([])

     
    # if there are none, then define:

    else:
        
        foodrad = np.amin(det_circ)
        foodbound = foodrad
        food = np.asarray([det_circ[i] for i,e in enumerate(det_circ) if det_circ[i,2] <= foodrad + foodbound])
        
        # Lets fix this enemyfood dammit
        
        enemyfood = det_circ[np.all(np.vstack((det_circ[:,2] < np.full(TotCirc, enfoodbound), det_circ[:,2] > np.full(TotCirc, foodrad + foodbound))).T, axis = 1)]
        if len(enemyfood) != 0:
            # Check if the color is the same, if you check within 2/3 of the radius in the 4 cardinal directions
            NotEF = np.array([],dtype = bool)
            
            for i, ef in enumerate(enemyfood):
                
                # Sort for viruses. They always have the same colour
                if np.all(img[ef[1],ef[0]] == np.array([51, 255, 51])):
                    NotEF = np.append(NotEF, False)
                
                elif ef[2] >= ScreenBounds[0]:
                    NotEF = np.append(NotEF, True)
                else:
                    EnCol = img[ef[1],ef[0]]
                    EnColStack = np.vstack((EnCol,EnCol,EnCol,EnCol))
                    
                    EnColUp, EnColDown, EnColLeft, EnColRight, = img[ef[1]-int(ef[2]*(2/3)),ef[0]], img[ef[1]+int(ef[2]*(2/3)),ef[0]], img[ef[1], ef[0]-int(ef[2]*(2/3))], img[ef[1], ef[0]+int(ef[2]*(2/3))]
                
                    EnColStack4 = np.vstack((EnColUp, EnColDown, EnColLeft, EnColRight))
                
                    NotEF = np.append(NotEF, np.all(EnColStack == EnColStack4))
            
            # Now scram all fake enemy food
            enemyfood = enemyfood[NotEF]
        if len(enemyfood) == 0:
            enemyfood = np.array([])

 

        
        
        enemy = np.asarray([det_circ[i] for i,e in enumerate(det_circ) if det_circ[i,2] > enbound])


    # resize it to normal coords
    food = imagescale*food
    enemyfood = imagescale*enemyfood
    playercirc = imagescale*playercirc
    enemy = imagescale*enemy
    prevplayercirc = imagescale*prevplayercirc

    # ------------------------------------------------------------------------------------------
    #To draw circles:
    # img = cv2.resize(img, (0, 0), fx=2, fy=2)
    # for pt in playercirc:
    #     a, b, r = pt[0], pt[1], pt[2]

    #     # Draw the circumference of the circle.
    #     cv2.circle(img, (a, b), r, (255, 255, 255), 2)

    #     # Draw a small circle (of radius 1) to show the center.
    #     cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

    # for pt in food:
    #     a, b, r = pt[0], pt[1], pt[2]

    #     # Draw the circumference of the circle.
    #     cv2.circle(img, (a, b), r, (255, 0, 0), 2)

    #     # Draw a small circle (of radius 1) to show the center.
    #     cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

    # for pt in enemyfood:
    #     a, b, r = pt[0], pt[1], pt[2]

    #     # Draw the circumference of the circle.
    #     cv2.circle(img, (a, b), r, (0, 255, 0), 2)

    #     # Draw a small circle (of radius 1) to show the center.
    #     cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

    # for pt in enemy:
    #     a, b, r = pt[0], pt[1], pt[2]

    #     # Draw the circumference of the circle.
    #     cv2.circle(img, (a, b), r, (0, 0, 255), 2)

    #     # Draw a small circle (of radius 1) to show the center.
    #     cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

    # from matplotlib import pyplot as plt
    # plt.imshow(img, interpolation='nearest')
    # plt.show()

    return food, enemyfood, enemy, prevplayercirc



