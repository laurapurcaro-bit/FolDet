# -*- coding: utf-8 -*-
"""

# author          :     Laura Purcaro
# title           :     Evaluation metrics.py
# description     :     Evaluation metrics for Folds detection.py
# date            :     02.05.2021
# version         :     1.0
# python_version  :     3.8.8


"""

# Import Libraries
import cv2
import openslide as op
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import re
import LocalizationMetric as LM
import pandas as pd 
from openpyxl import load_workbook
import AppendToExcel as ap

###########################################################################
# Evaluation metrics: 
# The algorithm contains three evaluation metrics for semantic segmentation:
# IoU score metric, Dice score metric, Localization metric (specially created)
###########################################################################

'''Convert manual annotation in png format.
   Background with no tissue will be cropped out.'''

# For Ground truth Folds
for i in glob.glob("Annotation\\Folds\\tiff\\study no.*.tif"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])
        
        # Open .tif mask
        path1 = r"Annotation\Folds\tiff\study no.{}.tif".format(m)
        wsi_tif = op.OpenSlide(path1)
        slide_level = 5
        
        # Open corresponding .mrxs slide number
        path2 = r"WSI Folds\study no.{}.mrxs".format(m)
        wsi = op.OpenSlide(path2)
        # Decide at what level we want to process the slides
        slide_level = 5
    
        # Read region in order to process the image with numpy
        # Starting point of the tissue scanned
        x = wsi.properties[op.PROPERTY_NAME_BOUNDS_X]
        y = wsi.properties[op.PROPERTY_NAME_BOUNDS_Y]
    
        # Dimension of the image is previous x and y
        dim = (int(int(x)),int(int(y)))

        # Maximum width and height of just tissue scanned dimension
        w,h = wsi.properties[op.PROPERTY_NAME_BOUNDS_WIDTH], wsi.properties[op.PROPERTY_NAME_BOUNDS_HEIGHT]
        wh = (int(int(w)/2**slide_level),int(int(h)/2**slide_level))
        
        img = wsi_tif.read_region(dim,slide_level,wh)
        img_wsi = np.array(img)
        RGB_image = cv2.cvtColor(img_wsi, cv2.COLOR_RGB2GRAY)
        
        print('Converting n.{}.tif image into .png'.format(m))
        
        annotation_folder = r'Ground Truth\GT Folds'
        if not os.path.exists(annotation_folder):
            os.makedirs(annotation_folder, exist_ok=True)
        
        plt.imsave(annotation_folder + r"\groundtruth n.{}.png".format(m), RGB_image, cmap="gray")
        
# For Ground truth Good
for i in glob.glob("Annotation\\Good\\tiff\\study no.*.tif"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])
        
        # Open .tif mask
        path1 = r"Annotation\Good\tiff\study no.{}.tif".format(m)
        wsi_tif = op.OpenSlide(path1)
        slide_level = 5
        
        # Open corresponding .mrxs slide number
        path2 = r"WSI Good\study no.{}.mrxs".format(m)
        wsi = op.OpenSlide(path2)
        # Decide at what level we want to process the slides
        slide_level = 5
    
        # Read region in order to process the image with numpy
        # Starting point of the tissue scanned
        x = wsi.properties[op.PROPERTY_NAME_BOUNDS_X]
        y = wsi.properties[op.PROPERTY_NAME_BOUNDS_Y]
    
        # Dimension of the image is previous x and y
        dim = (int(int(x)),int(int(y)))

        # Maximum width and height of just tissue scanned dimension
        w,h = wsi.properties[op.PROPERTY_NAME_BOUNDS_WIDTH], wsi.properties[op.PROPERTY_NAME_BOUNDS_HEIGHT]
        wh = (int(int(w)/2**slide_level),int(int(h)/2**slide_level))
        
        img = wsi_tif.read_region(dim,slide_level,wh)
        img_wsi = np.array(img)
        RGB_image = cv2.cvtColor(img_wsi, cv2.COLOR_RGB2GRAY)
        
        print('Converting n.{}.tif image into .png'.format(m))
        
        annotation_folder_g = r'Ground Truth\GT Good'
        if not os.path.exists(annotation_folder_g):
            os.makedirs(annotation_folder_g, exist_ok=True)
        plt.imsave(annotation_folder_g + r'\groundtruth n.{}.png'.format(m), RGB_image, cmap="gray")
        
