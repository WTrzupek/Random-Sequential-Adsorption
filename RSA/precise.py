#from shapely.geometry import MultiLineString
import matplotlib.pyplot as plt
import matplotlib.patches as pth
import numpy as np
import math
import time
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from line_profiler import LineProfiler

from termcolor import colored

np.random.seed(56478965)
V = 1.0

#@profile
def box(size): 
    """ Returns coordinates for pixels in Cartesian system 
    
    Keyword arguments:
    size -- radius of single circle
    
    """
    
    p_list = []
    
    for i in np.arange(0,V-size,size):
        for j in np.arange(0,V-size,size):
            p_list.append([i,j,size])
      
    p_coords = set(tuple(i) for i in p_list)

    return p_coords

#@profile              
def search_s1(saturation, size, startTime):
    
    """ First stage for sequential adsorption. Returns list of circles.
    
    Keyword arguments:
    saturation -- maximal saturation
    size -- radius of single circle
    
    """
    
    global nAttemptsList
    global ntimeList 
    global satList
    
    nAttemptsList = []
    ntimeList = []
    satList = []
    
    nAttempts = 0
    N = 0                         #number of tries
    added = 0                     #added within 500 tries
    com_sat = 0
    D = size*2
    
    circles = [plt.Circle((np.random.rand(),np.random.rand()), size)]    
    
    while (N <= 500 and com_sat <= saturation):
        
        N+=1
        nAttempts += 1
        
        newX = np.random.rand()
        newY = np.random.rand()
        
        new = plt.Circle((newX, newY), size)

        for circle in circles:
            
            circleX = circle.get_center()[0]
            circleY = circle.get_center()[1]
            
            if (math.sqrt((newX - circleX)**2 + (newY - circleY)**2) <= D or 
                math.sqrt((newX - circleX-V)**2 + (newY - circleY)**2) <= D or 
                math.sqrt((newX - circleX+V)**2 + (newY - circleY)**2) <= D or
                math.sqrt((newX - circleX)**2 + (newY - circleY-V)**2) <= D or
                math.sqrt((newX - circleX)**2 + (newY - circleY+V)**2) <= D or
                math.sqrt((newX - circleX+V)**2 + (newY - circleY+V)**2) <= D or
                math.sqrt((newX - circleX-V)**2 + (newY - circleY+V)**2) <= D or
                math.sqrt((newX - circleX+V)**2 + (newY - circleY-V)**2) <= D or
                math.sqrt((newX - circleX-V)**2 + (newY - circleY-V)**2) <= D):
                
                collision = 1
                
                break
            else:
                collision = 0
        
        if (collision == 0):
            
            circles.append(new)
            added+=1
                        
            com_sat = math.pi * size**2 * len(circles) * 100

            nAttemptsList.append(nAttempts)
            ntimeList.append(time.time() - startTime) 
            satList.append(com_sat)
            
            nAttempts = 0
            
        if added >= 3:
            N = 0
            added = 0   
            
    return circles, com_sat, nAttemptsList, ntimeList, satList

#@profile 
def search_s2(size, pixels, circles, com_sat, saturation, nAttemptsList, ntimeList, satList, startTime):
    """ Second stage for sequential adsorption only in free pixels.
        Returns list of circles.
    
    Keyword arguments:
    pixels -- list of free pixels
    circles -- list of already added circles
    com_sat -- actual saturation
    size -- radius of single circle
    saturation -- max saturation
    ntimeList -- list of end-times
    satList -- list of end saturations
    startTime -- start time of algorithm
    
    """
    if len(pixels) == 0:
        return circles, com_sat, ntimeList, satList
    
    D = size*2
    added = 0  
    Nn = 0
    nAttempts = 0
    
    
    while(Nn <= 500 and com_sat < saturation):
        
        pixel = random.choice(list(pixels))
        p_size = pixel[2]
        
        Nn += 1
        nAttempts += 1
        
        newX = random.uniform(pixel[0], pixel[0] + p_size)
        newY = random.uniform(pixel[1], pixel[1] + p_size)

        for circle in circles:
            
            circleX = circle.get_center()[0]
            circleY = circle.get_center()[1]
            
            if (math.sqrt((newX - circleX)**2 + (newY - circleY)**2) < D or 
                math.sqrt((newX - circleX-V)**2 + (newY - circleY)**2) < D or 
                math.sqrt((newX - circleX+V)**2 + (newY - circleY)**2) < D or
                math.sqrt((newX - circleX)**2 + (newY - circleY-V)**2) < D or
                math.sqrt((newX - circleX)**2 + (newY - circleY+V)**2) < D or
                math.sqrt((newX - circleX+V)**2 + (newY - circleY+V)**2) < D or
                math.sqrt((newX - circleX-V)**2 + (newY - circleY+V)**2) < D or
                math.sqrt((newX - circleX+V)**2 + (newY - circleY-V)**2) < D or
                math.sqrt((newX - circleX-V)**2 + (newY - circleY-V)**2) < D):
                        
                collision = 1
                break
            
            else:
                collision = 0
    
        
        if (collision == 0):
            
            new = plt.Circle((newX, newY), size)
            circles.append(new)
            
            added += 1

            com_sat = math.pi * size**2 * len(circles) * 100
            nAttemptsList.append(nAttempts)
            ntimeList.append(time.time() - startTime) 
            satList.append(com_sat)

            nAttempts = 0
            
        if added >= 3:
            Nn = 0
            added = 0 
       
    return circles, com_sat, ntimeList, satList
   
