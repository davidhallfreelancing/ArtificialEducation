import Tkinter as tk
from PIL import ImageTk, Image
import subprocess
import platform
import os
import time


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Logo, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Logo")
        self.raise_app()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def raise_app(self):
        self.attributes("-topmost", True)
        if platform.system() == 'Darwin':
            tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
            script = tmpl.format(os.getpid())
            output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
        self.after(0, lambda: self.attributes("-topmost", False))



class Logo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.overrideredirect(True)
        self.size()
        self.image()
        self.pack()

    def setup(self):
        self.config(bg="black")

    def size(self):
        width = 708
        height = 310

        screenwidth = self.controller.winfo_screenwidth()
        screenheight = self.controller.winfo_screenheight()

        horizontal = (screenwidth / 2) - (width / 2)
        vertical = (screenheight / 2) - (height / 2)

        self.controller.geometry('%dx%d+%d+%d' % (width, height, horizontal, vertical))

    def image(self):
        self.config(bg="black")
        original = Image.open('icons/logo.png')
        resized = original.resize((708, 82), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        label = tk.Label(self, image=photo, highlightcolor="black", bg="black")
        label.image = photo
        label.place(y=100)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.content(controller)

    def content(self, controller):
        label = tk.Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.after(100000, lambda: app.show_frame("PageOne"))
    app.mainloop()
