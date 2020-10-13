# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:02:55 2020

@author: 江翊宏
"""
import time
from time import sleep
import numpy as np
import pylab as plt
from PIL import ImageGrab
from PIL import Image
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

# set the range
x_1 = 0
y_1 = 0
x_2 = 960  #1920
y_2 = 1080 #1080

# parameters
std_color = [42, 34, 53]

U = 0
while U<200:
    U += 1
    # read the screen
    img_1 = ImageGrab.grab(bbox=(x_1, y_1, x_2, y_2))
    img_2 = np.asarray(img_1)
    
    init_x = 500
    init_y = 270
    
    # find the initial point
    d = 0
    while np.all(img_2[init_x+d, init_y+d, ] == std_color):
        d += 1
        if d > 500:
            fail = 1
            break

    init_x += d+2
    init_y += d+2
    
    init_color = img_2[init_x, init_y, ]

    # find the center
    d_x = 0
    while np.all(img_2[init_x+d_x, init_y, ] == init_color):
        d_x += 1
    center_x = init_x+(d_x//2)

    d_y = 0
    while np.all(img_2[init_x, init_y+d_y, ] == init_color):
        d_y += 1
    center_y = init_y+(d_y//2)

    # find the radius
    r = 0
    while np.all(img_2[center_x+r, center_y, ] == init_color):
        r += 1

    # find the number of circle(N*N)
    if d>90:
        N = 2
    else:        
        N = round(195/r)
    
    x_axis = 0
    y_axis = 0
    err = 0
    sample = 0
    end = 0
    
    for i in range(0,N):
        for j in range(0,N):
            if np.any(img_2[center_x + i*(2*r), center_y + j*(2*r),] != init_color):
                x_axis = i
                y_axis = j
                err += 1
            if sample>2:
                if err>1:
                    x_axis = 0
                    y_axis = 0
                    end = 1
                    break
                elif err == 1:
                    end = 1
                    break
            sample += 1
        if end:
            break
    
    # click & sleep
    ans_x = center_x + x_axis*(2*r)
    ans_y = center_y + y_axis*(2*r)
    click(ans_y,ans_x)
    sleep(0.3)
    
    # end show
    if np.all(img_2[275, 475, ] != [255, 232, 69]):
        plt.imshow(img_1)
        break
    