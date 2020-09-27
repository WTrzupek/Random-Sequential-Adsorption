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

V = 1.0
np.random.seed(56478965)

#@profile
def box(size): 
    """ 
    Returns coordinates for pixels in Cartesian system 
    
    Keyword arguments:
    size -- radius of single circle
    
    """
    
    p_size = 0.1 * size*2
    pixels = []
    attempts = 0
    
    for i in np.arange(0, V, p_size):
        for j in np.arange(0, V, p_size):
            pixels.append([i, j, p_size, attempts])

    return pixels
 
    
#@profile
def neighbors(newX, newY, circles, rC):
    """
    Generating list of neighbors for every circle.
    Returns list of neighbors.
    
    Keyword arguments:
    circles -- list of circles
    rC -- neighbor radius
    neighborList -- list of neighbors
    

    """
    neighborList = []
    
    for circle in circles:

        circleX = circle.get_center()[0]
        circleY = circle.get_center()[1]
            
        if (math.sqrt((newX - circleX)**2 + (newY - circleY)**2) < rC or 
            math.sqrt((newX - circleX-V)**2 + (newY - circleY)**2) < rC or 
            math.sqrt((newX - circleX+V)**2 + (newY - circleY)**2) < rC or
            math.sqrt((newX - circleX)**2 + (newY - circleY-V)**2) < rC or
            math.sqrt((newX - circleX)**2 + (newY - circleY+V)**2) < rC or
            math.sqrt((newX - circleX+V)**2 + (newY - circleY+V)**2) < rC or
            math.sqrt((newX - circleX-V)**2 + (newY - circleY+V)**2) < rC or
            math.sqrt((newX - circleX+V)**2 + (newY - circleY-V)**2) < rC or
            math.sqrt((newX - circleX-V)**2 + (newY - circleY-V)**2) < rC):
                
            neighborList.append(circles.index(circle))

    return neighborList
            
    
#@profile           
def search_s1(saturation, size, startTime):
    """ 
    First stage for sequential adsorption.
    Returns list of circles, current saturation, list of times and list
    of saturations.
    
    Keyword arguments:
    size -- radius of single circle
    saturation -- max saturation
    startTime -- start time of algorithm

    
    """
    D = size*2
    rC = size*5
    com_sat = 0
    N = 0
    
    ntimeList = []
    satList = []
    
    circles = [plt.Circle((np.random.rand(),np.random.rand()), size)]
    
    while(com_sat < saturation and N <= 1000):
        
        N += 1
        newX = np.random.rand()
        newY = np.random.rand()
        
        neighborList = neighbors(newX, newY, circles, rC)
        
        if len(neighborList) != 0:
            for e in neighborList:
                
                circleX = circles[e].get_center()[0]
                circleY = circles[e].get_center()[1]
                
                
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
                circles.append(plt.Circle((newX, newY), size))
                com_sat = math.pi * size**2 * len(circles) * 100
                
                ntimeList.append(time.time() - startTime)  
                satList.append(com_sat)
                N = 0
                
        else:
            circles.append(plt.Circle((newX, newY), size))
                
    return circles, com_sat, satList, ntimeList
 
#@profile                
def search_s2(pixels, circles, com_sat, size, saturation, ntimeList, satList, startTime):
    
    """ Second stage for sequential adsorption only in available pixels.
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
    D = size*2

    while(len(pixels) > 0 and com_sat < saturation):

        pixel = random.choice(pixels)
        p_size = pixel[2]
        pixelsC = pixels.copy()
        
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
                pixel[3] += 1
                
                if pixel[3] >= 1000:
                    pixels.remove(pixel)
                break
                
            else:
                collision = 0
        
                            
        if (collision == 0):

            circles.append(plt.Circle((newX, newY), size))
            com_sat = math.pi * size**2 * len(circles) * 100
            pixels = access_list(pixels.copy(), [circle], size)
            ntimeList.append(time.time() - startTime) 
            satList.append(com_sat)

    
    return pixels, circles, com_sat, satList, ntimeList

#@profile
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

#@profile        
def access_list(pixels, circles, size):
    
    """ Returns list of free pixels
    
    Keyword arguments:
    pixels -- list of pixels
    circles -- list of circles
    size -- radius of single circle
    """

    Rpixel = random.choice(pixels)
    p_size = Rpixel[2]
    
    temp = boundary_cond(circles, size)
    circles = circles + temp
    D = size*2

    for circle in circles:
        
        circleX = circle.get_center()[0]
        circleY = circle.get_center()[1]
        pixelsC = pixels.copy()
        
        for pixel in pixelsC:
            
            pixelX = pixel[0]
            pixelY = pixel[1]
            
            w1 = math.sqrt((circleX - pixelX)**2 + (circleY - pixelY)**2)
            w2 = math.sqrt((circleX - (pixelX + p_size))**2 + (circleY - pixelY)**2)
            w3 = math.sqrt((circleX - pixelX)**2 + (circleY - (pixelY + p_size))**2)
            w4 = math.sqrt((circleX - (pixelX + p_size))**2 + (circleY - (pixelY + p_size))**2)

            if w1 <= D and w2 <= D and w3 <= D and w4 <= D:
                pixels.remove(pixel)

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
    size -- size of single circle
    
    """
    
    startTime = time.time()
    
    global endSaturation
    global circles
    global endTime
    global satList
    global ntimeList
    global com_sat
    global endSaturation
    
    print("Adding circles: Step 1...")
    circles, com_sat, satList, ntimeList = search_s1(saturation, size, startTime)
    
    print("Creating pixels...")
    pixels = box(size)
    
    print("Creating available pixel list...")    
    pixels = access_list(pixels.copy(), circles, size)
        
    print("Adding circles: Step 2...")
    pixels, circles, com_sat, satList, ntimeList = search_s2(pixels.copy(), circles.copy(), com_sat, size, saturation, ntimeList.copy(), satList.copy(), startTime)
    
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
        
    """ Adding free pixels to plot """
    for p in acc_pixels:
        ax.add_artist(p)
        p.set_facecolor('g')
        #p.set_edgecolor('k')
        p.set_alpha(0.3)
        
    """ Adding circles to plot """
    for c in circles:
        ax.add_artist(c)
        c.set_clip_box(ax.bbox)
        c.set_alpha(0.6)
        c.set_facecolor('c')
    
    endTime = round(time.time() - startTime, 3)
    
    print("\nNumber of circles: " + str(circlesN))
    print("End saturation: " + str(round(com_sat, 2)) + "%")
    print("End time: " + str(round(endTime, 2)) + "s")
    print("###################################")

def call(saturation, size):    

    main(float(saturation), float(size))

#call(100, 0.05)