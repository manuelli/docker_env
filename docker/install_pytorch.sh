#!/bin/bash

set -euxo pipefail

pip install \
  future \
  numpy==1.16.0 \
  pyyaml \
  requests \
  setuptools \
  six \
  typing
pip install --no-deps torch==1.2.0 torchvision==0.4.0 -f https://download.pytorch.org/whl/cu100/torch_stable.html
