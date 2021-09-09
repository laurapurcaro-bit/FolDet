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

## Whole slide images properties
A WSI usually has an extremely high magnification, such as 20x or 40x. Because of the great magnification,
whole slide pictures are often rather huge. The maximum file size for a single whole-slide image in our dataset
was 3.0 GB, with an average over 1 GBA microscope scans a slide and merges tiny pictures into a huge picture
to form a whole-slide picture. Merging scanned square tiles into a whole-slide image and combining scanned
strips into a resultant whole-slide image are examples of techniques. Because of the high file size, each
image's height and width ranged from 13,347 to 256,256 pixels, with an average of 73,154 pixels.
OpenSlide is a Python interface to the OpenSlide library that allows you to read whole-slide photos with ease.
These photos can be tens of gigabytes in size when uncompressed, making them difficult to interpret using
normal tools or libraries meant for pictures that can be quickly uncompressed into RAM. Whole-slide images
are often multi-resolution and OpenSlide allows reading a small amount of image data at the resolution
closest to a specific zoom level.

OpenSlide library has an important function called `level_count` that read the number of levels in the slide.
Levels are numbered from 0 (highest resolution) to `level_count - 1` (lowest resolution). Resolution 0 is
the full-resolution plane while resolutions 1 to 8 are reduced along the X and Y dimensions using a consistent
downsampling factor.



```python

```

