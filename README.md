                          # WORK IN PROGRESS
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
<ul>
  <li>Based on Python3 and OpenCV library</li>
  <li>OpenSlide was utilized for reading WSI, and Pillow for basic image manipulation in Python.</li>
  <li>NumPy was used for fast, concise, powerful processing of images as NumPy arrays. </li>
  <li>Scikit-image heavily works with a wide variety of image functionality, such as morphology, thresholding, and edge detection.</li>
</ul>

# Aim
<ul>
  <li>Visualize and detect tissue folds from low-pixel resolution WSI (.png images) and use this information to determine bad quality tissue slides from good quality tissue slides for diagnosis.</li>
  <li>Since the amount of dye absorbed by the tissue is a function of its thickness, the tissue folds being thicker will appear darker (lower luminance) and will express stronger color saturation compared to adjacent non-folded areas. Hence, three color enhancement methods based on the luminance and saturation properties of tissue folds will be described.</li>
  <li>The best from the three proposed algorithms could be optimized for a future use into the diagnostic lab routine as an upgrade for the current quality control process.</li>
</ul>

Developing color filters that can be used to highlight and detect tissue areas can be challenging for a variety of reasons, including:
1. Filters need to be general enough to work across all slides in the dataset.
2. Filters should handle issues such as variations in shadows and lighting.
3. The amount of H&E (purple and pink) staining can vary greatly from slide to slide.
4. Folds colors vary from purple and pink to dark red due to different reasons i.e., thickness, staining duration, blood infiltration in tissue.

The algorithm can be divided into:
  - WSI pre-processing
  - Filter application
  - WSI classification

## 1. Whole slide images pre-processing
a) Retrieve current working directory with ```os.path.abspath(os.getcwd())```
b) Crop and keep only tissue area and do downscaling.
    example:
  <p align="center">
    <kbd>
      <img style='border:1px solid #000000' src="Images/study n.3.png?raw=true" width="300" height="400"/>
    </kbd>
    <kbd>
      <img src="Images/no crop study no.3.png?raw=true" width="200" height="400" border="1"/>
    </kbd>
    <br>
    <em>Figure 1. Cropped and no cropped WSI</em>
  </p>

## 2. Filter application
### a) Approach 1: Contrast stretch
In the contrast stretch approach we tried to take advantage of low intensity pixel values with the ```rescale_intensity()``` function, that stretches or shrinks the intensity levels of the image given a min and max values. As described before, the in_range parameter defines a linear mapping from the original image to the modified image. The intensity range of the input image can be chosen with in_range parameter and it was the only parameter used for the output image. If the minimum/maximum value of in_range is greater than the maximum and less than the minimum value of the image intensity, the intensity level will be clipped, that is, only the intensity level within the range of in_range will be retained.

<p align="center">
<img src="Images/contrast stretch workflow.PNG?raw=true" width="270" height="400"/><img src="Images/CS_mod.PNG?raw=true" width="550" height="400"/>
  <br>
  <em>Figure 2. Contrast stretch workflow</em>
</p>

### b) Approach 2: HSV
<ul>
  <li>In HSV, it is easier to represent a color than in RGB color-space:</li>
  <ol>
    <li>Unlike RGB, HSV separates luma, or the image intensity, from chroma or the color information.</li>
    <li>The RGB color information is usually much noisier than the HSV information</li>
  </ol>

  <li>One of the most efficient ways to increase an image's color contrast while keeping its hue (color) is to convert the image's original RGB color to HSV (hue, saturation, value) color space and use only the saturation channel or luminance portion of its pixel.</li>
  <li>Saturation and luminance enhancement are traditionally accomplished by performing forward and reverse color transformations between the RGB and HSV color spaces:</li>
  <ol>
    <li>The original RGB colors of the pixels are transformed into their HSV color equivalents in the forward color transformation, where the color saturation or luminance of the image pixels is showed.</li>
    <li>The reverse color transition, from HSV to RGB, is then done to see the result of the change (enhanced image).</li>
  </ol>
</ul>

#### BGR2HSV
To produce an image that is only in the saturation channel, we must first convert our BGR image to HSV color space using ```cv2.COLOR_BGR2HSV``` method and then split the HSV channels and pick the saturation one using ```hsv[:,:,1]```.

<p align="center">
<img src="Images/HSV images.png?raw=true" width="700" height="350"/>
  <br>
  <em>Figure 3. Example of channel’s types in HSV color space. In order: Hue, Saturation, Value.</em>
  <br>
</p>

The resulting image is then read in grayscale mode and thresholded with the method ```cv2.THRESH_BINARY``` of ```cv2.threshold()```. With the performance of the previous method, the thresholding no longer needs to be strong. The above will generate a binary mask, which will be used for object detection in ```cv2.findContours()```. The ```cv2.drawContours()``` function is used to visualize the detected folds. 

<p align="center">
<img src="Images/HSV workflow.PNG?raw=true" width="300" height="450"/>&nbsp;&nbsp;<img src="Images/HSV_GIFT.gif" width="300" height="450"/>
  <br>
  <em>Figure 4. HSV workflow</em>
</p>

### c) Approach 2: Brightness enhanced
Contrast enhancement (CE) refers to the image enhancement on contrast by adjusting the dynamic range of pixel intensity distribution. CE plays an important role in the improvement of visual quality for computer vision, pattern recognition and digital image processing. In real applications, we usually encounter digital images with poor contrast or abnormal brightness, which may result from different factors, such as the deficiency of imaging devices. The capturing scenes with low or high illuminance intensity may also lead to reduced contrast quality. Despite of visual quality degradation, low contrast might hinder the further applications of a digital image, including image analysis and object recognition. As such, it is essential to enhance the contrast and brightness of such distorted images before further applications.

In this step we used the function ```ImageEnhance.Brightness()``` from the Python Imaging Library (PIL). This class can be used to control the brightness of an image, i.e., an enhancement factor of 0.0 gives a black image, while a factor of 1.0 gives the original image. First of all, it is required to create an object of the corresponding class in order to enhance the image, enhancer = ImageEnhance.Brightness(im), second enhancer.enhance(factor) is used for the enhancing. Figure 5 displays the difference between a standard enhancing factor of 1.5 and 2. In this approach, a factor of 2 was selected.












