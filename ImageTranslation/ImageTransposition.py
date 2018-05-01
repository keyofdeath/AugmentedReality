#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
from ImgOperator.Trasformations.VisionTool import *
from ImgOperator.Tool import *
import cv2


class ImageTransposition(Oporation):

    def __init__(self, corner_position, img_src):
        """
        H = Haut
        B = Bas
        D = Droit
        G = Gauche
                                                        0                       1
        :param corner_position: Sous la forme [ [HG X, HG Y, ou HG Z], [HD X, HD Y, ou HD Z],
                                                                ..Autre point..
                                                        -2                      -1
                                                [BG X, BG Y, ou BG Z], [BD X, BD Y, ou BD Z] ]
        :param img_src: Image a superposer sur l'image principale
        """
        super().__init__()
        self.corn_pos = corner_position
        self.out_height = max(abs(self.corn_pos[0][1] - self.corn_pos[-2][1]),
                              abs(self.corn_pos[1][1] - self.corn_pos[-1][1]))
        self.out_height = int(self.out_height)

        self.out_width = max(abs(self.corn_pos[0][0] - self.corn_pos[1][0]),
                             abs(self.corn_pos[-2][0] - self.corn_pos[-1][0]))
        self.out_width = int(self.out_width)

        self.out_position = [[0, 0], [self.out_width, 0], [0, self.out_height], [self.out_width, self.out_height]]
        self.mat_l = dlt(2, self.corn_pos, self.out_position)

        # on cree une liste de coordoner pour appliquer une fonction sur chaque element de cette liste
        self.pos_list = [[x, y] for x in range(self.out_width) for y in range(self.out_height)]
        self.img_src = cv2.resize(img_src, (self.out_width, self.out_height))
        # self.img_src = creat_empty_img(self.out_height, self.out_width)
        self.img_out = None

    def __pix_func(self, pos):
        """
        Fonction appler sur notre liste de position
        :param pos:
        :return:
        """
        # On trouve le pixel assosier dans l'image originale a la position de notre notre image de sortie
        img_pos = dlt_reconstruction(2, 1, self.mat_l, pos)
        # on mais le pixel de notre image src dans l'image principale
        self.img_out[int(img_pos[1])][int(img_pos[0])] = self.img_src[pos[1]][pos[0]]

    def apply(self, img):
        # image de fin
        self.img_out = img
        # on applique la foncion pix func sur chaque element de notre liste qui sont pour nous des positions dans
        # Limage de sortie
        list(map(lambda e: self.__pix_func(e), self.pos_list))
        return self.img_out


if __name__ == "__main__":
    pass
