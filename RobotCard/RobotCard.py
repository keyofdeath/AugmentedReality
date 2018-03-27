#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from RobotCard import *
from ImgOperator.Tool import get_4_point_contour
from ImgOperator.Trasformations.VisionTool import *
import ImgOperator as io


class RobotCard(object):

    def __init__(self):

        self.cam = WebCam(True)
        cv2.namedWindow("Main")

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
        self.height, self.width, _ = self.cam.get_current_fram().shape
        self.pos_x, self.pos_y = self.width / 2, self.height / 2

    def test_cube(self):

        self.cam.start()

        step_x = -2
        step_y = 2

        while True:

            img = self.cam.get_current_fram()
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

            self.angleX += 0.5
            self.angleY += 1
            self.angleZ += 1.5

            self.pos_x += step_x
            self.pos_y += step_y

            if self.pos_y >= self.height:
                step_y = -step_y
            elif self.pos_y <= 0:
                step_y = abs(step_y)

            if self.pos_x >= self.width:
                step_x = -step_x
            elif self.pos_x <= 0:
                step_x = abs(step_x)

            cv2.imshow("Main", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cam.stop()

    def start(self):

        while True:
            img = self.cam.get_current_fram()
            screenCnt = get_4_point_contour(img)

            if screenCnt is not None:
                t = []
                height, width, _ = img.shape
                for v in self.vertices:
                    # Transform the point from 3D to 2D
                    p = v.project(width / 2, height / 2, 100, 2)
                    # Put the point in the list of transformed vertices
                    t.append(p)

                s = 3
                cube_point = [[int(t[self.faces[s][0]].x), int(t[self.faces[s][0]].y)],
                              [int(t[self.faces[s][1]].x), int(t[self.faces[s][1]].y)],
                              [int(t[self.faces[s][2]].x), int(t[self.faces[s][2]].y)],
                              [int(t[self.faces[s][3]].x), int(t[self.faces[s][3]].y)]]

                mat_dlt = dlt(2, [[0, 0], [width, 0], [0, height], [width, height]], screenCnt)

                for f in self.faces:
                    p1 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[0]].x), int(t[f[0]].y)))
                    p2 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[1]].x), int(t[f[1]].y)))
                    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 255, 255))

                    p1 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[1]].x), int(t[f[1]].y)))
                    p2 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[2]].x), int(t[f[2]].y)))
                    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (255, 255, 255))

                    p1 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[2]].x), int(t[f[2]].y)))
                    p2 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[3]].x), int(t[f[3]].y)))
                    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (255, 255, 255))

                    p1 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[3]].x), int(t[f[3]].y)))
                    p2 = dlt_reconstruction(2, 1, mat_dlt, (int(t[f[0]].x), int(t[f[0]].y)))
                    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (255, 255, 255))

            cv2.imshow("Main", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cam.stop()


if __name__ == "__main__":
    pass