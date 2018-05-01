#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BouncingCube.Webcam import WebCam
from ImgOperator import *
from ImageTranslation.ImageTransposition import ImageTransposition
import cv2
import traceback


class ImageTranslation:

    def __init__(self, path_image_dest, cam_src, width=1024, height=768):
        """

        :param image_dest:
        """
        self.cam_src = cam_src
        self.image_dest = cv2.imread(path_image_dest)
        if self.image_dest is None:
            raise ValueError("Le path de l'image donnée n'est pas valide !")

    def start(self):
        cap = cv2.VideoCapture(self.cam_src)
        while True:
            # Capture frame-by-frame
            try:
                ret, frame = cap.read()
                coint = get_4_point_contour(frame)
                cv2.imshow("Main", frame)
                if coint is not None:
                    opp = ImgOprerator(frame)
                    opp.add_oporation(ImageTransposition(coint, self.image_dest))
                    cv2.imshow("wrap", opp.img)
            except:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    pass