#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pymunk
from time import time
from pymunk import Vec2d
from random import randint
from collections import deque

from BouncingCube.Traking import Traking
from BouncingCube.Webcam import WebCam


class BouncingCube(object):

    MASS = 1
    RADIUS = 14
    METAL_FRICTION = 0.5
    COLLTYPE_BALL = 2

    def __init__(self, width=1024, height=768, cam=None, buffer=128):
        """

        :param width: Largeur de la fenêtre d'affichage
        :param height: Hauteur de la fenêtre d'affichage
        :param cam: Caméra a activer
        :param buffer: Taille du buffer (plus le buffer est grand plus les ligne resteron sur l'écrant)
        """

        self.cam = WebCam(True, None, height, width) if cam is None else cam
        self.traking = Traking(self.cam)
        cv2.namedWindow("Main")
        cv2.moveWindow("Main", 0, 0)
        self.width = width
        self.height = height

        self.buffer = buffer
        self.point_que = deque(maxlen=buffer)
        self.static_line = list()
        self.space = pymunk.Space()
        self.space.gravity = 0.0, -900.0

    def to_pymunk_y(self, y):
        """
        Convertir un position y de notre écrant en position y pymuk
        :param y:
        :return:
        """
        return self.height - y

    def add_ball(self):
        """
        Rajoute une boulle dans notre ecrant
        :return: le shape de la boulle cree
        """

        mass = BouncingCube.MASS
        radius = BouncingCube.RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        body = pymunk.Body(mass, inertia)
        body.position = randint((self.width // 2) - 10, (self.width // 2) + 10), self.to_pymunk_y(0)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = BouncingCube.METAL_FRICTION
        shape.collision_type = BouncingCube.COLLTYPE_BALL
        self.space.add(body, shape)
        return shape

    def draw_point(self, img, color):
        """
        Dessine la liste des point dans l'image donnée
        :param img:
        :param color:
        :return:
        """

        # loop over the set of tracked points
        for i in range(1, len(self.point_que)):
            # if either of the tracked points are None, ignore
            # them
            if self.point_que[i - 1] is None or self.point_que[i] is None:
                continue
            cv2.line(img, self.point_que[i - 1], self.point_que[i], color, 10)
        return img

    def start(self):
        """
        Fonction pour commencer le jeux
        :return:
        """

        self.cam.start()

        balls = []
        point_num = 0
        color_trai = (0, 0, 255)

        while True:

            self.space.step(1 / 50.0)
            ball_shape = self.add_ball()
            balls.append(ball_shape)

            # on track la balle
            center, img_out = self.traking.tick()
            # Si on a decter la balle
            if center is not None:
                point_num += 1
                # on ajoute sa position dans la liste
                self.point_que.appendleft(center)

            # on rajout un vector que si on a 2 point
            if point_num == 2:

                # on cree nos 2 point en pymunk
                line_point_1 = Vec2d(self.point_que[1][0],
                                     self.to_pymunk_y(self.point_que[1][1]))
                line_point_2 = Vec2d(self.point_que[0][0],
                                     self.to_pymunk_y(self.point_que[0][1]))
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                # on cree un segment
                shape = pymunk.Segment(body, line_point_1, line_point_2, 0.0)
                shape.fraction = 0.99
                self.space.add(shape)
                self.static_line.append(shape)
                point_num = 0
                # on regarde si le buffer n'est pas plein
                if len(self.point_que) >= self.buffer:
                    try:
                        # on enlève le premier vector
                        shape = self.static_line.pop(0)
                        self.space.remove(shape, shape.body)
                        self.static_line.remove(shape)
                    except KeyError:
                        pass
            # on dessine les boulles
            for ball in balls:
                # On supprime les boulles en dehord de l'écrant
                if self.to_pymunk_y(ball.body.position.y) > self.height + 20:
                    self.space.remove(ball, ball.body)
                    balls.remove(ball)
                else:
                    r = ball.radius
                    v = ball.body.position
                    p = int(v.x), int(self.to_pymunk_y(v.y))
                    cv2.circle(img_out, p, int(r), (0, 255, 255), 2)

            # on affiche l'image
            cv2.imshow("Main", self.draw_point(img_out, color_trai))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        self.cam.stop()


if __name__ == "__main__":
    pass
