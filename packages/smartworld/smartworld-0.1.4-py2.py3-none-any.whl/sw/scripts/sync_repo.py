#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @File    : sync_repo.py
# @Time    : 2022/8/4
# @Author  : Frank
# @Description： sync

import os
import sys

from git.repo import Repo  # pip install gitpython
import xml.etree.ElementTree as et
import tempfile
import shutil

root_url = "http://10.12.32.39:10023/smartworld"


class _Repo(object):
    def __init__(self, repo, branch="master"):
        self.branch = branch
        self.name = repo.attrib["name"]
        self.path = "" if repo.attrib["path"] == './' else repo.attrib["path"]

    @property
    def url(self):
        return "{}/{}.git".format(root_url, self.name)

    def clone(self, to):
        print("clone from {} to {}".format(self.url, os.path.join(to, self.path)))
        Repo.clone_from(self.url, to_path=os.path.join(to, self.path), branch=self.branch)


def _sync(save_path):
    temp_path = tempfile.mkdtemp()
    Repo.clone_from(url="{}/manifest.git".format(root_url), to_path=temp_path, branch="master")
    repos = et.parse(os.path.join(temp_path, "default.xml")).getroot()  # sync manifest to temp folder

    if os.path.exists(save_path):
        shutil.rmtree(save_path)

    for project in repos:
        if project.tag == "project":
            _Repo(project).clone(to=save_path)
            if project.attrib["name"] == "manifest":  # create symlink for catkin_build.sh
                os.symlink(os.path.join(save_path, project.attrib["path"], "catkin_build.sh"), os.path.join(save_path, "catkin_build.sh"))


if __name__ == '__main__':
    _sync(save_path=sys.argv[1] if len(sys.argv) > 1 else "/data/user/ginger/tmp/smartworld")
