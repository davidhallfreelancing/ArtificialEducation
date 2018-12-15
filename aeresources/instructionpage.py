from __future__ import print_function
from PIL import Image, ImageTk
import os
import subprocess
import platform
import time
import Visual as Visual
import Tkinter as Tk


NeededDirectory = os.path.dirname(os.path.realpath(__file__))
os.chdir(NeededDirectory)


class SampleApp(Tk.Tk):

    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)

        container = Tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.grab_set()  # Allow to always see mouse position
        self.frames = {}
        for F in (StoryBoard, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StoryBoard")
        self.raise_app()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def raise_app(self):
        self.attributes("-topmost", True)
        if platform.system() == 'Darwin':
            tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
            script = tmpl.format(os.getpid())
            subprocess.check_call(['/usr/bin/osascript', '-e', script])
        self.after(0, lambda: self.attributes("-topmost", False))


class StoryBoard(Tk.Frame):

    def __init__(self, controller, parent):
        Tk.Frame.__init__(self, parent)
        controller.title('Essay Assistant')
        self.controller = controller
        self.parent = parent
        self.start = 0
        self.stop = 0
        self.pages = []
        self.labels = []
        self.customcontent = []
        self.testlabel = None
        self.previouspage = None
        self.currentpage = None
        self.nextpage = None
        self.imgs = None
        self.canvas = Tk.Canvas(controller, background='black', highlightbackground='black', highlightthickness=0)
        self.instructions = Visual.InstructionBox(self.canvas, self, self.controller)
        self.setup()
        self.imagestore()
        self.pack(expand=Tk.YES, fill=Tk.BOTH)  # packs the frame

    def imagestore(self):

        print(os.getcwd())

        self.imgs = [
            ImageTk.PhotoImage(Image.open("../Resources/background.jpg").resize((1000, 750), Image.ANTIALIAS)),
            #ImageTk.PhotoImage(Image.open("testphoto/2.jpg").resize((500, 500), Image.ANTIALIAS)),
            #ImageTk.PhotoImage(Image.open("testphoto/3.jpg").resize((500, 500), Image.ANTIALIAS))
        ]
        self.pages[0].create_image(0, 0, anchor=Tk.NW, image=self.imgs[0])




    def setup(self):
        self.canvas.place(width=1000, height=50, x=0, y=700)

        pagecolors = ['gray', 'white', 'white']

        for pageid, color in enumerate(pagecolors):
            self.pages.append(Tk.Canvas(self, background='black', highlightthickness=0))
            self.pages[pageid].place(width=1000, height=750, x=pageid * 1000, y=0)

        self.currentpage = 0
        self.nextpage = self.pages[1]

        self.controller.bind('<Motion>', self.motion)

        self.size()

    def size(self):
        width = 1000
        height = 750

        screenwidth = self.controller.winfo_screenwidth()
        screenheight = self.controller.winfo_screenheight()

        horizontal = (screenwidth / 2) - (width / 2)
        vertical = (screenheight / 2) - (height / 2)

        self.controller.geometry('%dx%d+%d+%d' % (width, height, horizontal, vertical-100))

    def pageupdate(self, gotopage, amount):

        if gotopage is not None:

            # GOto page is not === None when returning to 0

            pos = self.pages.index(gotopage)
            if pos > self.currentpage:
                direction = 100
                self.pageidchange(amount)
            else:
                direction = -100
                self.pageidchange(-amount)

            self.on_vertical(gotopage, direction)

    def pageidchange(self, amount):
        if -1 < (self.currentpage + amount) < len(self.pages):
            self.currentpage += amount
            self.instructions.graphics[self.currentpage].selected(None)

        if self.currentpage - 1 < 0:  # self.pages[-1] returns last table item
            self.previouspage = None
        else:
            self.previouspage = self.pages[self.currentpage - 1]

        if self.currentpage + 1 >= len(self.pages):
            self.nextpage = None
        else:
            self.nextpage = self.pages[self.currentpage + 1]

    def on_vertical(self, gotopage, direction):
        while gotopage.winfo_x() != 0:
            for eachpage in self.pages:
                currentx = eachpage.winfo_x()
                eachpage.place_configure(x=currentx - direction)
            self.controller.update()
            time.sleep(.0001)

    def motion(self, event):
        x, y = event.x, event.y
        if 925 < x < 1000:
            if self.delay(1.3):
                pass
                #self.pageupdate(self.nextpage, 1)
        elif 0 < x < 75:
            if self.delay(1.3):
                pass
                #self.pageupdate(self.previouspage, 1)

        # print('{}, {}'.format(x, y))

    def mousetimer(self):
        pass

    def delay(self, seconds):
        # print(self.stop-self.start)
        if (self.stop - self.start) >= seconds:
            self.reset()
            return True
        else:
            self.stop = time.time()
            return False

    def reset(self):
        self.start = time.time()
        self.stop = time.time()


class PageOne(Tk.Frame):

    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
