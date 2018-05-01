#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import numpy as np


class Traking:

    def __init__(self, cam, color_hsv_low=(29, 86, 6), color_hsv_hight=(64, 255, 255)):

        self.cam = cam
        self.greenLower = color_hsv_low
        self.greenUpper = color_hsv_hight

    def tick(self, iteration):
        """
        Ajoute la position de l'objet tracket dans point_que
        :return:
        """
        frame = self.cam.get_current_fram()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # on recupaire la zone qui on les zone de couleur
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        # on fait une erosion et dilation pour supprimer les petit pixel blanc qui peut être pris pour la balle
        mask = cv2.erode(mask, None, iterations=iteration)
        mask = cv2.dilate(mask, None, iterations=iteration)

        cv2.imshow("mask", mask)

        # Recherche de contour pour savoir ou est la balle
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            # on charche le contour le plus grand (celui de la balle)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            moment_cont = cv2.moments(c)
            # on recupaire le centre de la balle
            center = (int(moment_cont["m10"] / moment_cont["m00"]), int(moment_cont["m01"] / moment_cont["m00"]))
            # on controle la taille du rayon de la balle
            if radius > 30:
                # Puis on dessin la boulle
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        return center, frame


if __name__ == "__main__":
    pass
