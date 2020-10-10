#!/bin/bash

set -euxo pipefail

# here you can install all the dependencies you want in your docker image
# basically anything you would usually do with `sudo apt-get install <package>`
apt-get update
apt install -y --no-install-recommends \
  python-pip \
  python-dev \
  terminator \
  tmux \
  vim \
  gedit \
  git \
  nvidia-settings
# openssh-client \
#  unzip \
#  htop \
#  libopenni-dev \
#  apt-utils \
#  usbutils \
#  dialog \
#  ffmpeg \
#  cmake-curses-gui \
#  libyaml-dev \
#  virtualenv \
#  wget \
#  python3-tk \
#  curl \
#  dbus-x11 \
#  libqt5gui5 # needed for vREP libqt5gui5
  # mesa-utils # this will give us glxgears

#apt install -y dbus-x11 # needed for terminator fonts


