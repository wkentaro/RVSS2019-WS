#!/usr/bin/env python3
import os.path as osp
import datetime
import time
import click
import math
import sys
sys.path.append("..")
import cv2
import numpy as np
import penguinPi as ppi
import pygame
import torch
from torch import nn


#~~~~~~~~~~~~ SET UP Game ~~~~~~~~~~~~~~
pygame.init()
pygame.display.set_mode((100,100))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# stop the robot 
ppi.set_velocity(0,0)

now = datetime.datetime.now()
prefix = now.strftime('%Y%m%d_%H%M%S')

try:
    angle = 0
    lead = 0
    while True:

        # get an image from the the robot
        image = ppi.get_image()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle = 0
                    print("straight")
                if event.key == pygame.K_DOWN:
                    angle = 0
                if event.key == pygame.K_RIGHT:
                    print("right")
                    angle += 0.1
                if event.key == pygame.K_LEFT:
                    print("left")
                    angle -= 0.1
                if event.key == pygame.K_SPACE:
                    print("stop")                    
                    ppi.set_velocity(0,0)
                    raise KeyboardInterrupt
        
        angle = np.clip(angle, -0.5, 0.5)
        Kd = 20
        Ka = 20
        left  = int(Kd + Ka*angle)
        right = int(Kd - Ka*angle)
        
        ppi.set_velocity(left,right) 

        base = osp.join('data/{}_{:06d}'.format(prefix, lead))
        cv2.imwrite(base + '.jpg', image)
        with open(base + '.txt', 'w') as f:
            f.write('{}'.format(angle))
        lead += 1
        
        
except KeyboardInterrupt:    
    ppi.set_velocity(0,0)

