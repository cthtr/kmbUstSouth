from busArrival import *
import tkinter as tk

from PIL import ImageTk, Image
import pathlib, os

#hardcode south gate stops only
southGateNormal = 'B002CEF0DBC568F5'
southGateSpecial = 'E9018F8A7E096544'

pinFlag = False

###Canvas setup
window = tk.Tk()
xloc = window.winfo_screenwidth() - 330
yloc = window.winfo_screenheight() - 480
window.minsize(160, 240)
window.maxsize(320, 480)

window.geometry(f'{320}x{480}+{xloc}+{yloc}')
window.configure(background='#8f0000')
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "#8f0000")
###Image filepath
imageFilename = "busStopRed_corrected.png"
currentDir = pathlib.Path(__file__).parent.resolve()
imgPath = os.path.join(currentDir, imageFilename)


global globalUpdate

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def closeApp():
    quit()

def repositionApp(side = "right"):
    global window
    if side == "left":
        xloc = 0
        yloc = window.winfo_screenheight() - 480
    else:
        xloc = window.winfo_screenwidth() - 330
        yloc = window.winfo_screenheight() - 480
    window.wm_geometry(f'{320}x{480}+{xloc}+{yloc}')
    
def pinApp():
    global m
    global pinFlag
    pinFlag = not pinFlag
    window.attributes('-topmost', pinFlag)
    m.entryconfigure(2, label="Pin App" if pinFlag == False else "Unpin App")
    


def updateBusInfo():
    global globalUpdate
    globalUpdate = window.after(30000, updateBusInfo)
    
    try:
        busNow = getEtaData(southGateNormal)
        nextArrival = []
        busTimes = []

        buses = ([r for r in busNow if r.route == '91'], [r for r in busNow if r.route.upper() == '91M'])

        for bus in buses:   # [0]: 91, [1]: 91M

            # sort in place according to time until bus
            bus.sort(key = lambda x: x.timeTill)

            if bus[0].status == -1: # No more buses
                nextArrival.append(" - ")
                busTimes.append("last bus has passed")

            else:
                # append time till for nearest bus
                nextArrival.append(bus[0].timeTill)

                # append time string for up to 3 buses
                displayTimes = [x.timeString for x in bus if x.status != -1]
                if(len(bus) < 3 and bus[-1].status == 0):
                    displayTimes[-1] += " (Last)"
                busTimes.append(" > ".join(displayTimes[:3]))

        # End of bus for-loop

    except:
        # Any error (mostly used to catch network issues)
        nextArrival = ['?', '?']
        busTimes = ['Disconnected', 'No internet']
        pass

    finally:
        # Config output to tkinter
        nineOneArrival.config(text = nextArrival[0])
        nineOneTimes.config(text = busTimes[0])
        mBusArrival.config(text = nextArrival[1])
        mBusTimes.config(text = busTimes[1])
    
def manualUpdate():
    window.after_cancel(globalUpdate)
    updateBusInfo()

def displayTime():
    current = datetime.now()
    timeLbl.config(text=current.strftime('%H:%M:%S'))
    timeLbl.after(1000, displayTime)
    if current.hour == 0 and current.second == 0:
        dateLbl.config(text = datetime.now().strftime('%a - %d %b %Y'))


bgImage = tk.PhotoImage(file=imgPath)
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

# Popup menu for right click
m = tk.Menu(window, tearoff=0)
m.add_command(label="Reposition App Left", command= lambda: repositionApp("left"))
m.add_command(label="Reposition App Right", command= lambda: repositionApp("right"))
m.add_command(label="Pin App", command = pinApp)
m.add_command(label="Close App", command= closeApp)

signLabel.bind("<Button-3>", do_popup)

displayTime()
updateBusInfo()
window.mainloop()
