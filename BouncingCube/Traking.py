#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import numpy as np


class Traking:

    def __init__(self, cam, color_hsv_low=(29, 86, 6), color_hsv_hight=(64, 255, 255)):

        self.cam = cam
        self.greenLower = color_hsv_low
        self.greenUpper = color_hsv_hight

    def tick(self):
        """
        Ajoute la position de l'objet tracket dans point_que
        :return:
        """
        frame = self.cam.get_current_fram()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # on recupaire la zone qui on les zone de couleur
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        # on fait une erosion
        mask = cv2.erode(mask, None, iterations=2)
        # est dilatation
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            moment_cont = cv2.moments(c)
            center = (int(moment_cont["m10"] / moment_cont["m00"]), int(moment_cont["m01"] / moment_cont["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # update the points queue
        return center, frame


if __name__ == "__main__":
    pass