'''Evaluation metrics'''

# a) IoU score
# For Folds
slides_number = []
iou_scores_eb = []
iou_scores_cs = []
iou_scores_hsv = []

for i in glob.glob("Ground Truth\\GT Folds\\groundtruth n.*.png"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])

        #prediction = cv2.imread("D:\\Classification\\Denoised gray\\Mask\\mask_denoised n.{}.png".format(m),0)
        prediction_eb = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced folds\study no-{}.png".format(m),0)
        prediction_cs = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Folds\Mask Folds\study no-{}_mask.png".format(m),0)
        prediction_hsv = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Folds\HSV2RGB Folds\Threshold folds\study n.{}.png".format(m),0)
        # Open .png mask (previous .tif mask)
        target = cv2.imread(r"Ground Truth\GT Folds\groundtruth n.{}.png".format(m),0) 

        # Iou score for Enhanced Brightness
        intersection = np.logical_and(target, prediction_eb)
        union = np.logical_or(target, prediction_eb)
        iou_eb = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_eb.append('Study no.'+str(m)+';'+'enhanced b.'+';'+str(iou_eb))

        print('IoU Enhanced Brightness: Study no.'+str(m)+': '+ str(iou_eb))
        
        # Iou score for Contrast stretch
        intersection = np.logical_and(target, prediction_cs)
        union = np.logical_or(target, prediction_cs)
        iou_cs = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_cs.append('Study no.'+str(m)+';'+'contrast stretch'+';'+str(iou_cs))

        print('IoU Contrast stretch: Study no.'+str(m)+': ' + str(iou_cs))
        
        # Iou score for HSV
        intersection = np.logical_and(target, prediction_hsv)
        union = np.logical_or(target, prediction_hsv)
        iou_hsv = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_hsv.append('Study no.'+str(m)+';'+'HSV'+';'+str(iou_hsv))

        print('IoU HSV: Study no.'+str(m)+': ' + str(iou_hsv))
        
# For Good
slides_number = []
iou_scores_eb_g = []
iou_scores_cs_g = []
iou_scores_hsv_g = []

for i in glob.glob("Ground Truth\\GT Good\\groundtruth n.*.png"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])

        #prediction = cv2.imread("D:\\Classification\\Denoised gray\\Mask\\mask_denoised n.{}.png".format(m),0)
        prediction_eb_g = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced good\Noise reduction\study no.{}.png".format(m),0)
        prediction_cs_g = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Good\Mask Good\study no.{}_mask.png".format(m),0)
        prediction_hsv_g = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Good\HSV2RGB Good\Threshold Good\study n.{}.png".format(m),0)
        # Open .png mask (previous .tif mask)
        target_g = cv2.imread(r"Ground Truth\GT Good\groundtruth n.{}.png".format(m),0) 

        # Iou score for Enhanced Brightness
        intersection = np.logical_and(target_g, prediction_eb_g)
        union = np.logical_or(target_g, prediction_eb_g)
        iou_eb_g = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_eb_g.append('Study no.'+str(m)+';'+'enhanced b.'+';'+str(iou_eb_g))

        print('IoU Enhanced Brightness: Study no.'+str(m)+': '+ str(iou_eb_g))
        
        # Iou score for Contrast stretch
        intersection = np.logical_and(target_g, prediction_cs_g)
        union = np.logical_or(target_g, prediction_cs_g)
        iou_cs_g = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_cs_g.append('Study no.'+str(m)+';'+'contrast stretch'+';'+str(iou_cs_g))

        print('IoU Contrast stretch: Study no.'+str(m)+': ' + str(iou_cs_g))
        
        # Iou score for HSV
        intersection = np.logical_and(target_g, prediction_hsv_g)
        union = np.logical_or(target_g, prediction_hsv_g)
        iou_hsv_g = np.sum(intersection) / np.sum(union)

        #Append results on a list
        iou_scores_hsv_g.append('Study no.'+str(m)+';'+'HSV'+';'+str(iou_hsv_g))

        print('IoU HSV: Study no.'+str(m)+': ' + str(iou_hsv_g))


# b) Dice score
# For Folds
dice_score_hsv_f = []
dice_score_contrast_f = []
dice_score_enhanced_f = []

