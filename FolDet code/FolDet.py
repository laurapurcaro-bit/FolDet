# -*- coding: utf-8 -*-
"""

# author          :     Laura Purcaro
# title           :     FolDet.py
# description     :     Folds detection in WSI
# date            :     02.05.2021
# version         :     1.0
# python_version  :     3.8.8


"""

# Libraries
import cv2
import openslide as op
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import pandas as pd
from PIL import Image, ImageEnhance
from scipy import ndimage
import util
import shutil


###########################################################################
# FolDet: 
# The algorithm aims to visualize and detect tissue folds.
# In this algorithm, the Enhanced brightness filter is used.
# Output: 
# - WSI with contoured folds saved in 'Output WSI'
# - excel file 'Folds info.xlsx' with:
#     >  Study n.; Tissue area; Folds area; N° of folds; % Folded area; optional: Accepted/Rejected
# - optional: WSI classified as 'Accepted' or 'Rejected' directory based on folds info
###########################################################################

'''Define the path'''
# Get current working directory
current_path = os.path.abspath(os.getcwd())


# At the same level of "Folds detection", input the folder's NAME (not the path) with all the WSI.mrxs
path_with_wsi = current_path + '\\' + str(input('Input your Whole slide images folder NAME (ex. .mrxs): '))


# Create new folder where all results will be stored
new_path = current_path + '\\' + 'Folds detection'

# If "Folds detection" folder does not exist, create it
if not os.path.exists(new_path):
    os.makedirs(new_path, exist_ok=True)

print('Successfully created: ', new_path)
print('Your WSI path for good: ', path_with_wsi)



'''Convert all WSI from .mrxs to .png'''
#  WSI name should follow the pattern "study n. 4"

# For folds
for filename in os.listdir(path_with_wsi):
    if filename.endswith(".mrxs"):
        # Create file path
        file_path = os.path.join(path_with_wsi, filename)
        
        
        # Open the image
        wsi = op.OpenSlide(file_path)
        # Decide at what level we want to process the slides
        #print(wsi.level_count) # It is counts how many levels has the image (9 in this case)
        #print(wsi.level_downsamples) # It is counts the 2^n (n=level) for each 9 levels; 
        # for e.g the first value will be: 2^0= 1.0
        slide_level = 5
    
        #####################################################
        # Read region in order to process the image with numpy
        # Crop the image based on where the tissue starts
        # Remove background from slides (not scanned area)
        ######################################################

        # Starting point of the tissue scanned
        x = wsi.properties[op.PROPERTY_NAME_BOUNDS_X]
        y = wsi.properties[op.PROPERTY_NAME_BOUNDS_Y]
    
        # Dimension of the image of coords x and y
        dim = (int(int(x)),int(int(y)))

        # Maximum width and height of just tissue scanned dimension
        w,h = wsi.properties[op.PROPERTY_NAME_BOUNDS_WIDTH], wsi.properties[op.PROPERTY_NAME_BOUNDS_HEIGHT]
        # Downsampling factor
        wh = (int(int(w)/2**slide_level),int(int(h)/2**slide_level))
        # Reading the image
        img = wsi.read_region(dim,slide_level,wh)
    
        # Convert into an array
        image = np.array(img)
    
        # Remove black background
        image[image[:,:,3]!=255] = 255
    
        # Convert the original RGBA image into RGB image
        RGB_image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
        # Save .png image
        # Create new folder
        wsi_png_dir = new_path + r'\WSI png'
        
        if not os.path.exists(wsi_png_dir):
            os.makedirs(wsi_png_dir, exist_ok=True)
            
        # Remove format of original image (.mrxs) in the string
        new = filename.split(".")
        new.pop()
        new_filename = '.'.join(new)
        
        print('Step 1: Saving {}.png to folder WSI png'.format(new_filename))
        plt.imsave(wsi_png_dir + '\\' + str(new_filename) + '.png', RGB_image)



'''Folds detection'''

