import cv2
import numpy as np
import imutils
from collections import defaultdict

# mouse callback function
def define_points(target_img):
    corners  = []
    refPt = []
    def draw_circle(event,x,y,flags,param):
        global refPt
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(param,(x,y),5,(255,0,0),-1)
            refPt = [x,y]
            print(type(refPt))
            corners.append(refPt)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle, target_img)
    while(1):
        cv2.imshow('image',target_img)
        k = cv2.waitKey(20) & 0xFF
        # corners.append(refPt)
        if k == 27:
            break
    cv2.destroyAllWindows()
    print (corners)
    new_corners = np.array(corners)

    return new_corners

def order_points(pts):
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

def segment_by_angle_kmeans(lines,k=2, **kwargs):
    """Groups lines based on angle with k-means.

    Uses k-means on the coordinates of the angle on the unit circle
    to segment `k` angles inside `lines`.
    """

    # Define criteria = (type, max_iter, epsilon)
    default_criteria_type = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))
    flags = kwargs.get('flags', cv2.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get('attempts', 10)

    # returns angles in [0, pi] in radians
    angles = np.array([line[0][1] for line in lines])
    # multiply the angles by two and find coordinates of that angle
    pts = np.array([[np.cos(2*angle), np.sin(2*angle)]
                    for angle in angles], dtype=np.float32)

    # run kmeans on the coords
    labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)  # transpose to row vec

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in zip(range(len(lines)), lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    return segmented

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]

def segmented_intersections(lines):
    """Finds the intersections between groups of lines."""

    intersections = []
    for i, group in enumerate(lines[:-1]):
        for next_group in lines[i+1:]:
            for line1 in group:
                for line2 in next_group:
                    intersections.append(intersection(line1, line2))

    return intersections


def isEqual(l1, l2):
    length1 = sqrtf((l1[2] - l1[0])*(l1[2] - l1[0]) + (l1[3] - l1[1])*(l1[3] - l1[1]))
    length2 = sqrtf((l2[2] - l2[0])*(l2[2] - l2[0]) + (l2[3] - l2[1])*(l2[3] - l2[1]))

    product = (l1[2] - l1[0])*(l2[2] - l2[0]) + (l1[3] - l1[1])*(l2[3] - l2[1])

    if (fabs(product / (length1 * length2)) < cos(CV_PI / 30)):
        return false

    mx1 = (l1[0] + l1[2]) * 0.5
    mx2 = (l2[0] + l2[2]) * 0.5

    my1 = (l1[1] + l1[3]) * 0.5
    my2 = (l2[1] + l2[3]) * 0.5
    dist = sqrtf((mx1 - mx2)*(mx1 - mx2) + (my1 - my2)*(my1 - my2))

    if (dist > max(length1, length2) * 0.5):
        return false

    return true


def birdseye_correction(img = "angled.jpg"):
    img = cv2.imread(img,0)
    resized = imutils.resize(img, height = 1000)
    copy = resized.copy()

    rect = order_points(define_points(copy))
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

    # gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    blurred_img = cv2.GaussianBlur(warped,(3,3),0)
    binary = cv2.adaptiveThreshold(blurred_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,31,2)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel, iterations = 2)
    # Apply edge detection method on the image
    edges = cv2.Canny(warped,50,150,apertureSize = 3)
    #
    cv2.imshow("edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges,1,np.pi/180, 140)

    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for line in lines:
        for r,theta in line:
            # Stores the value of cos(theta) in a
            a = np.cos(theta)
            # Stores the value of sin(theta) in b
            b = np.sin(theta)
            # x0 stores the value rcos(theta)
            x0 = a*r
            # y0 stores the value rsin(theta)
            y0 = b*r
            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
            x1 = int(x0 + 1000*(-b))
            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
            y1 = int(y0 + 1000*(a))
            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
            x2 = int(x0 - 1000*(-b))
            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
            y2 = int(y0 - 1000*(a))

            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
            # (0,0,255) denotes the colour of the line to be
            # In this case, it is red.
            cv2.line(warped,(x1,y1), (x2,y2), (0,0,255),2)

    # labels = []
    # num_lines = partition(lines, labels, isEqual)

    # define criteria, number of clusters(K) and apply kmeans()
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 54, 1.0)
    # K = 54
    # ret,label,center=cv2.kmeans(lines,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    #
    # # Now convert back into uint8, and make original image
    # center = np.uint8(center)
    # res = center[label.flatten()]
    # print(res.shape, img.shape)
    # # res2 = res.reshape((img.shape))
    # cv2.imshow('res',res)
    # res2 = cv2.resize(res, warped.shape);
    # cv2.imshow('img', img)
    # cv2.imshow('res2',res2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    cv2.imwrite("unclustered_lines.jpg", warped)
    #
    cv2.imshow("lines", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # segmented = segment_by_angle_kmeans(lines)
    # intersections = segmented_intersections(segmented)

    # print(intersections)

    # draw the intersection points
    # intersectsimg = img.copy()
    # for cx, cy in zip(intersections):
    #     cx = np.round(cx).astype(int)
    #     cy = np.round(cy).astype(int)
    #     color = np.random.randint(0,255,3).tolist() # random colors
    #     cv2.circle(intersectsimg, (cx, cy), radius=2, color=color, thickness=-1) # -1: filled circle
    #
    #
    # cv2.imshow("intersections", intersectionimg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



def main():
    birdseye_correction()


if __name__ == "__main__":
    main()

