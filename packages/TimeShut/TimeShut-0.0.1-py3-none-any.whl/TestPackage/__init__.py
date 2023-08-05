from tkinter import *
from tkinter import messagebox
import os
import sys
import time
import psutil


FONT_NAME = "Courier"
BGCOLOR = '#323232'
CLOCKCOLOR = '#3232ff'
SETMIN = '00'
SETSEC = '00'
timerr = None
t = 0




#---------------SLEEP---------------------#


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def computer_sleep(seconds_until_sleep=1, verbose=1):
    
    range_top = int(seconds_until_sleep * 10)-1
    spinner_1 = spinning_cursor()
    spinner_2 = spinning_cursor()
    
    if verbose:
        
        for _ in range (range_top, 0, -1):
            
            sys.stdout.write('\r' + spinner_1.__next__() + spinner_2.__next__())
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
            sys.stdout.flush()
            
        sys.stdout.write('\rGoodnight                                       ')
        time.sleep(1)
        sys.stdout.write('\r                                                ')
        
    else:
        
        time.sleep(seconds_until_sleep)
        
    if psutil.OSX:
        
        os.system('pmset sleepnow')
        
    else:
        
        if psutil.LINUX:
            
            os.system('systemctl suspend')
            
        else:
            
            if psutil.WINDOWS:
                
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")




#----------------RESET--------------------#


def reset():
    
    window.after_cancel(timerr)
    timertext.config(text = '00:00:00')
    
    
    

#--------------COUNTDOWN------------------#


def down():
        
    computer_sleep() 
    timertext.config(text = '00:00:00')
    messagebox.showwarning(title='STOP', message='I THINK YOU ARE SLACKING OFF AGAIN')
    
    
def final(coun):
    
    mins,secs = divmod(coun,60)
    hours, mins = divmod(mins,60)
    timer ='{:02d}:{:02d}:{:02d}'.format(hours,mins,secs)
    timertext.config(text = timer)
    
    if coun >0:

        global timerr
        timerr = window.after(1000, final, coun -1) 
        
    else:
        
        down()   

def countdown():
    
    hour = int(h.get()) 
    minu = int(m.get())
    coun = hour*3600 + minu* 60
    final(coun)
    



#---------------UI SETUP------------------#


window = Tk()
window.title('TimeShut')

if psutil.WINDOWS:
    
    window.minsize(575,150)
    window.maxsize(575,150)
    
else:
    
    window.minsize(655,150)
    window.maxsize(655,150)

window.config(bg=BGCOLOR,padx=50,pady=30)


#LABELS

timertext = Label(window, text='00:00:00',font=(FONT_NAME,35,'bold'),bg=BGCOLOR, fg=CLOCKCOLOR)
timertext.grid(column=1,row=1)


#BUTTONS

start= Button(text='Start', command = countdown)
start.grid(row=1,column=0)

reseti= Button(text='Reset', command = reset)
reseti.grid(row=1,column=2)


#ENTRIES

h = Entry(window,bg='#32ffff')
h.grid(row=2,column=0)
h.insert(0,'0')

m = Entry(window,bg='#32ffff')
m.grid(row=2,column=2)
m.insert(0,'0')



window.mainloop()