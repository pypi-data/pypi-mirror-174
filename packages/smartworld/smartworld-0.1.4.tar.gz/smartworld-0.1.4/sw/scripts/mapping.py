# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mapping
   Description :
   Author :       Frank.Xu
   date：          2022/6/28
-------------------------------------------------
   Change Activity:
                   2022/6/28:
-------------------------------------------------
"""
__author__ = 'Frank.Xu'

import subprocess
import time
import os
# from .resource_monitor import ResourceMonitor
import click
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)

stop = False


def kill(p):
    """
    kill rosnode and roslaunch
    """
    subprocess.Popen("rosnode kill /hd_map_mapping", shell=True)
    p.kill()


def playing(bag, mission_id, p_launch):
    # ResourceMonitor("hd_map_node", 10, bag, mission_id)
    playing_cmd = "rosbag play --clock {} > /dev/null 2>&1".format(bag)
    playing_process = subprocess.Popen(playing_cmd, shell=True)

    while True:
        if playing_process.poll() is None:
            continue
        else:
            kill(p_launch)
            break


def _mapping(bag, source_path, output_folder, use_vision, use_lidar2d, mission_id):
    """
        <arg name="use_lio" default="false"/>
        <arg name="map_id" default="test" />
        <arg name="output_folder" default="/tmp" />
        <arg name="is_simulation" default="false" />
        <arg name="use_vision" default="true"/>
        <arg name="use_lidar2d" default="false"/>
        <arg name="camera_type" default="0" />      <!-- 0:auto  1:d435i  2:kkd2213 -->
    """
    try:
        output_folder = os.path.join(output_folder, os.path.basename(bag))
        mapping_cmd = "source {}/devel/setup.bash && exec roslaunch hd_map_node hd_map_mapping.launch is_simulation:=true output_folder:={} use_vision:={} use_lidar2d:={}".format(source_path, output_folder,
                                                                                                                                                                            use_vision,
                                                                                                                                                                            use_lidar2d)
        logging.info(mapping_cmd)
        p_launch = subprocess.Popen(mapping_cmd, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid, executable="/bin/bash")
        time.sleep(5)
        playing(bag, mission_id, p_launch)
    except KeyboardInterrupt:
        global stop
        stop = True
        kill(p_launch)


@click.command()
@click.option("--source_path", "-s", default="./", help="Enter the same level path as devel, such as ~/smartword/, the default is the current path",required=True)
@click.option("--input_path", "-i", help="The path of data",required=True)
@click.option("--output_path", "-o", default="/tmp", help="The path of output ",required=True)
@click.option("--use_vision", default="true", type=click.Choice(['true','false']),help="use vision,the default is true",required=True)
@click.option("--use_lidar2d", default="true", type=click.Choice(['true','false']),help="use lidar2d,the default is true",required=True)
@click.option("--mission_id", default=str(uuid.uuid1()),required=False)
def mapping(source_path, input_path, output_path, use_vision, use_lidar2d, mission_id):
    """ Usage: sw mapping -s ~/smartword/ -i ~/input -o ~/output """
    for root, dirs, files in os.walk(input_path):
        for _file in files:
            if stop:
                break
            if _file.endswith(".bag"):
                logging.info("start mapping :{}".format(os.path.join(root, _file)))
                _mapping(os.path.join(root, _file), source_path, output_path, use_vision, use_lidar2d, mission_id)
                time.sleep(10)
    logging.info("mapping done")


if __name__ == '__main__':
    mapping()
