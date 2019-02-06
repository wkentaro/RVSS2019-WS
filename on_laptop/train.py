#!/usr/bin/env python

import datetime
import os
import os.path as osp

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms

from steer_net.steerDS import SteerDataSet
from steer_net.steerNet import SteerNet


def main():
    now = datetime.datetime.now()
    out_dir = osp.join('logs', now.strftime('%Y%m%d_%H%M%S'))
    os.makedirs(out_dir)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    ds = SteerDataSet("dev_data/training_data",".jpg",transform)

    print("The dataset contains %d images " % len(ds))

    ds_dataloader = DataLoader(ds,batch_size=1,shuffle=True)

    model = SteerNet()

    optimizer = torch.optim.Adam(model.parameters())

    losses = []

    num_epochs = 20
    for epoch in range(num_epochs):
        for iteration, S in enumerate(ds_dataloader):
            image = S['image']
            y_true = S['steering_class']

            # print(image.shape, y_true.shape)
            # print(type(image), type(y_true))

            y_pred = model(image)

            loss = F.cross_entropy(y_pred, y_true)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print('Epoch: {:04d}, Iteration: {:04d}, Loss: {:.4f}'.format(epoch, iteration, loss.item()))
            losses.append(loss.item())

        model_file = osp.join(out_dir, 'model_{:04d}.pth'.format(epoch))
        torch.save(model.state_dict(), model_file)

        with open(osp.join(out_dir, 'loss.csv'), 'w') as f:
            f.write('loss\n')
            for loss in losses:
                f.write('{}\n'.format(loss))


if __name__ == '__main__':
    main()
