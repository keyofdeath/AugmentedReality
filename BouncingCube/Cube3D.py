#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BouncingCube import *
import cv2


class Cube3D:

    def __init__(self, width, height):

        self.longeur = 1
        self.largeur = 1
        self.hauteur = 1

        self.vertices = [
            # Plan arrière x, y, z
            Point3D(-self.longeur, self.hauteur, -self.largeur),
            Point3D(self.longeur, self.hauteur, -self.largeur),
            Point3D(self.longeur, -self.hauteur, -self.largeur),
            Point3D(-self.longeur, -self.hauteur, -self.largeur),
            # Plan avent
            Point3D(-self.longeur, self.hauteur, self.largeur),
            Point3D(self.longeur, self.hauteur, self.largeur),
            Point3D(self.longeur, -self.hauteur, self.largeur),
            Point3D(-self.longeur, -self.hauteur, self.largeur)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]

        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.height, self.width, = width, height
        self.pos_x, self.pos_y = self.width / 2, self.height / 2

    def set_x_y(self, x, y):

        self.pos_x = x
        self.pos_y = y

    def draw_cube(self, img):

        # Will hold transformed vertices.
        t = []

        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(self.pos_x, self.pos_y, 100, 4)
            # Put the point in the list of transformed vertices
            t.append(p)

        for f in self.faces:
            cv2.line(img, (int(t[f[0]].x), int(t[f[0]].y)), (int(t[f[1]].x), int(t[f[1]].y)), (255, 255, 255))
            cv2.line(img, (int(t[f[1]].x), int(t[f[1]].y)), (int(t[f[2]].x), int(t[f[2]].y)), (255, 255, 255))
            cv2.line(img, (int(t[f[2]].x), int(t[f[2]].y)), (int(t[f[3]].x), int(t[f[3]].y)), (255, 255, 255))
            cv2.line(img, (int(t[f[3]].x), int(t[f[3]].y)), (int(t[f[0]].x), int(t[f[0]].y)), (255, 255, 255))


if __name__ == "__main__":
    pass