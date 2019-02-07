#!/usr/bin/env python

import argparse
import pathlib
import pprint

import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
import sklearn.metrics

from steer_net.steerDS import SteerDataSet
from steer_net.steerNet import SteerNet


def test(model_file):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    ds = SteerDataSet('./dev_data/testing_data', '.jpg', transform)
    ds_dataloader = DataLoader(ds, batch_size=1, shuffle=True)

    model = SteerNet()
    model.load_state_dict(torch.load(model_file))

    Y_true = []
    Y_pred = []
    for iteration, S in enumerate(ds_dataloader):
        image = S['image']
        y_true = S['steering_class']
        y_pred = model(image)
        y_pred = np.argmax(y_pred.data.numpy()[0])
        Y_true.append(y_true)
        Y_pred.append(y_pred)

    Y_true = np.asarray(Y_true)
    Y_pred = np.asarray(Y_pred)

    return Y_true, Y_pred


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('log_dir_or_model_file')
    args = parser.parse_args()

    print('==> Arguments:')
    pprint.pprint(args.__dict__)

    log_dir_or_model_file = pathlib.Path(args.log_dir_or_model_file)

    if log_dir_or_model_file.is_file():
        model_file = args.log_dir_or_model_file
        y_true, y_pred = test(model_file)
        accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
        print(f'==> Testing: {model_file}, {accuracy}')
    else:
        model_files = list(log_dir_or_model_file.glob('model_*.pth'))
        accuracies = []
        for model_file in model_files:
            y_true, y_pred = test(model_file)
            accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
            print(f'==> Testing: {model_file}, {accuracy:.1%}')
            accuracies.append(accuracy)

        index = np.argmax(accuracies)
        model_file = model_files[index]
        y_true, y_pred = test(model_file)

    print(f'==> Result of: {model_file}')
    report = sklearn.metrics.classification_report(y_true, y_pred)
    print(report)
    accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
    print(f'==> Accuracy: {accuracy}')


if __name__ == '__main__':
    main()
