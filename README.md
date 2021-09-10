
# FolDet
Folds detection in Whole slides images


## Abstract
In recent digital pathology studies involving whole-slide images (WSI), researchers avoid tissue artifacts by
manually selecting images or regions-of-interest (ROI). Even though manual selection ensures the quality of
selected tissue regions, it limits the speed and objectivity of analysis by introducing a subjective userinteractive step. 
Moreover, manual selection is a tedious process for large datasets, and thus, their automatic
identification is essential in order to save time and proceed with further analysis. Tissue folding is a common
artifact in histological images that appear when the tissue folds over twice or more by a non-precise cutting
due to defect in the blade edge or when placing it on the microscope slide. The aim of this study is to improve
the visualization and detection of tissue folds from low-pixel resolution images. This information can be used
to determine bad quality tissue slides from good quality tissue slides and therefore, being rejected or
accepted by the algorithm. Here, three automated image analysis methods for identifying tissue folds in
section images are presented and evaluated. The outputs were compared with manually annotated WSI and
evaluated with three different metrics: the widely used Dice score and IoU metrics, and a localization metric
specifically created for this study. Our results showed that the algorithm is able to detect a high percentage
of folds making it possible to standardize a threshold to automate the classification of “Good” and “Folds”
images. Likewise, the huge diversity of tissue types present in this dataset gives a great relevance to this
study, confirming that, although difficult, it is possible to establish a generalized algorithm that works
optimally for the whole dataset.


## Dataset
In order to have an algorithm that correctly detects folds, 220 Whole Slide Images H&E stained **with folds** were used and
220 Whole Slide Images H&E stained **with NO folds** were included to see if the algorithm was accurate with folds-free cases.
In summray, a total of 440 WSI were used for the creation of the algorithm:
- 220 Whole slides images H&E stained labeled as 'with folds' (bad quality) from pathologist
- 220 Whole slides images H&E stained labeled as 'no folds' (good quality) from pathologist

They represented a total of 58 different type of tissues corresponding to 413 patients, including aorta,
appendix, artery, eye, breast, small intestine, duodenum, endometrium, epiglottis, gallbladder, bile duct,
brain, cerebrum, urinary bladder, skin, heart, ileum, jejunum, jaw, bone marrow, colon, larynx, liver, lung,
lymph nodes, stomach, oral cavity, oral mucosa, nose, paranasal sinus, nervous system, kidney, esophagus,
ear, omentum, ovary, pancreas, parotid gland, penis, peritoneum, pharynx, placenta, cervix uteri, prostate,
rectum, seminal vesicle, thyroid gland, skeletal muscle, vocal fold, synovial tissue, tonsils and adenoids,
uterine tube, ureter, urethra, uterus, soft tissue, cecum and tongue.

## FolDet algorithm
Python3 and the OpenCV package were widely used in this project since it is an appropriate language for
image processing. As a result, cv2.imread() was used to read all .png images for improved synchronization with the rest of the functions. 
It is worth noting that it reads the images in the inverted BGR channels.
In this study, OpenSlide was utilized for reading the WSI files, and Pillow for basic image manipulation in Python. 
NumPy was used for fast, concise, powerful processing of images as NumPy arrays. 
Scikit-image heavily works with a wide variety of image functionality,such as morphology, thresholding, and edge detection. 

Step 1: Install required libraries

```python
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
```

Step 2: Define the path

```python
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
```

























