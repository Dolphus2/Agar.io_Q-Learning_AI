# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:20:39 2022

@author: gabri
"""

import numpy as np

def Closest_Point(Point, Points, PointsConsideredByAbsVal = 0):
    
    Points[:,0:2] = Points[:,0:2] - Point
    
    if PointsConsideredByAbsVal != 0:
        
        Abs = np.abs(Points[:,0:3])
        Points = Abs[np.argsort(Abs[:,0],axis =0)[0:PointsConsideredByAbsVal+1]]
        Points = np.unique(np.append(Points,Abs[np.argsort(Abs[:,1],axis =0)[0:PointsConsideredByAbsVal+1]], axis = 0),axis = 0)
    
    # print(Points)
    # Calculate the euclidian distance to all points
    EucDist = np.linalg.norm(Points[:,0:2],axis=1)
    
    # Subtract the radii of the circles
    EucDistR = EucDist - Points[:,2]
    
    ClosestPoint = Points[np.argmin(EucDistR)]
    
    return ClosestPoint





