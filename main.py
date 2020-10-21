# First Page: Intro and url textfield
# Page 2: Loads video details(Thumbnail, Name of video, author, likes, length of video and all streams available-as list to choose(Scrollable if possible))
# Page 3: Start Downloading with indicatorshowing how many chunks downloaded
# Page 4: thanks and redirect to page 1

import tkinter as tk 
from tkinter import ttk 
from tkinter import filedialog
from src import *
import _thread
from math import ceil
# Add new field and button for picking files
# If file is picked add it to text field

LARGEFONT = ("Verdana", 20) 
SMALLFONT = ("Verdana", 10) 

class tkinterApp(tk.Tk): 

    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 

        # self.folder = ""
        
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
        frame = self.frames[cont] 
        self.clearStuff(frame)
        frame.tkraise() 
    
    def getFrame(self, c):
        return self.frames[c]
    
    def clearStuff(self, f):
        if f.entryExist:
            f.Pframe.entry.delete(0, 'end')
            f.Uframe.entry.delete(0, 'end')

# first window frame startpage 

class StartPage(tk.Frame): 
    def __init__(self, parent, controller): 
        # self.cotroller = controller
        self.entryExist = True
        tk.Frame.__init__(self, parent) 
        self.folder = ""

        self.Hframe = HeadingPage1(self, controller)
        self.Hframe.grid(row = 0, padx = 10, pady = 10) 

        self.Pframe = PathPage1(self, controller)
        self.Pframe.grid(row = 1, padx = 10, pady = 10) 

        self.Uframe = UrlPage1(self, controller)
        self.Uframe.grid(row = 2, padx = 10, pady = 10) 
        

class HeadingPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        label = ttk.Label(self, text ="Download From Youtube", font = LARGEFONT) 
        label.pack(side=tk.LEFT, padx=10)

class PathPage1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) 
        self.mystring =tk.StringVar(self)

        label = ttk.Label(self, text="Pick Folder:", font=SMALLFONT)
        label.pack(side=tk.LEFT, padx=5)
        self.entry = ttk.Entry(master=self, textvariable = self.mystring)
        self.entry.pack(side=tk.LEFT, padx=5)

        button1 = ttk.Button(self, text ="Browse..", 
        command = self.getFile)
        button1.pack(side=tk.LEFT, padx=5)
    
    def getFile(self):
        self.controller.folder = filedialog.askdirectory()
        self.mystring.set(self.controller.folder)

class UrlPage1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) 
        self.mystring =tk.StringVar(self)

        label = ttk.Label(self, text="Url:", font=SMALLFONT)
        label.pack(side=tk.LEFT, padx=10)
        self.entry = ttk.Entry(master=self, textvariable = self.mystring)
        self.entry.pack(side=tk.LEFT, padx=10)

        button = ttk.Button(self, text ="Download", 
        command = lambda : self.download())
        button.pack(side=tk.LEFT, padx=10)
    
    def download(self):
        self.controller.show_frame(Page1)
        if self.controller.folder != "":
            url = self.mystring.get()
            try: 
                
                _thread.start_new_thread(self.filedownload, (url,))
                
            except Exception as e:
                print(e)
        else:
            print("No Folder Choosen")

    def filedownload(self, url):
        a = Manager(url).video
        a.getbestaudio(preftype='m4a').download(filepath=self.controller.folder, callback = self.callback)
    
    def callback(self, total, recvd, ratio, rate, eta):
        page2 = self.controller.getFrame(Page1)
        page2.progress['value'] = ceil(ratio*100)
        page2.label['text'] = 'Recieved: ' + str(recvd) + ", ETA: " + str(eta)
        if page2.progress['value'] >= 100:
            page2.button['state'] = tk.NORMAL
            page2.label['text'] = "Download Complete!"
        self.controller.update_idletasks() 

    


# second window frame page1 
class Page1(tk.Frame): 
    def __init__(self, parent, controller): 
        self.entryExist = False
        tk.Frame.__init__(self, parent) 

        self.label = ttk.Label(self, text="Download Will Start Soon!", font=SMALLFONT)
        self.label.grid(row=0, padx = 10, pady = 10)

        self.progress = ttk.Progressbar(self, orient = tk.HORIZONTAL, length = 400, mode = 'determinate')
        self.progress.grid(row = 1, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        self.button = ttk.Button(self, text ="StartPage", state=tk.DISABLED,
                            command = lambda : controller.show_frame(StartPage)) 

        # putting the button in its place 
        # by using grid 
        self.button.grid(row = 2, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        # button2 = ttk.Button(self, text ="Page 2", 
        #                     command = lambda : controller.show_frame(Page2)) 

        # putting the button in its place by 
        # using grid 
        # button2.grid(row = 2, padx = 10, pady = 10) 




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
