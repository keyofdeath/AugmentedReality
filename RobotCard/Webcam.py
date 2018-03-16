#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

import cv2


class WebCam:

    def __init__(self):

        self.cam = cv2.VideoCapture(0)
        self.current_frame = self.cam.read()[1]
        self.end_app = False

    def start(self):
        Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while not self.end_app:
            self.current_frame = self.cam.read()[1]

    def get_current_fram(self):
        return self.current_frame

    def stop(self):
        self.end_app = True


if __name__ == "__main__":
    pass