for i in glob.glob("Ground Truth\\GT Folds\\groundtruth n.*.png"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])

        #prediction = cv2.imread("D:\\Classification\\Denoised gray\\Mask\\mask_denoised n.{}.png".format(m),0)
        prediction_eb_f = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced folds\Noise reduction\study no-{}.png".format(m),0)
        prediction_cs_f = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Folds\Mask Folds\study no-{}_mask.png".format(m),0)
        prediction_hsv_f = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Folds\HSV2RGB Folds\Threshold Folds\study n.{}.png".format(m),0)
        # Open .png mask (previous .tif mask)
        target_f = cv2.imread(r"Ground Truth\GT Folds\groundtruth n.{}.png".format(m),0) 
        
        
        # Dice similarity function
        def dice(pred, true, k = 255):
            intersection = np.sum(pred[true==k]) * 2.0
            dice = intersection / (np.sum(pred) + np.sum(true))
            return dice

        # Dice score for
        dice_score_col_eb_f = dice(prediction_eb_f, target_f, k = 255)
        
        # Dice score for
        dice_score_col_cs_f = dice(prediction_cs_f, target_f, k = 255)
        
        # Dice score for
        dice_score_col_hsv_f = dice(prediction_hsv_f, target_f, k = 255)
        
        
        '''Append results on a list'''
        
        print('Study no.'+str(m)+' Dice score enhanced b. : '+ str(dice_score_col_eb_f))
        dice_score_enhanced_f.append('Study no.'+str(m)+';'+'enhanced b.'+';'+str(dice_score_col_eb_f))
        print('Study no.'+str(m)+' Dice score contrast stretch : '+ str(dice_score_col_cs_f))
        dice_score_contrast_f.append('Study no.'+str(m)+';'+'contrast stretch'+';'+str(dice_score_col_cs_f))
        print('Study no.'+str(m)+' Dice score HSV : '+ str(dice_score_col_hsv_f))
        dice_score_hsv_f.append('Study no.'+str(m)+';'+'HSV'+';'+str(dice_score_col_hsv_f))

        


# For Good
dice_score_hsv_g = []
dice_score_contrast_g = []
dice_score_enhanced_g = []

