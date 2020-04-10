#!/usr/bin/env python

import os

if __name__ == '__main__':
    for i in range(12):
        os.rename("wrist_guidance" + " (" + str(i) + ").png", "p" + str(i) + ".png")
        print(i)
