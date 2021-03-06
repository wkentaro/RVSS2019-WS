#!/bin/bash

verbose_eval () {
  echo "+ $*"
  eval $*
}

echo_bold () {
  echo -e "\033[1m$*\033[0m"
}

usage () {
  echo "usage: $0 MODEL_FILE"
}

set -e

if [ ! $# -eq 1 ]; then
  usage
  exit 1
fi

MODEL_FILE=$1

echo_bold "==> Uploading steerNet.py to penguinpi"
verbose_eval scp ./steer_net/steerNet.py penguinpi:/home/pi/RVSS2019-WS/on_robot/deploy/steerNet.py

echo_bold "==> Uploading model file to penguinpi"
# scp ./logs/20190205_175900/model_0010.pth penguinpi:/home/pi/RVSS2019-WS/on_robot/deploy/steerNet.pt
# scp ./logs/20190205_183103/model_0010.pth penguinpi:/home/pi/RVSS2019-WS/on_robot/deploy/steerNet.pt
verbose_eval scp $MODEL_FILE penguinpi:/home/pi/RVSS2019-WS/on_robot/deploy/steerNet.pt
