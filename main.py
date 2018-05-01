#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BouncingCube import *
from ImageTranslation.ImageTranslation import ImageTranslation
import cv2


def disp_menu():

    print("1) Ball tracking game")
    print("2) Image translation")
    print("3) exit")


def choix():
    """
    Fonction qui demmande a l'utisateur d'entrer un numéro
    :return:
    """
    while True:
        c = input(">>>")
        # Traitement basique sur la chaine
        c = c.lower()
        c = c.strip()
        # pour retirer les character spéciaux
        c = ''.join(e for e in c if e.isalnum())
        try:
            c = int(c)
            return c
        except ValueError:
            print("Votre choix n'est pas valide")


def choix_str():
    """
    Fonction qui demmande a l'utisateur d'entrer une string
    :return:
    """

    c = input(">>>")
    return c.strip()


def ballTracking(cam_src):
    """

    :return:
    """
    print("***Ball tracking***")
    print("Pour quiter taper 'q'")
    robotCard = BouncingCube(cam=WebCam(cam_src, cam_activ=True))
    robotCard.start()


def imageTranslate(cam_src):
    """

    :param cam_src:
    :return:
    """
    print("***Translation d'image***")
    print("Entrer le chemin vers l'image:")
    chemin_img = choix_str()
    img = cv2.imread(chemin_img)
    while img is None:
        print("reco_img: Le chemin donnée n'est pas valide")
        chemin_img = choix_str()
        img = cv2.imread(chemin_img)

    print("Pour quiter taper 'q'")
    trans = ImageTranslation(chemin_img, cam_src)
    trans.start()


def quiter(cam_src):
    """

    :param cam_src:
    :return:
    """
    exit(1)


def menu(cam_src):
    """

    :param cam_src:
    :return:
    """

    action = {1: ballTracking, 2: imageTranslate, 3: quiter}
    while True:
        disp_menu()
        action[choix()](cam_src)


if __name__ == "__main__":
    menu(0)