# For Folds
for filename in os.listdir(wsi_png_dir):
    if filename.endswith(".png"):
        # Create image path
        file_path2 = os.path.join(wsi_png_dir, filename)
        #read the image
        im = Image.open(file_path2)

        #image brightness enhancer
        enhancer = ImageEnhance.Brightness(im)

        factor = 2 #brightens the image
        im_output3 = enhancer.enhance(factor)
        
        print('Approach 1: Enhancing folded image n.{}'.format(filename))
        # Apply filters
        rgb = util.pil_to_np_rgb(im_output3)
        grayscale = util.filter_rgb_to_grayscale(rgb)
        contrast_stretch = util.filter_contrast_stretch(grayscale, low=0, high=2)
        
        # Create new destination folder
        enhanced_folder = new_path + r'\Output WSI'
        
        if not os.path.exists(enhanced_folder):
            os.makedirs(enhanced_folder, exist_ok=True)
        
        new = filename.split(".")
        remove_last = new.pop()
        new_filename = '.'.join(new)
        
        # Save images in 'Output WSI'
        plt.imsave(enhanced_folder + r'\{}.png'.format(new_filename), contrast_stretch, cmap="gray")
        
# Binary fill
for filename in os.listdir(enhanced_folder):
    if filename.endswith(".png"):
        # Create image path
        file_path3 = os.path.join(enhanced_folder, filename)
        # Read the image
        img = cv2.imread(file_path3,0)
        
        # Apply filters
        ret,thresh2 = cv2.threshold(img,180,255,cv2.THRESH_BINARY) #170
        complement = util.filter_complement(thresh2)
        binary = ndimage.binary_fill_holes(complement, structure=np.ones((5,5))).astype(int)
    
        
        print("Step 2: processing image {}".format(filename))
        
        # Create new destination folder
        threshold_folder = enhanced_folder + r'\Threshold folds'
        
        if not os.path.exists(threshold_folder):
            os.makedirs(threshold_folder,exist_ok=True)
            
        new = filename.split(".")
        remove_last = new.pop()
        new_filename = '.'.join(new)
        
        # Save images in 'Threshold folds'
        plt.imsave(threshold_folder + r"\{}.png".format(new_filename), binary, cmap="gray")


# Noise reduction
for filename in os.listdir(threshold_folder):
    if filename.endswith(".png"):
        # Create image path
        file_path4 = os.path.join(threshold_folder, filename)
        
        # Read the image
        img2 = cv2.imread(file_path4, 0)
        
        # Apply filters
        median = cv2.medianBlur(img2,3)
        ret, thresh = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY)
        
        
        print("Step 2: processing image {}".format(filename))
        
        # Create new destination folder
        noiseRed_folder = enhanced_folder + r'\Noise reduction'
        
        if not os.path.exists(noiseRed_folder):
            os.makedirs(noiseRed_folder,exist_ok=True)
            
        new = filename.split(".")
        remove_last = new.pop()
        new_filename = '.'.join(new)
        
        # Save images in 'Noise reduction' folder
        plt.imsave(noiseRed_folder + r"\{}.png".format(new_filename), thresh, cmap="gray")
        
# Noise reduction contour

for filename in os.listdir(noiseRed_folder):
    if filename.endswith(".png"):
        # Create image path for predicted binary mask
        file_path4 = os.path.join(noiseRed_folder, filename)
        # Create image path for original png image
        file_path5 = os.path.join(wsi_png_dir, filename)
        
        # Read original png image
        original = cv2.imread(file_path5)
        rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        # Read predicted binary mask
        mask = cv2.imread(file_path4, 0)
        # Find contours on predicted binary mask
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # draw all contours
        result = cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)
        print("Step 3: final processing of image {}".format(new_filename))
        
        # Create 'Result' folder
        result_folder = noiseRed_folder + r'\Result'
        if not os.path.exists(result_folder):
            os.makedirs(result_folder, exist_ok=True)
        
        new = filename.split(".")
        remove_last = new.pop()
        new_filename = '.'.join(new)
        
        # Save resulting image in 'Result' folder
        plt.imsave(result_folder + r"\{}_result.png".format(new_filename), result)
        


