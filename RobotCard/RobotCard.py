#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np

from RobotCard import *


class RobotCard(object):

    def __init__(self):

        self.cam = WebCam()
        self.texture_background = None

        self.rtri = 0.0
        self.rquad = 2.0
        self.speed = 0.1
        self.cube_pos = [0, 0]

    def __init_gl(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        self.cam.start()
        glEnable(GL_TEXTURE_2D)

        # self.texture_background = glGenTextures(1)

    def __draw_scene(self):
        """

        :return:
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        img = self.cam.get_current_fram()
        self.__handle_background(img.copy())
        self.__handle_markers(img.copy())
        glutSwapBuffers()

    def __handle_background(self, image):
        """

        :param image:
        :return:
        """
        # convert image to OpenGL texture format
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes('raw', 'BGRX', 0, -1)

        # create background texture
        # glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)

        # draw background
        # glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(4.0, 3.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-4.0, 3.0, 0.0)

        glEnd()
        glPopMatrix()

    def __handle_markers(self, image):
        """

        :param image:
        :return:
        """
        glTranslatef(self.cube_pos[0], self.cube_pos[1], -10)
        glScaled(0.1, 0.1, -0.1)
        glRotatef(self.rquad, self.speed, self.speed, self.speed)
        glBegin(GL_QUADS)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)

        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)

        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glEnd()

        self.rtri += 1
        self.rquad -= 2

        self.cube_pos[0] = (self.cube_pos[0] + 0.01) % 5
        self.cube_pos[1] = (self.cube_pos[1] + 0.01) % 5

    def __key_pressed(self, *args):
        """

        :param args:
        :return:
        """
        print(args)
        if args[0] == b"\x1b":
            print("stop")
            self.cam.stop()
            exit()

    def start(self):

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b'Robot card')
        glutDisplayFunc(self.__draw_scene)
        glutIdleFunc(self.__draw_scene)
        glutKeyboardFunc(self.__key_pressed)
        self.__init_gl()
        glutMainLoop()
        print("end")
        self.cam.stop()


if __name__ == "__main__":
    pass