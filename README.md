# BwLabel function for Python

This script processes binary images to identify and analyze objects within them. It computes various properties such as area, bounding box, centroid, orientation, eccentricity, perimeter, aspect ratio, solidity, and extent. Additionally, it provides 
interactive visualization and property saving options.

## Features

- Detects and labels objects in a binary image;
- Computes various properties for each object;
- Has an interactive mode to inspect objects one by one;
- Allows saving the object properties to a file;
- Computes properties average values for all saved objects;
- Filters and selects objects based on specified property thresholds.

## Requirements

Required dependencies:

```sh
pip install numpy scipy opencv-python skimage screeninfo
```

## Usage

Example image : 

![Example image - binary_image.png](binary_image.png)

**binary_image.png**

### Function ***show_labels_and_props(bin_img)*** - Detect and analyze objects
```py
import cv2
import bwlabel as bw
# Load a binary image
bin_img = cv2.imread("binary_image.png", cv2.IMREAD_GRAYSCALE)
bw.show_labels_and_props(bin_img)