for i in glob.glob("Ground Truth\\GT Good\\groundtruth n.*.png"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        m = int(m[i])

        #prediction = cv2.imread("D:\\Classification\\Denoised gray\\Mask\\mask_denoised n.{}.png".format(m),0)
        prediction_eb_g = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced good\Noise reduction\study no.{}.png".format(m),0)
        prediction_cs_g = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Good\Mask Good\study no.{}_mask.png".format(m),0)
        prediction_hsv_g = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Good\HSV2RGB Good\Threshold Good\study n.{}.png".format(m),0)
        # Open .png mask (previous .tif mask)
        target_g = cv2.imread(r"Ground Truth\GT Good\groundtruth n.{}.png".format(m),0) 
        
        
        # Dice similarity function
        def dice(pred, true, k = 255):
            intersection = np.sum(pred[true==k]) * 2.0
            dice = intersection / (np.sum(pred) + np.sum(true))
            return dice

        # Dice score for
        dice_score_col_eb_g = dice(prediction_eb_g, target_g, k = 255)
        
        # Dice score for
        dice_score_col_cs_g = dice(prediction_cs_g, target_g, k = 255)
        
        # Dice score for
        dice_score_col_hsv_g = dice(prediction_hsv_g, target_g, k = 255)
        
        
        '''Append results on a list'''
        
        print('Study no.'+str(m)+' enhanced b. : '+ str(dice_score_col_eb_g))
        dice_score_enhanced_g.append('Study no.'+str(m)+';'+'enhanced b.'+';'+str(dice_score_col_eb_g))
        print('Study no.'+str(m)+' contrast stretch : '+ str(dice_score_col_cs_g))
        dice_score_contrast_g.append('Study no.'+str(m)+';'+'contrast stretch'+';'+str(dice_score_col_cs_g))
        print('Study no.'+str(m)+' HSV : '+ str(dice_score_col_hsv_g))
        dice_score_hsv_g.append('Study no.'+str(m)+';'+'HSV'+';'+str(dice_score_col_hsv_g))



# c) Localization metric
# For Folds
loc_contrast_f = []
loc_enhanced_f = []
loc_hsv_f = []
for i in glob.glob("Annotation\\Folds\\tiff\\study no.*.tif"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        slide_n = int(m[i])
        imgA = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced folds\Noise reduction\study no-{}.png".format(slide_n),0)
        imgB = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Folds\Mask Folds\study no-{}_mask.png".format(slide_n),0)
        imgC = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Folds\HSV2RGB Folds\Threshold Folds\study n.{}.png".format(slide_n),0)
        img1 = cv2.imread(r"Ground Truth\GT Folds\groundtruth n.{}.png".format(slide_n),0)
        
        a,b,c,d,e = LM.LocalizationMetric(slide_n,imgA,img1)
        f,g,h,i,l = LM.LocalizationMetric(slide_n,imgB,img1)
        m,n,o,p,q = LM.LocalizationMetric(slide_n,imgC,img1)
        
        loc_enhanced_f.append(str(slide_n)+';'+'enhanced b.'+';'+str(b)+';'+str(c)+';'+str(d)+';'+str(e))
        loc_contrast_f.append(str(slide_n)+';'+'contrast stretch'+';'+str(g)+';'+str(h)+';'+str(i)+';'+str(l))
        loc_hsv_f.append(str(slide_n)+';'+'HSV'+';'+str(n)+';'+str(o)+';'+str(p)+';'+str(q))

        
# For Good
loc_contrast_g = []
loc_enhanced_g = []
loc_hsv_g = []
for i in glob.glob("Annotation\\Good\\tiff\\study no.*.tif"):
    # Matching just the number of slide present in the folder JustFolds
    m = re.findall("[0-9]+", i)
    for i in range(0, len(m)): 
        slide_n = int(m[i])
        imgA = cv2.imread(r"Folds detection_prova\Enhanced\Enhanced good\Noise reduction\study no.{}.png".format(slide_n),0)
        imgB = cv2.imread(r"Folds detection_prova\Contrast stretch\Contrast stretch Good\Mask Good\study no.{}_mask.png".format(slide_n),0)
        imgC = cv2.imread(r"Folds detection_prova\HSV\BGR2HSV Good\HSV2RGB Good\Threshold Good\study n.{}.png".format(slide_n),0)
        img1 = cv2.imread(r"Ground Truth\GT Good\groundtruth n.{}.png".format(slide_n),0)
        
        a,b,c,d,e = LM.LocalizationMetric(slide_n,imgA,img1)
        f,g,h,i,l = LM.LocalizationMetric(slide_n,imgB,img1)
        m,n,o,p,q = LM.LocalizationMetric(slide_n,imgC,img1)
        
        loc_enhanced_g.append(str(slide_n)+';'+'Enhanced b.'+';'+str(b)+';'+str(d)+';'+str(e))
        loc_contrast_g.append(str(slide_n)+';'+'Contrast stretch'+';'+str(g)+';'+str(i)+';'+str(l))
        loc_hsv_g.append(str(slide_n)+';'+'HSV'+';'+str(n)+';'+str(p)+';'+str(q))
        

'''Create final excel file'''

# IoU scores data
iou_enhanced = iou_scores_eb + iou_scores_eb_g
iou_contrast = iou_scores_cs + iou_scores_cs_g
iou_hsv = iou_scores_hsv + iou_scores_hsv_g

# Dice score data
dice_score_enh = dice_score_enhanced_f + dice_score_enhanced_g
dice_score_contrast = dice_score_contrast_f + dice_score_contrast_g
dice_score_hsv = dice_score_hsv_f + dice_score_hsv_g

# Localization metric data
local_score_enhanced = loc_enhanced_f + loc_enhanced_g
local_score_contrast = loc_contrast_f + loc_contrast_g
local_score_hsv = loc_hsv_f + loc_hsv_g


# Save output into excel file
df = pd.DataFrame({"Study n.; Filter.; IoU score": iou_enhanced + iou_contrast + iou_hsv})
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(r'Evaluation metrics scores.xlsx', engine='openpyxl')
    
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='IoU score', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.close()

# Append dataframe
df2 = pd.DataFrame({"Study n.; Filter; Dice score": dice_score_enh + dice_score_contrast + dice_score_hsv})

df3 = pd.DataFrame({"Study n.; Filter; N° GT obj.; Tot match; % Folds detected": \
                    local_score_enhanced + local_score_contrast + local_score_hsv})

filename = r'Evaluation metrics scores.xlsx'

ap.append_df_to_excel(filename, df2, header=True, sheet_name='Dice score', index=False)
ap.append_df_to_excel(filename, df3, header=True, sheet_name='Localization score', index=False)







