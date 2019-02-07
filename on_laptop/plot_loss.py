#!/usr/bin/env python

import argparse
import os.path as osp

import matplotlib.pyplot as plt
import numpy as np
import pandas


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument('log_dir')
args = parser.parse_args()


df = pandas.read_csv(osp.join(args.log_dir, 'loss.csv'))

N = len(df)
step = 20

df = df.rolling(window=step, center=True).mean()

iterations = np.arange(step // 2, N, step)
loss = df.ix[iterations]['loss']

plt.plot(iterations, loss)
plt.show()
