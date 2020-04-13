#!/usr/bin/env python

import os

if __name__ == '__main__':
    # os.rename("wrist_guidance (1).png", "p1.png")
    for i in range(13):
        try:
            os.rename("wrist_guidance ("+str(i)+").png", "y"+str(i)+".png")
            print(i)
        except:
            print str(i)+"not found"
