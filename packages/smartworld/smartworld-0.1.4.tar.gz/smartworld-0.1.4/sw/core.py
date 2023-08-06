# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   core.py
@Time    :   2022/10/26 17:17:15
@Author  :   Frank.Xu
"""
import os
import click
import shutil
import linecache
import subprocess
from .scripts.sync_repo import _sync
from .scripts.mapping import mapping

HERE = os.path.abspath(os.path.dirname(__file__))
OTA_FOLDER_PATH = "/home/ginger/grpc_ota_tmp"
GATEWAY_FILE_PATH = "/etc/network/interfaces"


@click.group()
@click.version_option(package_name='smartworld')
def sw():
    """ Tools Collection of SmartWorld, documentation link: https://df54vg7fe0.feishu.cn/docx/EmajdGEJ2oqAArxzyxlcFJcznSb """


@click.command()
@click.option("-p", "--package", help="package path", prompt="Please input the path of OTA package",type=click.Path(exists=True))
def ota(package):
    """ Usage: sw ota -p or --package """
    """ Simple program that enter the path of the package and '101' to complete the ota upgrade """
    # if not os.path.exists(package):
    #     raise FileNotFoundError

    if not os.path.isfile(package):
        raise NotADirectoryError("package should be a file")

    shutil.copy(package, os.path.join(OTA_FOLDER_PATH, "ginger_lite-ota.zip"))
    os.system("cd {} && md5sum ginger_lite-ota.zip > md5.txt".format(OTA_FOLDER_PATH))
    os.system("roslaunch test_client test_client.launch")


@click.command()
def switch_gateway():
    """ Usage: sw switch-gateway """
    try:
        _type, gateway = linecache.getline(GATEWAY_FILE_PATH, 8).split()
    except ValueError:
        raise click.FileError
    if not _type == "gateway":
        raise ValueError("The file has been modified, line 8 is no longer the gateway")

    if click.confirm('Current gateway is {}, do you want to continue?'.format(gateway)):
        subprocess.call("sudo python3 {}".format(os.path.join(HERE, "scripts/switch_gateway.py")), shell=True)

@click.command()
@click.option("-t","--to",help="save path",prompt="Please input the path")
def clone(to):
    """ Usage: sw clone -t or --to """
    _sync(save_path=to)
    

sw.add_command(ota)
sw.add_command(switch_gateway)
sw.add_command(mapping)
sw.add_command(clone)

