import matplotlib.pyplot as plt
import numpy as np
import math
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

from termcolor import colored
np.random.seed(56478965)
V = 1.0

def search(saturation, size, startTime):
    """ 
    First stage for sequential adsorption. Returns list of 
    non-overlapping circles.
    
    Keyword arguments:
    saturation -- maximal saturation
    size -- size of single circle
    """
    
    global nAttemptsList
    global ntimeList 
    global satList
    
    D = size*2
    com_sat = 0
    N = 0
    added = 0
    nAttempts = 0
    
    nAttemptsList = []
    ntimeList = []
    satList = []
    
    circles = [plt.Circle((np.random.rand(),np.random.rand()), size)]
    
    while (com_sat <= saturation and N < 1000):
        
        N += 1
        nAttempts += 1
        
        newX = np.random.rand()
        newY = np.random.rand()
        
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
            
            
            circles.append(plt.Circle((newX, newY), size))
            com_sat = math.pi * size**2 * len(circles) * 100
            
            added += 1
            nAttemptsList.append(nAttempts)
            ntimeList.append(time.time() - startTime)  
            satList.append(com_sat)
            
            nAttempts = 0
            
        if added >= 3:
            N = 0
            added = 0
            
    return circles, com_sat

def boundary_cond(circles, size):    
    """ 
    Adding boundary conditions for given set of circles.
    Returns list of circles with boundary conditions.
    
    Keyword arguments:
    circles -- list of circles
    size -- size of single circle
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
    
def test(circles, size):   
    """ 
    Returns test result for overlapping circles
    
    Keyword arguments:
    circles -- list of circles
    size -- radius of single circle
    """
    
    d_list = []
    i=1
    
    for el_1 in circles:
        
        d_list.clear()

        circlesCopy = circles.copy()
        circlesCopy.remove(el_1)

        for el_2 in circlesCopy:
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
    """ 
    Main funcion.
    
    Keyword arguments:
    saturation -- given saturation
    size -- size of single circle
    """
    startTime = time.time()
    
    global circles
    global endTime
    global satList
    global ntimeList
    global com_sat
    
    print("Adding circles...")
    circles, com_sat = search(saturation, size, startTime)
    endSaturation = round(math.pi * size**2 * len(circles) * 100, 2)
    com_sat = round(math.pi * size**2 * len(circles) * 100, 2)
    circlesN = len(circles)
    circles = circles.copy() + boundary_cond(circles, size)
    
    global fig
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
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

    main(float(saturation), float(size))


#call(100, 0.05)

