import cv2 as cv
import numpy as np


def bin_img_preprocessing(rgbimg="test2.jpg"):
    """Gives the binary image representation of an RGB image

    Given an RGB image, do the following image processing steps:
        1) Convert to grayscale
        2) Apply a Gaussian Blurring Filter to smooth image
        3) Convert to a black/white image using Adaptive Gaussian thresholding
        4) Apply morphological operations (opening and then closing)
        5) Apply adaptive Gaussian thresholding again
    Returns a string of the binary image representation file

    Keyword arguments:
    rgbimg -- a string that represents the file of an RGB image of maze
                in JPEG, PNG, TIFF, BMP

    In the future, implement a way to manipulate the image contrast,
        brightness, and  saturation to better preserve maze walls

    """

    img = cv.imread(rgbimg,0)
    blurred_img = cv.GaussianBlur(img,(5,5),0)

    bin_img = cv.adaptiveThreshold(blurred_img,255, \
                  cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)

    for i in range(1, 5):
        bin_img = cv.morphologyEx(bin_img, cv.MORPH_OPEN, \
                      cv.getStructuringElement(cv.MORPH_CROSS,(3,3)))
        bin_img = cv.morphologyEx(bin_img, cv.MORPH_CLOSE, \
                      cv.getStructuringElement(cv.MORPH_CROSS,(3,3)))

    bin_img = cv.adaptiveThreshold(bin_img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY,11,2)

    did_write = cv.imwrite("bin_img.png",bin_img)

    if (did_write):
        return "bin_img.png"


# The main function was for testing purposes
# def main():
#     bin_img_preprocessing()
#
#
# if __name__ == "__main__":
#     main()
