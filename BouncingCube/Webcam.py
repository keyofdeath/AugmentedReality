#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

import cv2
import numpy as np
import imutils


class WebCam:

    def __init__(self, cam_src, cam_activ=False, img_path=None, width=1024, height=768):
        self.height = height
        self.width = width
        if cam_activ:
            self.cam = cv2.VideoCapture(cam_src)
            self.current_frame = self.cam.read()[1]
            self.end_app = False
        elif img_path is None:
            self.cam = None
            self.current_frame = np.zeros((int(height) + 1, int(width) + 1, 3), np.uint8)
        else:
            self.cam = None
            self.current_frame = cv2.imread(img_path)

    def start(self):
        if self.cam is not None:
            Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while not self.end_app:
            self.current_frame = self.cam.read()[1]

    def get_current_fram(self):
        return imutils.resize(self.current_frame, width=self.width, height=self.height)

    def stop(self):
        self.end_app = True


if __name__ == "__main__":
    pass