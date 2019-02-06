#!/bin/bash

usage () {
  echo "usage: $0 [train|test]"
}

echo_bold () {
  echo -e "\033[1m$*\033[0m"
}

set -e

if [ $# -eq 0 ]; then
  usage
  exit 1
fi

echo_bold "==> Downloading data from PenguinPi"
if [ "$1" = "train" ]; then
  scp PenguinPi:/home/pi/RVSS2019-WS/on_robot/collect_data/data/* dev_data/training_data/
elif [ "$1" = "test" ]; then
  scp PenguinPi:/home/pi/RVSS2019-WS/on_robot/collect_data/data/* dev_data/testing_data/
else
  usage
  exit 1
fi

echo_bold "==> Removing downloaded data from PenguinPi"
ssh PenguinPi rm -f /home/pi/RVSS2019-WS/on_robot/collect_data/data/*
