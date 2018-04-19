import cv2
import imutils
import numpy as np

# from mouse_click import define_points


def ordered_points(pts):
	"""Create an np array (list) of the input coordinates ordered as top left,
	   top right, bottom right, and then bottom left.

	   Keyword arguments:
	   pts -- list of manually selected points from an image which represents
	   		  the corners of a rectangular shape in the real world
	"""
	rect = np.zeros((4, 2), dtype = "float32")

	pt_sum = pts.sum(axis = 1)
	# Represents the top left corner
	rect[0] = pts[np.argmin(pt_sum)]
	# Represents the bottom right corner
	rect[2] = pts[np.argmax(pt_sum)]

	diff = np.diff(pts, axis = 1)
	# Represents the top right corner
	rect[1] = pts[np.argmin(diff)]
	# Represents the bottom left corner
	rect[3] = pts[np.argmax(diff)]

	return rect


def remove_excess_red(img):

    soln = cv2.imread(img)
    soln_copy = soln.copy()

    rows = soln_copy.shape[0]
    columns = soln_copy.shape[1]

    for i in range(rows):
        for j in range(columns):






def birdseye_correction(img, i):
    """Use homography to transform an image from an angled perspective to a
       rectified image.

    Keyword arguments:
    img -- a string that represents the image path and name

    TODO:
    - Make is so we read in the corners from the app (client)
    - Find a way to make dimensions of the image with its actual proportions
    """
    img = cv2.imread(img,0)

    resized = imutils.resize(img, height = 750)
    copy = resized.copy()

    # # rect = ordered_points(define_points(copy))
    # (tl, tr, br, bl) = rect


    # # Computer width of warped image, which is either the max distance between
    # # the top left and top right corners or the bottom left and bottom right
    # # corners (considering only x coordinates)
    # widthTop = np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
    # widthBottom = np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))

    # maxWidth = max(int(widthTop), int(widthBottom))

    # # compute the height of the new image, which will be the
    # # maximum distance between the top-right and bottom-right
    # # y-coordinates or the top-left and bottom-left y-coordinates
    # heightA = np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
    # heightB = np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
    # maxHeight = max(int(heightA), int(heightB))

    # dst = np.array([[0, 0], \
    # [maxWidth - 1, 0], \
    # [maxWidth - 1, maxHeight - 1], \
    # [0, maxHeight - 1]], dtype = "float32")

    # # compute the perspective transform matrix and then apply it
    # M = cv2.getPerspectiveTransform(rect, dst)
    # warped = cv2.warpPerspective(resized, M, (maxWidth, maxHeight))

    # cv2.imshow("warped", warped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #Bniarize image
    blurred_img = cv2.GaussianBlur(copy,(3,3),0)
    binary = cv2.adaptiveThreshold(blurred_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,31,2)

    #Find the edges of the maze walls and clean up binary walls through
    #   morhpological operations
    kernel = np.ones((3,3),np.uint8)
    edges = cv2.Canny(copy,50,150,apertureSize = 3)
    dilated = cv2.dilate(edges, kernel, iterations = 5)
    eroded = cv2.erode(dilated, kernel, iterations = 3)

    inverted = cv2.bitwise_not(eroded)
    colorImg = cv2.cvtColor(inverted, cv2.COLOR_GRAY2RGB)

    filename = "warped" + str(i) + ".png"

    cv2.imwrite("warped.png", colorImg)

    # # For testing
    # filename = "warped" + str(i) + ".png"

    # cv2.imwrite("warped.png", copy)    



def image_segmentation(img, i):
    """Solve maze image using image segmentation

    Keyword arguments:
    img -- Maze image to be solved
    	   Will only work with perfect mazes (enclosed walls with only
    	   two outer openings)

    @TODO: Get rid of "warped.png"
    """
    img = cv2.imread(img,0)
    resized = imutils.resize(img, height = 750)
    copy = resized.copy()

    copy_color = cv2.cvtColor(copy, cv2.COLOR_GRAY2RGB)

    # Binarizing images for image segmentation
    binary = cv2.adaptiveThreshold(resized,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,101,2)

    inverted = cv2.bitwise_not(binary)
    im2, contours, hierarchy = cv2.findContours(inverted,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # Finding all paths in the maze
    path = np.zeros_like(binary)
    cv2.drawContours(path, contours, 0, (255,255,255), -1)

    # Separates the two groups of enclosed walls and finds the seam between
    # them (this is the actual solution path).
    kernel = np.ones((41,41),np.uint8)
    path = cv2.dilate(path, kernel)

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

    # Take only the maze solution path
    img2_fg = cv2.bitwise_and(colorImg,colorImg,mask = mask)

    # Put solution path in ROI and modify the copy image
    final = cv2.add(img1_bg,img2_fg)
    copy_color[0:rows, 0:cols ] = final

    filename = "solution" + str(i) + ".jpg"

    cv2.imwrite("solution.jpg", copy_color)

    # # For testing

    # filename = "solution" + str(i) + ".jpg"

    # cv2.imwrite("solution.jpg", copy)

#
# def main():
#     birdseye_correction()
#     image_segmentation()
#
# if __name__ == "__main__":
#     main()
