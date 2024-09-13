from busArrival import *
import tkinter as tk

from PIL import ImageTk, Image
import pathlib, os

#hardcode south gate stops only
southGateNormal = 'B002CEF0DBC568F5'
southGateSpecial = 'E9018F8A7E096544'

###Canvas setup
window = tk.Tk()
xloc = window.winfo_screenwidth() - 330
yloc = window.winfo_screenheight() - 480
window.minsize(160, 240)
window.maxsize(320, 480)
window.geometry('%dx%d+%d+%d' % (320, 480, xloc, yloc))
window.configure(background='#8f0000')
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "#8f0000")

###Image filepath
imageFilename = "busStopRed.png"
currentDir = pathlib.Path(__file__).parent.resolve()
imgPath = os.path.join(currentDir, imageFilename)


global globalUpdate


def updateBusInfo():
    global globalUpdate
    
    globalUpdate = window.after(60000, updateBusInfo)
    
    busNow = getEtaData('B002CEF0DBC568F5')[1] #dictionary - key: bus route, value: list[('time', difference, status)]

    nextArrival = []
    busTimes = []

    #print(busNow)

    for key in busNow:
        #print(key)
        #print(busNow[key][0][2])
        if busNow[key][0][2] != -1: #still have bus
            nextArrival.append(busNow[key][0][1])
            thisBusHours = ""

            routeBuses = busNow[key]
            numBus = len(routeBuses)
            for i in range(numBus): 

                if(i < (numBus - 1)):
                   thisBusHours += (routeBuses[i][0] + " > ")
                else:
                    if(routeBuses[i][2] == 0 and numBus <=2):
                        #last bus
                        thisBusHours += (routeBuses[i][0] + " (Last)")
                    else:
                        thisBusHours += routeBuses[i][0]
            
            #print(routeBuses)
            busTimes.append(thisBusHours)

        else: #no more bus
            #print(key + "no bus")
            nextArrival.append(" - ")
            busTimes.append("last bus has passed")


    nineOneArrival.config(text = nextArrival[0])
    nineOneTimes.config(text = busTimes[0])
    mBusArrival.config(text = nextArrival[1])
    mBusTimes.config(text = busTimes[1])

    
def manualUpdate():
    #print("manually called")
    window.after_cancel(globalUpdate)
    updateBusInfo()



def time():
    current = datetime.now()
    string = current.strftime('%H:%M:%S')
    timeLbl.config(text=current.strftime('%H:%M:%S'))
    timeLbl.after(1000, time)
    if current.hour == 0 and current.second == 0:
        dateLbl.config(text = datetime.now().strftime('%a - %d %b %Y'))


bgImage = tk.PhotoImage(file=imgPath)
#img_Label = tk.Label(image=click_btn)
#button = tk.Button(window, image=click_btn, command = manualUpdate, borderwidth=0, activebackground = '#0078D7')

#button.place(relx = 0.5, rely = 0.5, anchor='center')
signLabel = tk.Label(window, image = bgImage)
signLabel.place(relx = 0.5, rely = 0.5, anchor='center')




timeLbl = tk.Label(window, font=('Helvetica', 26, 'bold'),
            foreground='#333333', bg='white', bd = 0)


    
dateLbl = tk.Label(window, text = datetime.now().strftime('%a - %d %b %Y'), font=('Helvetica', 10),
                   fg = '#333333', bg = 'white', bd = 0)
#todo: update date data via function?



timeLbl.place(relx = 0.5, rely = 0.93, anchor='center')
dateLbl.place(relx = 0.5, rely = 0.995, anchor = 's')


##### Top Frame

topFrame = tk.Frame(window, bg = 'white')
topFrame.place(x=218, y=129, anchor='center')

nineOneArrival = tk.Label(topFrame, font=('Helvetica', 28,'bold'), fg = 'black', bg = 'white', bd=0)
nineOneArrival.grid(row=0, column=0, sticky = 'se', padx=(2, 0))

nineOneTimes = tk.Label(topFrame, font=('Helvetica', 8), fg = 'black', bg = 'white', bd=0)
nineOneTimes.grid(row=1, column = 0, columnspan = 2, sticky = 'n', padx=(2, 2))

nineOneMin = tk.Label(topFrame, text = " min", font=('Helvetica', 8, 'bold'), fg = 'black', bg = 'white', bd=0)
nineOneMin.grid(row=0, column=1,sticky='sw', pady=(0, 9), padx = (0, 2))

###### Bottom Frame

bottomFrame = tk.Frame(window, bg = 'white')
bottomFrame.place(x=218, y=196, anchor='center')

mBusArrival = tk.Label(bottomFrame, font=('Helvetica', 28,'bold'), fg = 'black', bg = 'white', bd=0)
mBusArrival.grid(row=0, column=0, sticky = 'se', padx = (2, 0))

mBusTimes = tk.Label(bottomFrame, font=('Helvetica', 8), fg = 'black', bg = 'white', bd=0)
mBusTimes.grid(row=1, column = 0, columnspan = 2, sticky = 'n', padx=(2, 2))

mBusMin = tk.Label(bottomFrame, text = " min", font=('Helvetica', 8, 'bold'), fg = 'black', bg = 'white', bd=0)
mBusMin.grid(row=0, column=1,sticky='sw', pady=(0, 9), padx=(0, 2))



time()
updateBusInfo()
window.mainloop()
