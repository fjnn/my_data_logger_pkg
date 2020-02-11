#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The files should be layouted as following:
    - All generated CSV files should be placed somewhere within the 'Output' folder
    - Every set of CSV files that belong to one Tester should be placed in a separate subfolder
    for example, if a user Ahmet ran the simulation 10 times, then 10 CSV files were generated,
    we place all of them in a folder called 'Ahmet' or some random number, it doesn't really matter.
    - Basically every subfolder represents one set of training runs. One person yani
    - The generated CSV files should be named with their timestamped
    so that there filenames are can be sorted in increasing order.
#todo: deal with different simulation scenarios (with vs without axis alignment)
"""

import os
from datetime import datetime


OUTPUT_FOLDER = "../Output"  # take it as a rosparam
OUTPUT_FILENAME_PREFIX = "data"

ID_MARK = 'mark'
ID_PITCH = 'human_pitch'
ID_ROLL = 'human_roll'
ID_YAW = 'human_yaw'
ID_TIME = 'elapsed_time'

DATA_LABELS = (ID_MARK, ID_PITCH, ID_ROLL, ID_YAW, ID_TIME)
DATA_INDICES = {
        ID_MARK: 0,  # now using for aiding but can be used as division between motions
        ID_PITCH: 1,
        ID_ROLL: 2,
        ID_YAW: 3,
        ID_TIME: 4
        }


def get_new_filename():
    postfix = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".csv"
    filename = OUTPUT_FILENAME_PREFIX + "_" + postfix
    # if folder doesn't exist, create it
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    filename = os.path.join(OUTPUT_FOLDER, filename)
    return filename
