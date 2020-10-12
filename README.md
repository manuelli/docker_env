# Overview

This repo shows an example of building a minimal docker image for development with graphics support (i.e. the ability to visualize windows from inside the docker). Arbitrary dependencies can be added to the image by adding to the [`install_dependencies.sh`](docker/install_dependencies.sh) file.

## Build the Docker Image

To build the docker image navigate to the [`docker`](docker/) subdirectory and run the `docker_build.py` script
```
cd docker && python docker_build.py
```


The docker build is managed by the [`docker_build.py`](docker/docker_build.py) python script. Essentially it just sets up the appropriate arguments and calls the docker build on [`env.dockerfile`](docker/env.dockerfile).


If the build was successful then running `docker images` should show the newly built image which is named`<username>-nvidia-docker`.

## Run a docker container

To run the docker container based on the docker image that was built in the previuos step navigate to the `docker` subfolder and run the `docker_run.py` script.

```
cd docker && python docker_run.py
```

This should run the docker image you created in the previous step. Note that you should have full graphics capabilities inside this docker. Try running 
```
terminator &
```
which should launch a new `terminator` window with a blue background. You can also try running

```
glxgears
``` 

