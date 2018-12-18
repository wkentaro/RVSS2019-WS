#!/usr/bin/env python3
import math
import cv2
import numpy as np
import penguinPi as ppi
import torch
from torch import nn
from steerNet import SteerNet
from torchvision import transforms

def load_net(wegihts_filename):
    model = SteerNet()
    model.load_state_dict(torch.load(wegihts_filename))
    model.eval()        
    return model

def preprocess_img(img,transform):
    img = transform(img)
    # add dimension for batch
    img = img.unsqueeze(0)
    return img


transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
net = load_net("steerNet.pt")


#~~~~~~~~~~~~ SET UP ROBOT ~~~~~~~~~~~~~~
ppi.set_velocity(0,0)

try:
    angle = 0
    Kd = 20
    Ka = 20
    while True:
        # read image from camera 
        image = ppi.get_image()
        # resize to fit network 
        image = image[110:, :]
        image = cv2.resize(image, (84,84))
        # preprocess
        input_img = preprocess_img(image,transform)
        # get steering prediction 
        steer = net(input_img).data.numpy()              
        
        steer_class = np.argmax(steer)
        angle = steer_class / 10. - 0.5

        if steer_class in [5]:
            Kd = min(28, Kd + 4)
        elif steer_class in [4, 6]:
            Kd = min(24, Kd + 2)
        else:
            Kd = 20

        print(steer_class, angle, Kd, Ka)

        left  = int(round(Kd + Ka * angle))
        right = int(round(Kd - Ka * angle))
        
        ppi.set_velocity(left, right)
        
except KeyboardInterrupt:
    ppi.set_velocity(0,0)
