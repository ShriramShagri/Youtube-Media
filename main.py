# First Page: Intro and url textfield
# Page 2: Loads video details(Thumbnail, Name of video, author, likes, length of video and all streams available-as list to choose(Scrollable if possible))
# Page 3: Start Downloading with indicatorshowing how many chunks downloaded
# Page 4: thanks and redirect to page 1

import tkinter as tk 
from tkinter import ttk 
from tkinter import filedialog
from src import *

# Add new field and button for picking files
# If file is picked add it to text field

LARGEFONT = ("Verdana", 20) 

class tkinterApp(tk.Tk): 

    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        
        # creating a container 
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True) 

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
        frame.tkraise() 

# first window frame startpage 

class StartPage(tk.Frame): 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 

        # label of frame Layout 2 
        label = ttk.Label(self, text ="Download From Youtube", font = LARGEFONT) 
        self.mystring =tk.StringVar(self)
        self.mystring2 =tk.StringVar(self)
        
        # putting the grid in its place by using 
        # grid 
        label.grid(row = 0, padx = 10, pady = 10) 

        path = tk.Frame(self)
        path.grid(row = 1, padx = 10, pady = 10) 
        label2 = ttk.Label(path, text="Pick Folder")
        label2.pack(side=tk.LEFT, padx=10)
        self.e1 = ttk.Entry(master=path, textvariable = self.mystring)
        self.e1.pack(side=tk.LEFT, padx=10)

        button1 = ttk.Button(path, text ="Browse..", 
        command = self.getFile)
        button1.pack(side=tk.LEFT, padx=10)

        # putting the button in its place by 
        # using grid 
        # button1.grid(row = 2, column = 1, padx = 10, pady = 10) 

        url = tk.Frame(self)
        url.grid(row = 3, padx = 10, pady = 10) 
        label3 = ttk.Label(url, text="url")
        label3.pack(side=tk.LEFT, padx=10)
        self.e2 = ttk.Entry(master=url, textvariable = self.mystring2)
        self.e2.pack(side=tk.LEFT, padx=10)

        button2 = ttk.Button(url, text ="Download", 
        command = lambda : self.download())
        button2.pack(side=tk.LEFT, padx=10)

        # button2.grid(row = 4, column = 1, padx = 10, pady = 10) 

    def download(self):
        try:
            if self.folder:
                url = self.mystring2.get()
                a = Manager(url).video
                a.getbestaudio(preftype='m4a').download(filepath=self.folder)
        except Exception as e:
            print(e)

    def getFile(self):
        self.folder = filedialog.askdirectory()

# second window frame page1 
class Page1(tk.Frame): 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 

        # putting the button in its place 
        # by using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button2 = ttk.Button(self, text ="Page 2", 
                            command = lambda : controller.show_frame(Page2)) 

        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 




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