def sub(pixels, size):
    
    """ Dividing each free pixel into four smaller.
        Return list of new pixels
        
    Keyword arguments:
    pixels -- list of old pixels
    size -- radius of single circle
    
    """
    
    if len(pixels) == 0:
        return pixels
        
    pixel = random.choice(list(pixels))
    p_size = pixel[2]
    
    sub_list = []
    
    for pixel in pixels:
        
        pixelX = pixel[0]
        pixelY = pixel[1]
                       
        sub_list.append([pixelX, pixelY, p_size/2])
        sub_list.append([pixelX + p_size/2, pixelY, p_size/2])
        sub_list.append([pixelX, pixelY + p_size/2, p_size/2])
        sub_list.append([pixelX + p_size/2, pixelY + p_size/2, p_size/2])
        
    sub_pixels = set(tuple(i) for i in sub_list)
    
    return sub_pixels

def boundary_cond(circles, size):    
    
    """ Adding boundary conditions for given set of circles.
        Returns list of circles with boundary conditions.
    
    Keyword arguments:
    circles -- list of circles
    size -- radius of single circle
    
    """
    
    boundaryCircles = []
    D = size*2
    
    for circle in circles:
        
        circleX = circle.get_center()[0]
        circleY = circle.get_center()[1]
        
        if circleX < D:
            boundaryCircles.append(plt.Circle((circleX + V, circleY), size))
            
        elif circleX + D > V:
            boundaryCircles.append(plt.Circle((circleX - V, circleY), size))
            
        elif circleY < D:
            boundaryCircles.append(plt.Circle((circleX,circleY + V), size))
            
        elif circleY + D > V:
            boundaryCircles.append(plt.Circle((circleX,circleY - V), size))
        
        #Left bottom
        if circleX < D and circleY < D:
            boundaryCircles.append(plt.Circle((circleX + V, circleY + V), size))
            boundaryCircles.append(plt.Circle((circleX + V, circleY), size))
            boundaryCircles.append(plt.Circle((circleX, circleY + V), size))
            
        #Left upper
        if circleX < D and circleY + D > V:
            boundaryCircles.append(plt.Circle((circleX + V, circleY - V), size))
            boundaryCircles.append(plt.Circle((circleX + V, circleY), size))
            boundaryCircles.append(plt.Circle((circleX, circleY - V), size))
        
        #Right bottom
        if circleX + D > V and circleY < D:
            boundaryCircles.append(plt.Circle((circleX - V,circleY + V), size))
            boundaryCircles.append(plt.Circle((circleX - V, circleY), size))
            boundaryCircles.append(plt.Circle((circleX, circleY + V), size))
        
        #Right upper
        if circleX + D > V and circleY + D > V:
            boundaryCircles.append(plt.Circle((circleX - V,circleY - V), size))
            boundaryCircles.append(plt.Circle((circleX - V, circleY), size))
            boundaryCircles.append(plt.Circle((circleX, circleY - V), size))

    return boundaryCircles
     
