#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

import cv2
import numpy as np


class WebCam:

    def __init__(self, cam_activ=False, img_path=None, height=600, width=500):
        if cam_activ:
            self.cam = cv2.VideoCapture(1)
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
        return self.current_frame.copy()

    def stop(self):
        self.end_app = True


if __name__ == "__main__":
    pass