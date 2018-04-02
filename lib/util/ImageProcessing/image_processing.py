import cv2
import numpy as np
import imutils
# from collections import defaultdict
from mouse_click import define_points


def ordered_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")

	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# return the ordered coordinates
	return rect

def birdseye_correction(img = "angled.jpg"):
    img = cv2.imread(img,0)
    resized = imutils.resize(img, height = 750)
    copy = resized.copy()

    rect = ordered_points(define_points(copy))
    print (rect)
    (tl, tr, br, bl) = rect

	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))
    widthB = np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
    heightB = np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0], \
    [maxWidth - 1, 0], \
    [maxWidth - 1, maxHeight - 1], \
    [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(resized, M, (maxWidth, maxHeight))

    cv2.imshow("warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #Bniarize image
    blurred_img = cv2.GaussianBlur(warped,(3,3),0)
    binary = cv2.adaptiveThreshold(blurred_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,31,2)

    #Find the edges of the maze walls and clean up binary walls through
    #   morhpological operations
    kernel = np.ones((3,3),np.uint8)
    edges = cv2.Canny(warped,50,150,apertureSize = 3)
    dilated = cv2.dilate(edges, kernel, iterations = 5)
    eroded = cv2.erode(dilated, kernel, iterations = 1)

    inverted = cv2.bitwise_not(eroded)
    colorImg = cv2.cvtColor(inverted, cv2.COLOR_GRAY2RGB)

    cv2.imwrite("warped.png", colorImg)


def image_segmentation(img = "warped.png"):
    img = cv2.imread(img,0)
    resized = imutils.resize(img, height = 500)
    copy = resized.copy()

    copy_color = cv2.cvtColor(copy, cv2.COLOR_GRAY2RGB)

    binary = cv2.adaptiveThreshold(resized,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,101,2)

    denoised = cv2.fastNlMeansDenoising(binary,None,21,21)


    inverted = cv2.bitwise_not(binary)
    im2, contours, hierarchy = cv2.findContours(inverted,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    cv2.imshow("solution?", inverted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("How many:", len(contours))

    path = np.zeros_like(binary)
    cv2.drawContours(path, contours, 0, (255,255,255), -1)

    cv2.imshow("contours", path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    kernel = np.ones((30,30),np.uint8)
    path = cv2.dilate(path, kernel)

    cv2.imshow("path", path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    eroded = cv2.erode(path, kernel)

    dst = cv2.absdiff(path, eroded)

    colorImg = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)

    colorImg[:,:,0] = 0
    colorImg[:,:,1] = 0

    #Creating ROI (AKA, selecting the solution path)
    rows,cols,channels = copy_color.shape
    roi = copy_color[0:rows, 0:cols ]

    # Now create a mask of solution path and the inverse mask
    img2gray = cv2.cvtColor(colorImg,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(colorImg,colorImg,mask = mask)

    # Put solution path in ROI and modify the copy image
    final = cv2.add(img1_bg,img2_fg)
    copy_color[0:rows, 0:cols ] = final

    cv2.imwrite("solution.jpg", copy_color)



def main():
    birdseye_correction()
    image_segmentation()

if __name__ == "__main__":
    main()
