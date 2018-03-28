#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
import cv2
import numpy as np


class Traking:

    def __init__(self, cam, buffer=1024, color_hsv_low=(29, 86, 6), color_hsv_hight=(64, 255, 255)):

        self.cam = cam
        self.buffer = buffer
        self.greenLower = color_hsv_low
        self.greenUpper = color_hsv_hight
        self.point_que = deque(maxlen=buffer)

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
        self.point_que.appendleft(center)

    def draw_point(self, img):
        """
        Dessine la liste des point dans l'image donnée
        :param img:
        :return:
        """

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if self.point_que[i - 1] is None or self.point_que[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(self.buffer / float(i + 1)) * 2.5)
            cv2.line(img, self.point_que[i - 1], self.point_que[i], (0, 0, 255), thickness)


if __name__ == "__main__":
    pass
