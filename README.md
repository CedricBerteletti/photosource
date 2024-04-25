# PhotoSource

## Introduction

PhotoSource is a small project to visualize, process and convert an image (or a batch of images) using python code. It is mainly built upon the OpenCV graphic processing library.

## Launching

If not already created, create the Python virtual environment and install the different package.
```
python.exe -m pip install --upgrade pip
python -m venv .venv
.\.venv\Scripts\activate
pip install PyQt6
pip install opencv-python
```

Activate the Python virtual environment
```
.\.venv\Scripts\activate
```

Launching
```
python photosource.py
```


## Files architecture

4 directories have to be considered :
- The source directory, with the original images.
- The target directory, for the final exports.
- The directory (*.photosource* by default) for the user script for processing each original images *{original_image_name}.{process_id}.py*.
- The directory (*.photosource* by default) containing all the previews and mipmaps of the images :
  - *{original_image_name}{.process_id}{.preview_id}.{mipmap}.png* ;
  - *{original_image_name}{.process_id}.previews.csv* : CSV files listing all previews for the specified image and process