''' Calculate tissue area and number of folds '''
area_folds_list = []

for filename in os.listdir(noiseRed_folder):
    if filename.endswith(".png"):
        # Create image path for prediction binary mask
        prediction_path = os.path.join(noiseRed_folder, filename)
        # Create image path for original png image
        original_png_path = os.path.join(wsi_png_dir, filename)
        
        new = filename.split(".")
        remove_last = new.pop()
        nr = new[1]
        
        
        #################################
        # Find the total WSI area
        #################################
        
        # Read original png image
        im = cv2.imread(original_png_path, 0)
        
        # Apply filters
        complement = util.filter_complement(im)
        ret, thresh = cv2.threshold(complement, 20, 255, 0)
        
        # Find external contour of original image
        contours1, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # Create array of zeros with the same shape and type as complement image
        out = np.zeros_like(complement)

        # On this output, draw all of the contours that we have detected
        # in white, and set the thickness to be 3 pixels
        r = cv2.drawContours(out, contours1, -1, 255, 3)
        
        # Calculate total WSI area
        Area_tissue = 0
        for idx in range(len(contours1)):
            area = cv2.contourArea(contours1[idx])
            Area_tissue += area
            
        print('N. of slide:', nr)
        print('Area of total tissue:', Area_tissue)
        
        ###################################
        # Find the folds area
        ###################################
        
        # Read prediction mask
        img = cv2.imread(prediction_path,0)
        # Find external contour of tissue folds
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Calculate tissue folds area
        area_folds = 0
        for idy in range(len(contours)):

            area2 = cv2.contourArea(contours[idy])
            area_folds += area2
        
        ##################################
        # Find number of folds
        ##################################
        number_of_folds = len(contours)
        
        # Percentage area of folds / total tissue area
        percentage_foldedArea = math.ceil((area_folds/Area_tissue)*100)
        
        print('Area of folds:',area_folds)
        print('Number of folds:',number_of_folds)
        print('% Folded area:',percentage_foldedArea)
        
        # Acceèted/Rejected value; N/A if 'Decision boundaries' is commented out
        a_or_r = 'N/A'
        
        '''Decision boundaries'''
        
        '''
        # Create Accepted and Rejected folders
        accepted_folder = new_path + r'\Accepted'
        if not os.path.exists(accepted_folder):
            os.makedirs(accepted_folder, exist_ok=True)
            
        rejected_folder = new_path + r'\Rejected'
        if not os.path.exists(rejected_folder):
            os.makedirs(rejected_folder, exist_ok=True)
        
        # Create empty list for both rejected and accepted
        rejected = []
        accepted = []
        
        # Reject or accept WSI based on % of folded area and number of folds
        if percentage_foldedArea >= 1.0 and number_of_folds >= 20:
            rejected.append(original_png_path)
            a_or_r = 'Rejected'
            print("Rejected")
        else:
            accepted.append(original_png_path)
            a_or_r = 'Accepted'
            print("Accepted")
        
        # If rejected, move the Whole slide image into Rejected folder
        for r_path in rejected:
            # or shutil.move(src, destination)
            shutil.copy(r_path, rejected_folder)
        # If accepted, move the Whole slide image into Accepted folder
        for a_path in accepted:
            shutil.copy(a_path, accepted_folder)
        '''
        
        # Save tissue folds info into a list
        area_folds_list.append(str(nr)+';'+str(Area_tissue)+';'+str(area_folds)+\
                               ';'+str(number_of_folds)+';'+str(percentage_foldedArea)+';'+str(a_or_r))


'''Create Folds info.xlsx excel file'''
# Save output "Area of folds" into excel file
df = pd.DataFrame({"Study n.; Tissue area; Folds area; N° of folds; % Folded area; A/R": area_folds_list})

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter(r'Folds detection\Folds info.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and save the output
writer.close()




















