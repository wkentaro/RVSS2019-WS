#!/bin/bash

set -e

echo_bold () {
  echo -e "\033[1m$*\033[0m"
}

echo_warning () {
  echo -e "\033[33m$*\033[0m"
}

conda_check_installed () {
  if [ ! $# -eq 1 ]; then
    echo "usage: $0 PACKAGE_NAME"
    return 1
  fi
  conda list | awk '{print $1}' | egrep "^$1$" &>/dev/null
}

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT=$HERE/..

cd $ROOT

source .anaconda3/bin/activate

# ---------------------------------------------------------------------------------------

echo_bold "==> Installing latest pip and setuptools"
pip install -U pip setuptools wheel

echo_bold "==> Installing with requirements-dev.txt"
pip install -r requirements-dev.txt

# ---------------------------------------------------------------------------------------

echo_bold "\nAdd below to ~/.ssh/config\n"
echo "$(cat $ROOT/on_laptop/ssh_config)"

echo_bold "\nAnd then, all is well! You can start using this!

  $ source .anaconda3/bin/activate
"