def access_list(pixels, circles, size):
    
    """ Returns list of free pixels
    
    Keyword arguments:
    pixels -- list of pixels
    circles -- list of circles
    size -- size of single circle
    
    """
    to_remove = set()
    Rpixel = random.choice(list(pixels))
    p_size = Rpixel[2]
    
    temp = boundary_cond(circles, size)
    circles = circles + temp
    
    D = size*2
    
    for circle in circles:
        
        circleX = circle.get_center()[0]
        circleY = circle.get_center()[1]
        
        for pixel in pixels:
            
            pixelX = pixel[0]
            pixelY = pixel[1]
            
            w1 = math.sqrt((circleX - pixelX)**2 + (circleY - pixelY)**2)
            w2 = math.sqrt((circleX - (pixelX + p_size))**2 + (circleY - pixelY)**2)
            w3 = math.sqrt((circleX - pixelX)**2 + (circleY - (pixelY + p_size))**2)
            w4 = math.sqrt((circleX - (pixelX + p_size))**2 + (circleY - (pixelY + p_size))**2)
              
            if w1 < D and w2 < D and w3 < D and w4 < D:
                to_remove.add(pixel)

    pixels = pixels - to_remove
    
    return pixels
    
def test(circles, size):
    
    """ Returns test result for overlapping circles
    
    Keyword arguments:
    circles -- list of circles
    size -- radius of single circle
    """
    
    d_list = []
    i=1
    
    for el_1 in circles:
        
        d_list.clear()
        
        circles_c = circles.copy()
        circles_c.remove(el_1)

        for el_2 in circles_c:
            d = math.sqrt((el_1.get_center()[0] - el_2.get_center()[0])**2 + (el_1.get_center()[1] - el_2.get_center()[1])**2)
            d_list.append(d)
            
            if d < size*2:
                collision = 1
            else: 
                collision = 0
       
        d_min = min(d_list)
        print(str(i) + ". " + colored(d_min, 'green'))
        
        i+=1
    
    return collision
       
def main(saturation, size):
    
    """ Main funcion.
    
    Keyword arguments:
    saturation -- given saturation
    size -- radius of single circle
    
    """
    startTime = time.time()

    global endSaturation
    global circles
    global endTime
    global satList
    global ntimeList
    global com_sat
    
    com_sat = 0
    
    print("Adding circles: Step 1...")
    circles, com_sat, nAttemptsList, ntimeList, satList = search_s1(saturation, size, startTime)

    print("Creating pixels...")
    pixels = box(size)

    print("Creating available pixel list...")
    pixels = access_list(pixels.copy(), circles, size)
    
    while (len(pixels) > 0 and com_sat < saturation):
        print("Actualize available pixel list...")    
        pixels = access_list(pixels.copy(), circles, size)

        print("Adding circles: Step 2...")
        circles, com_sat, ntimeList, satList = search_s2(size, pixels.copy(), circles.copy(), com_sat, saturation, nAttemptsList, ntimeList.copy(), satList.copy(), startTime)  

        print("Dividing pixels...")
        pixels = sub(pixels.copy(), size)
        

    endSaturation = round(math.pi * size**2 * len(circles) * 100, 2)
    com_sat = round(math.pi * size**2 * len(circles) * 100, 2)
    circlesN = len(circles)
    circles = circles.copy() + boundary_cond(circles.copy(), size)

    global fig
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    
    ax.set_xlim(0, V)
    ax.set_ylim(0, V)
    
    acc_pixels = []
    for pixel in pixels:
        p_size = pixel[2]
        acc_pixels.append(pth.Rectangle((pixel[0] - p_size/2, pixel[1] - p_size/2), p_size, p_size, angle=0.0))
        
    """ Free pixels for plot """
    for p in acc_pixels:
        ax.add_artist(p)
        p.set_facecolor('g')
        p.set_edgecolor('k')
        p.set_alpha(0.6)
        
    """ Adding circles to plot """
    for c in circles:
        ax.add_artist(c)
        c.set_clip_box(ax.bbox)
        c.set_alpha(0.6)
        c.set_facecolor('c')
        
    plt.show()
    
    endTime = round(time.time() - startTime, 3)
    
    print("\nNumber of circles: " + str(circlesN))
    print("End saturation: " + str(round(com_sat, 2)) + "%")
    print("End time: " + str(round(endTime, 2)) + "s")
    print("###################################")

def call(saturation, size):    
    
    global endTime

    main(float(saturation), float(size))

#call(100, 0.05)
