import naive
import improved
import precise

from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def naiveF(saturation, size, root):
    global flag
    flag = 0
    
    naive.call(saturation, size)
    
    canvas = FigureCanvasTkAgg(naive.fig, root)
    canvas.get_tk_widget().grid(row=4, columnspan = 3)
    canvas.draw()
    
    common_saturation.set(naive.com_sat)
    elapsed_time.set(naive.endTime)
    
    root.update_idletasks()
    
    button_plots['state']=NORMAL
#    button_test['state']=NORMAL
    

def improvedF(saturation, size, root):
    global flag
    flag = 1
    
    improved.call(saturation, size)   
    
    canvas = FigureCanvasTkAgg(improved.fig, root)
    canvas.get_tk_widget().grid(row=4, columnspan = 3)
    canvas.draw()
    
    common_saturation.set(improved.com_sat)
    elapsed_time.set(improved.endTime)
    
    root.update_idletasks()
    
    button_plots['state']=NORMAL
#    button_test['state']=NORMAL
    
def preciseF(saturation, size, root):
    global flag
    flag = 2
    
    precise.call(saturation, size)
    
    canvas = FigureCanvasTkAgg(precise.fig, root)
    canvas.get_tk_widget().grid(row=4, columnspan = 3)
    canvas.draw()
    
    common_saturation.set(precise.com_sat)
    elapsed_time.set(precise.endTime)
    
    root.update_idletasks()
    
    button_plots['state']=NORMAL
#    button_test['state']=NORMAL
    
def details(flag):
    if flag == 0:
        """ Details for naive algorithm """
        
        top = Toplevel(root)
        fig, ax = plt.subplots()
        ax.plot(naive.ntimeList, naive.satList)

        ax.set(xlabel='Czas (s)', ylabel='Osiągnięta saturacja (%)')
    
        canvas = FigureCanvasTkAgg(fig, top)
        canvas.get_tk_widget().grid()
        canvas.draw()
    
    elif flag == 1:
        """ Details for improved algorithm """

        top = Toplevel(root)
        fig, ax = plt.subplots()
        ax.plot(improved.ntimeList, improved.satList)

        ax.set(xlabel='Czas (s)', ylabel='Osiągnięta saturacja (%)')
    
        canvas = FigureCanvasTkAgg(fig, top)
        canvas.get_tk_widget().grid()
        canvas.draw()
        
    elif flag == 2:
        """ Details for precise algorithm """
        
        top = Toplevel(root)
        fig, ax = plt.subplots()
        ax.plot(precise.ntimeList, precise.satList)

        ax.set(xlabel='Czas (s)', ylabel='Osiągnięta saturacja (%)')
    
        canvas = FigureCanvasTkAgg(fig, top)
        canvas.get_tk_widget().grid()
        canvas.draw()
        
# =============================================================================
# def test(flag, size):
#     
#     test = Toplevel(root)
#     
#     if flag == 0:
#         """ Test for precise algorithm """
#         
#         if precise.test(naive.circles, float(size)) == 0:
#             test_result = Label(test, text = "Symulacja zakończona sukcesem")
#         
#         else: 
#             test_result = Label(test, text = "Symulacja zakończona niepowodzeniem")
#     
#     elif flag == 1:
#         """ Test for precise algorithm """
#     
#         if precise.test(improved.circles, float(size)) == 0:
#             test_result = Label(test, text = "Symulacja zakończona sukcesem")
#         
#         else: 
#             test_result = Label(test, text = "Symulacja zakończona niepowodzeniem")
#         
#     elif flag == 2:
#         """ Test for precise algorithm """
#     
#         if precise.test(precise.circles, float(size)) == 0:
#             test_result = Label(test, text = "Symulacja zakończona sukcesem")
#         
#         else: 
#             test_result = Label(test, text = "Symulacja zakończona niepowodzeniem")
#     
#     
#     button_exit = Button(test, text="Ok", padx=25, pady=6, command=test.destroy)
#     
#     test_result.grid(row = 0, column = 0)
#     button_exit.grid(row = 1, column = 0)
# =============================================================================


root = Tk()
root.title("RSA")

common_saturation = StringVar()
elapsed_time = StringVar()


common_saturation.set("0")
elapsed_time.set("0")

""" Pole do wpisania saturacji"""
    
e_sat = Entry(root, width = 15)
e_sat.insert(0, "0 - 100")

""" Pole do wpisania wielskosci próby """

e_size = Entry(root, width = 15)
e_size.insert(0, "0.05 - 0.1")

""" Przyciski """
button_naive = Button(root, text="Algorytm naiwny", padx = 20, pady = 12, command = lambda: naiveF(e_sat.get(), e_size.get(), root))
button_improved = Button(root, text="Algorytm ulepszony", padx=20, pady=12, command = lambda: improvedF(e_sat.get(), e_size.get(), root))
button_precise = Button(root, text="Algorytm precyzyjny", padx=20, pady= 12, command = lambda: preciseF(e_sat.get(), e_size.get(), root))

button_plots = Button(root, text="Szczegóły", padx=15, pady=6, command=lambda: details(flag), state=DISABLED)
#button_test = Button(root, text="Test", padx=35, pady=6, command=lambda: test(flag, e_size.get()), state=DISABLED)
    
""" Labels """
e_sat_label = Label(root, text = "Wysycenie: ")
e_size_label = Label(root, text = "Wielkość: ")

saturation_label_t = Label(root, text = "Osiągnięte wysycenie (%): ", anchor = "w")
saturation_label = Label(root, textvariable =  common_saturation)
    
time_label_t = Label(root, text = "Czas końcowy(s): ", anchor = "w")
time_label = Label(root, textvariable = elapsed_time)


""" Ustawienie obiektów w oknie """
e_sat_label.grid(row = 0, column = 0, padx = 10, pady = 10)
e_sat.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)

e_size_label.grid(row = 0, column = 1, pady = 10, sticky = E)
e_size.grid(row = 0, column = 2, pady = 10, sticky = W)


button_naive.grid(row = 1, column = 0, padx = 5)
button_improved.grid(row = 1, column = 1)
button_precise.grid(row = 1, column = 2, padx = 5)

saturation_label_t.grid(row = 2, column=0)    
saturation_label.grid(row = 2, column = 1, sticky=W)   
    
time_label_t.grid(row = 3, column = 0)  
time_label.grid(row = 3, column = 1, sticky=W)   

#button_test.grid(row = 2, column = 1, rowspan = 2, sticky = E)
button_plots.grid(row = 2, column = 2, rowspan = 2)


def call():
    root.mainloop()
    
    
call()

