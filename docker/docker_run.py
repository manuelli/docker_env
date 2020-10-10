#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import socket
import getpass

MOUNT_VOLUMES = True

MOUNT_VOLUME_DATA = [] # [host_machine_dir, container_dest]


SPARTAN_DIR_HOST_MACHINE = None
hostname = socket.gethostname()


if socket.gethostname() == "paladin-44":
    MOUNT_VOLUME_DATA.append(["/media/hdd/data", "data"])
    MOUNT_VOLUME_DATA.append(["/home/manuelli/data", "data_ssd"])
    # MOUNT_VOLUME_DATA.append(["/home/manuelli/code/spartan-hardware", 'code/spartan'])
if socket.gethostname() == "iiwa-2":
    MOUNT_VOLUME_DATA.append(["/home/manuelli/data", "data_ssd"])
    MOUNT_VOLUME_DATA.append(["/home/manuelli/data", "data"])
    MOUNT_VOLUME_DATA.append(["/home/manuelli/code/spartan", 'code/spartan'])

# MOUNT_VOLUME_DATA.append(["/Users/manuelli/data", "data"])

if __name__=="__main__":
    user_name = getpass.getuser()
    default_image_name = user_name + '-pdc'
    default_container_name = user_name + '-pdc'
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type=str,
        help="(required) name of the image that this container is derived from", default=default_image_name)

    parser.add_argument("-c", "--container", type=str, default=default_container_name, help="(optional) name of the container")

    parser.add_argument("-d", "--dry_run", action='store_true', help="(optional) perform a dry_run, print the command that would have been executed but don't execute it.")

    parser.add_argument("-e", "--entrypoint", type=str, default="", help="(optional) thing to run in container")

    parser.add_argument("-p", "--passthrough", type=str, default="", help="(optional) extra string that will be tacked onto the docker run command, allows you to pass extra options. Make sure to put this in quotes and leave a space before the first character")

    parser.add_argument("-ngpu", "--no_gpu", action='store_true', default=False, help="(optional) passing this option launches a docker container without GPU enabled")

    parser.add_argument("-usb", action="store_true", default=False, help="(optional) enable usb access from inside the container")

    parser.add_argument("--no_display", action='store_false', dest='display', default=True, help="(optional) launch without a display")


    args = parser.parse_args()
    print("running docker container derived from image %s" %args.image)

    pdc_source_dir = os.path.dirname(os.getcwd())

    print("pdc_source_dir", pdc_source_dir)
    image_name = args.image

    print("image_name", image_name)
    home_directory = '/home/' + user_name
    dense_correspondence_source_dir = os.path.join(home_directory, 'code')



    cwd = os.getcwd()
    pdc_root = os.path.dirname(os.path.dirname(cwd))

    cmd = None
    if args.no_gpu:
        cmd = "docker run "
    else:
        cmd = "docker run --gpus all"


    if args.container:
        cmd += " --name %(container_name)s " % {'container_name': args.container}

    # enable graphics
    # copied from https://www.pugetsystems.com/labs/hpc/NVIDIA-Docker2-with-OpenGL-and-X-Display-Output-1527/
    if args.display:
        cmd += "-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY -e XAUTHORITY -e NVIDIA_DRIVER_CAPABILITIES=all"


    if MOUNT_VOLUMES:
        cmd += " -v %(pdc_source_dir)s:%(home_directory)s/code/pdc "  \
            % {'pdc_source_dir': pdc_source_dir, 'home_directory': home_directory}              # mount source
        cmd += " -v ~/.ssh:%(home_directory)s/.ssh " % {'home_directory': home_directory}   # mount ssh keys
        cmd += " -v /media:/media " #mount media
        cmd += " -v ~/.torch:%(home_directory)s/.torch " % {'home_directory': home_directory}  # mount torch folder
                                                            # where pytorch standard models (i.e. resnet34) are stored

    for host_dir, container_dest in MOUNT_VOLUME_DATA:
        cmd += " -v %s:%s" %(host_dir, os.path.join(home_directory, container_dest))




    cmd += " --user %s " % user_name                                                    # login as current user

    # expose UDP ports
    # cmd += " -p 8888:8888 "
    cmd += " --ipc=host "

    # share host machine network
    cmd += " --network=host "

    cmd += " " + args.passthrough + " "

    # allow usb access inside the container
    if args.usb:
        cmd += " --privileged -v /dev/bus/usb:/dev/bus/usb "

    cmd += " --rm " # remove the image when you exit


    if args.entrypoint and args.entrypoint != "":
        cmd += "--entrypoint=\"%(entrypoint)s\" " % {"entrypoint": args.entrypoint}
    else:
        cmd += "-it "
    cmd += args.image
    cmd_endxhost = "xhost -local:root"

    print("command = \n \n", cmd, "\n", cmd_endxhost)
    print("")

    # build the docker image
    if not args.dry_run:
        print("executing shell command")
        code = os.system(cmd)
        print("Executed with code ", code)
        os.system(cmd_endxhost)
        # Squash return code to 0/1, as
        # Docker's very large return codes
        # were tricking Jenkins' failure
        # detection
        exit(code != 0)
    else:
        print("dry run, not executing command")
        exit(0)
