import cv2
import numpy as np


class MouseClicks:
    """Class for mouse click events"""
    corners  = []
    ref_pt = []

    def __init__(self):
        self.data = []

    def draw_point(event,x,y,flags,param):
        """Draw point in the image to represent input points

        Keyword arguments:
        event --
        x --
        y --
        flags --
        param --
        """
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(param,(x,y),5,(255,0,0),-1)
            ref_pt = [x,y]
            print(type(ref_pt))
            corners.append(ref_pnt)

    def define_points(target_img):
        """Manual input of points

        Keyword arguments:
        target_img -- image to apply inputs to (PNG, JPEG, BMP, etc)

        This function is used for testing
        """
        # Open a window of for target_img in order to maunally input points
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_point, target_img)
        while(1):
            cv2.imshow('image',target_img)
            # When esc is pressed, exit window for manually inputting point
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

        new_corners = np.array(corners)

        return new_corners
