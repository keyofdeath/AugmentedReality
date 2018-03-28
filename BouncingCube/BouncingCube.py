#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pymunk
from BouncingCube.Webcam import WebCam
from random import randint


class BouncingCube(object):

    MASS = 1
    RADIUS = 14
    METAL_FRICTION = 0.5
    COLLTYPE_BALL = 2

    def __init__(self, width=1024, height=768, cam=None):

        self.cam = WebCam(True, None, height, width) if cam is None else cam
        cv2.namedWindow("Main")
        cv2.moveWindow("Main", 0, 0)
        self.width = width
        self.height = height

        self.space = pymunk.Space()
        self.space.gravity = 0.0, -900.0

    def flipy(self, y):
        """
        Applique un changement sur l'axe des y
        :param y: position y de pymunk
        :return:
        """
        return -y + self.height

    def add_ball(self):

        mass = BouncingCube.MASS
        radius = BouncingCube.RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        body = pymunk.Body(mass, inertia)
        x = randint(100, self.width)
        body.position = x, self.flipy(0)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = BouncingCube.METAL_FRICTION
        shape.collision_type = BouncingCube.COLLTYPE_BALL
        self.space.add(body, shape)
        return shape

    def start(self):

        self.cam.start()

        balls = []

        while True:

            img = self.cam.get_current_fram()
            ball_shape = self.add_ball()
            balls.append(ball_shape)

            balls_to_remove = []
            for ball in balls:
                if self.flipy(ball.body.position.y) > self.height + 20:
                    balls_to_remove.append(ball)

            for ball in balls_to_remove:
                self.space.remove(ball, ball.body)
                balls.remove(ball)

            self.space.step(1 / 50.0)

            for ball in balls:
                r = ball.radius
                v = ball.body.position
                p = int(v.x), int(self.flipy(v.y))
                cv2.circle(img, p, int(r), (0, 255, 255), 2)

            cv2.imshow("Main", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cam.stop()


if __name__ == "__main__":
    pass
