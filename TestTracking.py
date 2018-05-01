#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from time import time


start = time()
show_res = True
color_hsv_low = (29, 86, 6)
color_hsv_hight = (64, 255, 255)

frame = cv2.imread("ref_img/ball3.jpg")

start_hsv = time()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
print("Temps RGB to HSV ", time() - start_hsv)

start_rang = time()
# on recupaire la zone qui on les zone de couleur
mask = cv2.inRange(hsv, color_hsv_low, color_hsv_hight)
print("Temps range: ", time() - start_rang)

if show_res:
    cv2.imshow("Mask", mask)
    cv2.moveWindow("Mask", 0, 0)

# on fait une erosion et dilation pour supprimer les petit pixel blanc qui peut être pris pour la balle

start_ero = time()
mask = cv2.erode(mask, None, iterations=18)
if show_res:
    cv2.imshow("Erode", mask)
    cv2.moveWindow("Erode", 0, 0)
mask = cv2.dilate(mask, None, iterations=18)
if show_res:
    cv2.imshow("Dilate", mask)
    cv2.moveWindow("Dilate", 0, 0)
print("Temps erosion dilat: ", time() - start_ero)

start_contour = time()
# Recherche de contour pour savoir ou est la balle -2 c'est pour la copatibiliter entre opencv2 et 3
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
print("Temps contour ", time() - start_contour)

center = None
if len(cnts) > 0:
    # on charche le contour le plus grand (celui de la balle)
    c = max(cnts, key=cv2.contourArea)
    contour_frame = mask.copy()
    cv2.drawContours(contour_frame, c, -1, (100, 255, 255), 5)
    if show_res:
        cv2.imshow("Contour", contour_frame)
        cv2.moveWindow("Contour", 0, 0)

    start_circle = time()
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    print("Temps circle ", time() - start_circle)

    moment_cont = cv2.moments(c)
    # on recupaire le centre de la balle
    center = (int(moment_cont["m10"] / moment_cont["m00"]), int(moment_cont["m01"] / moment_cont["m00"]))
    # on controle la taille du rayon de la balle
    if radius > 30:
        # Puis on dessin la boulle
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # cv2.circle(frame, center, 5, (0, 0, 255), -1)
print("Fin temps de calcule: {} sec".format(time() - start))
if show_res:
    cv2.imshow("Frame", frame)
    cv2.moveWindow("Frame", 0, 0)
cv2.waitKey(0)
cv2.destroyAllWindows()

if __name__ == "__main__":
    pass