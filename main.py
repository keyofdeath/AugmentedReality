#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BouncingCube import *

if __name__ == "__main__":
    robotCard = BouncingCube(cam=WebCam(cam_activ=False))
    robotCard.start()
