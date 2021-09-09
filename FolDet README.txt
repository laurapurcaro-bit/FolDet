# FolDet.py
 
 The algorithm aims to visualize and detect tissue folds.
 In this algorithm, the Enhanced brightness filter is used.
 Input:
 - collection of WSI in single folder
 Output: 
 - WSI with contoured folds saved in 'Output WSI'
 - excel file 'Folds info.xlsx' with:
      >  Study n.; Tissue area; Folds area; N° of folds; % Folded area; optional: Accepted/Rejected
 - optional: WSI classified as 'Accepted' or 'Rejected' directory based on folds info

**Set up**

Python Version 3.8.8

Install requirements

`pip install -r requirements.txt`


**Run Code**
To run FolDet.py open the file into a python IDE and press run. NOTE: copy the python file within the same path of WSI folder.
Note that there are additional helper files within Folds detection-master directory. 
The documentation can be found within the code.



# Folds detection.py
 
 The algorithm is prior to FolDet.py and aims to visualize and detect tissue folds.
 In this algorithm, three main approaches are presented for folds detection and evaluated with Evaluation metrics.py.