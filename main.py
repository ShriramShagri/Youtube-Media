# First Page: Intro and url textfield
# Page 2: Loads video details(Thumbnail, Name of video, author, likes, length of video and all streams available-as list to choose(Scrollable if possible))
# Page 3: Start Downloading with indicatorshowing how many chunks downloaded
# Page 4: thanks and redirect to page 1

#  Additional features

# 1) Use pydub to convert audio/video to different formats &&& change metadata.
# 2) Instead of asking for different formats other than downloadable ones...give some dropdown and if the audio isn't in required format, just convert
# 3)

import tkinter as tk 
from tkinter import ttk 
from tkinter import filedialog
import tkinter.messagebox as box
from src import *
import _thread
import os
import sys
from math import ceil


LARGEFONT = ("Verdana", 20) 
SMALLFONT = ("Verdana", 10) 

class tkinterApp(tk.Tk): 

    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        self.geometry("400x400")
        self.resizable(False, False)
        
        # creating a container 
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = False) 

        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 

        # initializing frames to an empty array 
        self.frames = {} 

        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, Page1, Page2): 

            frame = F(container, self) 

            # initializing frame of that object from 
            # startpage, page1, page2 respectively with 
            # for loop 
            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew") 

        self.show_frame(StartPage) 

    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        # Show certain frame based on which page we are in
        frame = self.frames[cont] 

        # Temporary function 
        # REMOVE SOON!!!!
        self.clearStuff(frame)

        frame.tkraise() 
    
    def getFrame(self, c):
        '''
        Used to access frame data of one frame in another

        c  --->  Class instance
        '''
        return self.frames[c]
    
    def clearStuff(self, f):
        # Temporary function 
        # REMOVE SOON!!!!!
        if f.entryExist:
            f.folderEntry.delete(0, 'end')
            f.urlEntry.delete(0, 'end')

# first window frame startpage 

class StartPage(tk.Frame, sys): 
    def __init__(self, parent, controller): 
        # Main class instance
        self.controller = controller

        # Temporary Variable
        self.entryExist = True

        # __init__ function for class Tk.Frame
        tk.Frame.__init__(self, parent) 

        # Frame For heading(Includes only Label)
        self.Hframe = tk.Frame(self)

        self.label = ttk.Label(self.Hframe, text ="Download From Youtube", font = LARGEFONT) 
        self.label.pack(side=tk.LEFT)

        self.Hframe.grid(row = 0, padx = 15, pady = 20) 

        # Frame for folder store path(Entry, Button and Label)
        self.Pframe = tk.Frame(self)

        # Saves folder entry string
        self.folderString =tk.StringVar(self)

        self.folderLabel = ttk.Label(self.Pframe, text="Pick Folder:", font=SMALLFONT)
        self.folderLabel.pack(side=tk.LEFT, padx=5)

        self.folderEntry = ttk.Entry(master=self.Pframe, textvariable = self.folderString)
        self.folderEntry.pack(side=tk.LEFT, padx=5)

        self.folderButton = ttk.Button(self.Pframe, text ="Browse..", command = self.getFile)
        self.folderButton.pack(side=tk.LEFT, padx=5)

        self.Pframe.grid(row = 1, padx = 10, pady = 10) 

        # Frame for folder store path(Entry, Button and Label)
        self.Uframe = tk.Frame(self)
        self.urlString =tk.StringVar(self)

        self.urlLabel = ttk.Label(self.Uframe, text="Url:", font=SMALLFONT)
        self.urlLabel.pack(side=tk.LEFT, padx=10)

        self.urlEntry = ttk.Entry(master=self.Uframe, textvariable = self.urlString)
        self.urlEntry.pack(side=tk.LEFT, padx=10)

        self.urlButton = ttk.Button(self.Uframe, text ="Download", 
        command = lambda : self.download())
        self.urlButton.pack(side=tk.LEFT, padx=10)

        self.Uframe.grid(row = 2, padx = 10, pady = 10) 
    
    def unraisablehook(self):
        '''
        Overriding sys class method to catch errors in Child Thread
        '''
        print('error')
    
    def download(self):
        '''
        Takes to next page 
        ONLY IF
        -> Valid url and folder selected
        '''
        if self.folderString.get() != "":
            # Check if Folder Exists
            if os.path.exists(self.folderString.get()):

                # Change this to end
                self.controller.show_frame(Page1)
                url = self.urlString.get()

                # if no url is selected
                if url == "":
                    box.showerror(title="No Url entered", message="Please enter a folder!")

                # Else check for validity of url
                else:
                    # Set entry strings to empty here

                    # try catch doesn't work....override unraisablehook from sys and try
                    try: 
                        _thread.start_new_thread(self.filedownload, (url,))
                        
                    except Exception as e:
                        print(e)
                        box.showerror(title="Error!", message=str(e))

            # If folder is invalid
            else:
                box.showerror(title="Invalid Path", message="Please choose a valid path")

        # If folder wasn't choosen
        else:
            box.showerror(title="No Folder Selected", message="Please choose a folder!")

    def filedownload(self, url):
        # Temporary Function
        a = Manager(url).video
        a.getbestaudio(preftype='m4a').download(filepath=self.controller.folder, callback = self.callback)
    
    def callback(self, total, recvd, ratio, rate, eta):
        # Status bar update function
        page2 = self.controller.getFrame(Page1)
        page2.progress['value'] = ceil(ratio*100)
        page2.label['text'] = 'Recieved: ' + str(recvd) + ", ETA: " + str(eta)
        if page2.progress['value'] >= 100:
            page2.button['state'] = tk.NORMAL
            page2.label['text'] = "Download Complete!"
        self.controller.update_idletasks() 
    
    def getFile(self):
        self.folderString.set(filedialog.askdirectory())
    

# second window frame page1 
class Page1(tk.Frame): 
    def __init__(self, parent, controller): 
        self.entryExist = False
        tk.Frame.__init__(self, parent) 

        self.label = ttk.Label(self, text="Download Will Start Soon!", font=SMALLFONT)
        self.label.grid(row=0, padx = 10, pady = 20)

        self.progress = ttk.Progressbar(self, orient = tk.HORIZONTAL, length = 400, mode = 'determinate')
        self.progress.grid(row = 1, padx = 10, pady = 20) 

        # button to show frame 2 with text 
        # layout2 
        self.button = ttk.Button(self, text ="StartPage", state=tk.DISABLED,
                            command = lambda : controller.show_frame(StartPage)) 

        self.button.grid(row = 2, padx = 10, pady = 5) 





# third window frame page2 
class Page2(tk.Frame): 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="Page 1", 
                            command = lambda : controller.show_frame(Page1)) 

        # putting the button in its place by 
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        # button to show frame 3 with text 
        # layout3 
        button2 = ttk.Button(self, text ="Startpage", 
                            command = lambda : controller.show_frame(StartPage)) 

        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 


# Driver Code 
app = tkinterApp() 
app.mainloop() 
