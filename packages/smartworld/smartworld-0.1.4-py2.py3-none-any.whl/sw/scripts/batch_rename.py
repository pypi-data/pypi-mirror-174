#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    for root, dirs, files in os.walk("."):
        # for dir in dirs:
        #     print(os.path.join(root, dir))
        for _file in files:
            if _file == 'scan_info.json':
                # print(os.path.join(root, _file))
                dirname = os.path.dirname(os.path.join(root, _file))
                new_name = os.path.basename(dirname) + "_" + _file
                # print(new_name)
                # # os.rename(_file,os.path.dirname(os.path.join(root,_file)))
                # print(os.path.join(dirname, new_name))
                os.rename(os.path.join(root, _file), new_name)
