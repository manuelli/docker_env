FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ARG USER_NAME
ARG USER_PASSWORD
ARG USER_ID
ARG USER_GID


# https://askubuntu.com/questions/909277/avoiding-user-interaction-with-tzdata-when-installing-certbot-in-a-docker-contai
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt install sudo
RUN useradd -ms /bin/bash $USER_NAME
RUN usermod -aG sudo $USER_NAME
RUN yes $USER_PASSWORD | passwd $USER_NAME

# set uid and gid to match those outside the container
# problems when building on mac https://github.com/pyro-ppl/pyro/blob/dev/docker/Dockerfile
#RUN usermod -u $USER_ID $USER_NAME
#RUN groupmod -g $USER_GID $USER_NAME

WORKDIR /home/$USER_NAME
ENV USER_HOME_DIR=/home/$USER_NAME

# install python3
# copied from https://github.com/FNNDSC/ubuntu-python3/blob/master/Dockerfile
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && pip3 install --upgrade pip

# install pytorch
RUN pip3 install torch==1.2.0 torchvision==0.4.0 -f https://download.pytorch.org/whl/cu100/torch_stable.html

# install other dependencies
COPY docker/install_dependencies.sh /tmp/install_dependencies.sh
RUN /tmp/install_dependencies.sh

# key_dynam requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# change color of terminator inside docker
RUN mkdir -p .config/terminator
COPY docker/terminator_config .config/terminator/config


# change ownership of everything to our user
RUN cd ${USER_HOME_DIR} && echo $(pwd) && chown $USER_NAME:$USER_NAME -R .


ENTRYPOINT bash -c "source ~/code/pdc/docker/entrypoint.sh && /bin/bash"

