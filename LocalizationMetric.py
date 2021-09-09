# -*- coding: utf-8 -*-
"""

# author          :     Laura Purcaro
# title           :     LocalizationMetric.py
# description     :     Helper function for Evaluation metrics.py
# date            :     02.05.2021
# version         :     1.0
# python_version  :     3.8.8


"""

# Libraries
import cv2
import numpy as np
import random as rng

###########################################################################
# Localization metric:
# It compares the exact location of predicted folds in an image with 
# the folds on the ground truth image. 
# Hence, the metric will consider only folds that match in both masks and 
# calculate a score over the number of matches.
###########################################################################

def LocalizationMetric(slide_n,groundtruth,prediction):
    # Set random seed
    rng.seed(12345)
    
    # Apply filters for better contouring
    blur1 = cv2.blur(groundtruth, (3,3))
    blur2 = cv2.blur(prediction, (3,3))

    ret, thresh = cv2.threshold(blur1, 127, 255,0)
    ret, thresh2 = cv2.threshold(blur2, 127, 255,0)

    kernel = np.ones((5,5),np.uint8)
    dilation1 = cv2.dilate(groundtruth,kernel,iterations = 1)
    dilation2 = cv2.dilate(prediction,kernel,iterations = 1)
    
    # Contours for both groundtruth and prediction images
    contours1,hierarchy1 = cv2.findContours(dilation1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours2,hierarchy2 = cv2.findContours(dilation2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    '''Create bounding boxes for Ground truth image'''
    # Create empty list with lenght as contours1
    contours_poly1 = [None]*len(contours1)
    boundRect1 = [None]*len(contours1)
    
    # Approximate contours to polygons + get bounding rects
    for i, c in enumerate(contours1):
        # It approximates a contour shape to another shape with less number of vertices
        contours_poly1[i] = cv2.approxPolyDP(c, 3, True)
        # Find a bounding rect for every polygon
        boundRect1[i] = cv2.boundingRect(contours_poly1[i])
        
        # Create new Mat of unsigned 8-bit chars, filled with zeros. 
        # It will contain all the drawings we are going to make (rects)
        drawing1 = np.zeros((thresh.shape[0], thresh.shape[1], 3), dtype=np.uint8)

    # For every contour: pick a random color, draw the contour and the bounding rectangle
    for i in range(len(contours1)):
        color1 = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv2.drawContours(drawing1, contours_poly1, i, color1)
        cv2.rectangle(drawing1, (int(boundRect1[i][0]), int(boundRect1[i][1])), \
              (int(boundRect1[i][0]+boundRect1[i][2]), int(boundRect1[i][1]+boundRect1[i][3])), color1, 2)

    '''Create bounding boxes for Prediction image'''
    # Create empty list with lenght as contours2
    contours_poly2 = [None]*len(contours2)
    boundRect2 = [None]*len(contours2)
    
    # Approximate contours to polygons + get bounding rects
    for i, c in enumerate(contours2):
        contours_poly2[i] = cv2.approxPolyDP(c, 3, True)
        boundRect2[i] = cv2.boundingRect(contours_poly2[i])

        drawing2 = np.zeros((thresh2.shape[0], thresh2.shape[1], 3), dtype=np.uint8)
        
    for i in range(len(contours2)):
        color2 = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        
        cv2.drawContours(drawing2, contours_poly2, i, color2)
        # Draw rectangle
        cv2.rectangle(drawing2, (int(boundRect2[i][0]), int(boundRect2[i][1])), \
              (int(boundRect2[i][0]+boundRect2[i][2]), int(boundRect2[i][1]+boundRect2[i][3])), color2, 2)
    
    '''Extract mass center from Prediction image'''
    gt_match = []

    # Get the moments
    mu = [None]*len(contours2)
    for i in range(len(contours2)):
        mu[i] = cv2.moments(contours2[i])

    # MASS CENTER of folds objects, not rectangle
    # Get the mass centers
    mc = [None]*len(contours2)
    for i in range(len(contours2)):
        # add 1e-5 to avoid division by zero
        mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
        # Draw the mass center
        cv2.circle(drawing2, (int(mc[i][0]), int(mc[i][1])), 4, color2, -1)
            
    # If the folds' mass center of the prediction image is inside the rectangle 
    # of groundtruth image, append the match
    for i in range(len(contours2)):
        # Mass center coords
        x = mc[i][0]
        y = mc[i][1]

        for j in range(len(contours1)):
            #Rectangle vertices coords
            x1 = int(boundRect1[j][0])
            y1 = int(boundRect1[j][1])
            x2 = int(boundRect1[j][0]+boundRect1[j][2])
            y2 = int(boundRect1[j][1]+boundRect1[j][3])

            if (x1 < x and x < x2):
                if (y1 < y and y < y2):
                    gt_match.append(j)
            pass
    
    print("Slide n.", slide_n)   
    print('Tot ground truth objects: {}'.format(len(contours1)))
    print('Tot prediction objects: {}'.format(len(contours2)))

    unique = list(set(gt_match))
    print('Tot match: {}'.format(len(unique)))
    
    # Avoid division by 0
    try:
        percentage = (len(unique)/len(contours1))*100
    except ZeroDivisionError:
        percentage = 0
    
    slide_number = "Study n."+str(slide_n)
    print('Percentage of exact location: {}%.  {} out of {}'.format(round(percentage),len(unique), len(contours1))) 
    
    return slide_number, len(contours1), len(contours2), len(unique), percentage


# Make the module callable
if __name__ == "__main__":
    
    LocalizationMetric()




