import os
import re
import glob
import shutil
import urllib
import zipfile
import platform
import requests
import subprocess
import ttk as ttk
import Tkinter as Tk
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from AEColors import *
from esky import *


#def check_for_updates():
#    if getattr(sys, "frozen", False):
#        print("Starting update")
#        exe = esky.Esky(sys.executable, "http://www.artificialeducation.com/wp-content/uploads/main/MacOS/")
#        exe.auto_update()
#        print("Updating complete")
#    else:
#        print("The Executable is running")


#def get_local_apps(frame):
#    localapps = frame.controller.frames["LocalApps"]
#    localapps.list_modules()
#    frame.controller.show_frame("LocalApps")


class SampleApp(Tk.Tk):
    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)

        self.overrideredirect(1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.container = Tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nswe")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Dashboard, AppPage, LocalApps, AppDownloadPage, Logo):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nswe")

        self.show_frame("Logo")
        self.raise_app()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.grab_set()
        self.focus_set()
        self.grab_release()

    def raise_app(self):
        self.attributes("-topmost", True)
        if platform.system() == 'Darwin':
            tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
            script = tmpl.format(os.getpid())
            output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
            print(output)
        self.after(0, lambda: self.attributes("-topmost", False))

    def main(self):
        self.tk.call("::tk::unsupported::MacWindowStyle", "style", self._w, "plain", "none")

        self.wm_attributes('-fullscreen', 1)

        self.show_frame("Dashboard")


class Logo(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.overrideredirect(True)
        self.image()
        self.size()

        self.after(7000, self.controller.main)

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
        label = Tk.Label(self, image=photo, highlightcolor="black", bg="black")
        label.image = photo
        label.place(y=100)


class PageAttributes(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="black", width=1000, height=750)
        self.columnconfigure(0, minsize=350)
        self.columnconfigure(1, minsize=350)
        self.place(x=0, y=0)
        self.content = None
        self.apps = []
        self.content_configure()

    def image(self):
        original = Image.open('icons/logo.png')
        resized = original.resize((708, 82), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        label = Tk.Label(self, image=photo, highlightcolor="black", bg="black")
        label.image = photo
        label.pack(side=Tk.TOP, pady=(25, 15))

    def content_configure(self):
        self.image()

        self.content = Tk.Frame(self, bg="black")
        self.content.pack(side=Tk.TOP, pady=0, padx=50, fill=Tk.Y)

        self.content.grid_rowconfigure(0, minsize=255)
        self.content.grid_rowconfigure(1, minsize=255)
        self.content.grid_rowconfigure(2, minsize=255)

        self.content.grid_columnconfigure(0, minsize=350)
        self.content.grid_columnconfigure(1, minsize=350)
        self.content.grid_columnconfigure(2, minsize=350)


class Dashboard(PageAttributes):
    def __init__(self, controller, parent):
        PageAttributes.__init__(self, parent, controller)
        self.addapps()

    def addapps(self):
        self.apps.append(App(self.content, row=0, column=0, rspan=1, cspan=2,
                             bg=lightblue, text="Applications", photo="icons/applications_icon.png",
                             action=lambda: self.controller.show_frame("AppPage"),
                             active=True
                             ))

        self.apps.append(App(self.content, row=0, column=2, rspan=1, cspan=2,
                             bg="purple", text="Artificial Essay", photo="icons/ae_icon.png"))
        self.apps.append(App(self.content, row=1, column=2, rspan=1, cspan=2,
                             bg=orange, text="Artificial Notebook", photo="icons/an_icon.png"))
        self.apps.append(App(self.content, row=2, column=2, rspan=1, cspan=2,
                             bg=blue, text="Artificial Solution", photo="icons/as_icon.png"))

        self.apps.append(App(self.content, row=1, column=0, rspan=1, cspan=1,
                             bg="red", text="Grades", photo="icons/grades_icon.png"))
        self.apps.append(App(self.content, row=2, column=0, rspan=1, cspan=1,
                             text="Download", bg="#00cccc", photo="icons/download_icon.png",
                             action=lambda: self.controller.show_frame("AppDownloadPage"),
                             active=True))

        self.apps.append(App(self.content, row=1, column=1, rspan=1, cspan=1,
                             text="Support", photo="icons/support_icon.png",
                             bg=green))
        self.apps.append(App(self.content, row=2, column=1, rspan=1, cspan=1,
                             text="Feedback", photo="icons/feedback_icon.png",
                             bg="#b29600"))


class AppPage(PageAttributes):
    def __init__(self, parent, controller):
        PageAttributes.__init__(self, parent, controller)
    #self.addapps()

#    def addapps(self):
#        self.apps.append(App(self.content, size=1, hsize=1.5, row=0, column=0, rspan=1, cspan=3,
#                             bg=orange, text="Global", photo="icons/global_icon.png"))
#        self.apps.append(App(self.content, size=1, hsize=1.5, row=1, column=0, rspan=1, cspan=3,
#                             bg=lightblue, text="Local", action=lambda: get_local_apps(self),
#                             photo="icons/local_icon.png",
#                             active=True))


class LocalApps(PageAttributes):
    def __init__(self, parent, controller):
        PageAttributes.__init__(self, parent, controller)

    def addapps(self):

        self.apps.append(App(self.content, size=1, hsize=1, row=0, column=0, rspan=1, cspan=1,
                             text="Home", bg=green, photo="icons/home_icon.png",
                             action=lambda: self.controller.show_frame("Dashboard"),
                             active=True))

    def list_modules(self):
        self.apps = []
        self.addapps()

        for modulename in os.listdir('modules/local'):
            if os.path.isdir("modules/local/" + modulename):

                moduledirectory = "modules/local/" + modulename

                resources = moduledirectory

                x = glob.glob(resources + '/*.app')

                print(resources + '/*.app')
                src = None

                for folder in os.listdir(x[0]):
                    src = x[0]
                    if "Contents" not in folder:
                        src = os.path.join(src, folder)
                        for appdir in os.listdir(src):
                            if ".app" in appdir:
                                src = os.path.join(src, appdir)
                                for contents in os.listdir(src):
                                    src = os.path.join(src, contents)
                                    for innerfolder in os.listdir(src):
                                        if "Resources" in innerfolder:
                                            src = os.path.join(src, innerfolder)

                basepath = os.path.join("modules", "local", modulename)

                self.apps.append(App(self.content, row=0, column=0, rspan=1, cspan=1,
                                     text=modulename, photo=src + "/Resources/icon.png",
                                     bg=orange, active=True,
                                     action=lambda: self.launch_app(modulename, basepath, src)
                                     ))

        row, column = 0, 0
        for eachmodule in self.apps:
            eachmodule.position_configure(row, column)

            column += 1
            if column > 2:
                column = 0
                row += 1

    def launch_app(self, modulename, module, src):

        src = os.path.dirname(src)

        executable1 = os.path.join(src, 'MacOS', 'main')
        executable2 = os.path.join(module, modulename + '.app', 'Contents', 'MacOS', 'main')
        executable3 = os.path.join(os.path.dirname(src))
        executable4 = os.path.join(module, modulename + '.app')

        for exe in (executable1, executable2, executable3, executable4):
            print(exe)

        for exe in (executable1, executable2, executable3, executable4, module):
            def make_executable(path):
                mode = os.stat(path).st_mode
                mode |= (mode & 0o444) >> 2  # copy R bits to X
                os.chmod(path, mode)

            make_executable(exe)

        subprocess.check_call([executable2])

        self.after(2000, lambda: sys.exit(1))


class AppDownloadPage(PageAttributes):
    def __init__(self, parent, controller):
        PageAttributes.__init__(self, parent, controller)
        self.addapps()
        self.after(200, self.list_modules)

    def addapps(self):

        self.apps.append(App(self.content, size=1, hsize=1, row=0, column=0, rspan=1, cspan=1,
                             text="Home", bg=green, photo="icons/home_icon.png",
                             action=lambda: self.controller.show_frame("Dashboard"),
                             active=True))

    def list_modules(self):

        url = "http://artificialeducation.com/wp-content/uploads/modules/MacOS/"
        f = urllib.urlopen(url)
        f = f.read()
        modulelist = re.findall('.*?> (.*?)/</a.*?', str(f))

        for eachmodule in modulelist:
            f = urllib.urlopen(url + eachmodule + '/info.txt')
            f = f.read()
            exec(f)

        row, column = 0, 0
        for eachmodule in self.apps:
            eachmodule.position_configure(row, column)

            column += 1
            if column > 2:
                column = 0
                row += 1


class DownloadBar:
    def __init__(self, parent):
        self.progress = ttk.Progressbar(parent, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.pack(side=Tk.BOTTOM, fill=Tk.X)
        self.parent = parent
        self.bytes = 0
        self.maxbytes = 0

    def start(self, modulename, moduletype):
        def list_url(url):
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            for node in soup.findAll('ul'):
                x = ''.join(node.findAll(text=True))
                modules = x.split('\n')[1:-1]  # Get rid of first parent directory and blank directory at end
                for x in modules:
                    print(x)

                return modules[0][1:]  # [1:] get's rid of space " EPS Generator"

        self.progress["value"] = 0
        self.action = None  # So we can't download twice in a row

        name = modulename
        self.name = modulename
        sys.stdout.write('\rFetching ' + name + '...\n')

        directory = "http://www.artificialeducation.com/wp-content/uploads/modules/MacOS/%s/" % modulename

        download = directory + list_url(directory)

        getfile = download
        savefile = 'modules/%s/%s.zip' % (moduletype, modulename)

        self.module = savefile

        urllib.urlretrieve(getfile, savefile, reporthook=self.read_bytes)

    def read_bytes(self, count, blockSize, totalSize):
        '''simulate reading 500 bytes; update progress bar'''

        self.progress["value"] = count * blockSize
        self.maxbytes = totalSize

        self.progress["maximum"] = totalSize
        self.parent.update()

        if self.progress["value"] >= self.maxbytes:
            self.after(1000, self.unpack_application)

    def unpack_application(self):

        zip = zipfile.ZipFile(self.module)
        directory = "modules/" + self.type + '/' + self.name
        zip.extractall(directory)
        os.remove(self.module)

        for folder in os.listdir(directory):
            if "MAC" in folder:
                try:
                    shutil.rmtree(directory + "/" + folder)
                except:
                    print("Couldn't remove Mac Directory")

        try:
            shutil.rmtree(self.module[:-4] + "/.idea/")
            shutil.rmtree(directory + self.type + "/" + "__MACOSX")
        except Exception as e:
            print('no /.idea', e)
        self.activate_application()

    def activate_application(self):
        self.action = None
        self.bg = self.bg_downloaded
        self.photo = self.photo_normal
        self.photo_hover = self.photo

        self.config(bg=self.bg, highlightbackground=self.bg)
        for widget in self.widgets:
            widget.config(bg=self.bg)

        self.progress.pack_forget()
        self.update_button()
        self.parent.update()


class CustomButton(Tk.Frame, DownloadBar):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent)
        self.k = kwargs

        self.appname = None
        self.img = None  # The image opened with PIL Image
        self.img2 = None  # The Image after being transformed for Tkinter
        self.imgtag = None  # The Image Object now inside the Tkinter Canvas
        self.label = None
        self.widgets = []

        self.action = kwargs.get('action', None)
        self.active = kwargs.get('active', False)
        self.bg = kwargs.get('bg', "#7e7e7e")
        self.name = kwargs.get('text', 'No Current Module')
        self.photo = kwargs.get('photo', 'icons/eps_icon.png')
        self.photo_normal = kwargs.get('photo', 'icons/eps_icon.png')
        self.photo_hover = kwargs.get('hoverphoto', self.photo)
        self.type = kwargs.get('type', 'local')

    def button_bindings(self):
        if not self.active:
            return

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_normal)
        self.bind("<Button-1>", self.on_clicked)

        for widget in self.widgets:
            widget.bind("<Button-1>", self.on_clicked)

    def button_text(self):
        self.appname = Tk.Label(self, text=self.name, font=("OpenSans", 24), fg="white", bg=self.bg, bd=0)
        self.appname.place(relx=0.5, rely=.8, anchor=Tk.CENTER)

        self.widgets.append(self.appname)

    def button_image(self):
        self.img = Image.open(self.photo)
        self.img = self.img.resize((50, 50), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img)
        self.label = Tk.Label(self, image=self.img2, bg=self.bg, bd=0)
        self.label.image = self.img2
        self.label.place(relx=0.5, rely=0.4, anchor=Tk.CENTER)

        self.widgets.append(self.label)

    def on_hover(self, event):
        if False:
            print(event)

        self.config(highlightbackground="white", highlightthickness=2)

        self.photo = self.photo_hover

        self.update_button()

    def on_clicked(self, event):
        if False:
            print(event)

        try:
            self.action()
        except Exception as e:
            print(e)

    def on_normal(self, event):
        if False:
            print(event)

        self.config(highlightbackground=self.bg, highlightthickness=0)

        for widget in self.widgets:
            widget.config(bg=self.bg)

        self.photo = self.photo_normal

        self.update_button()

    def update_button(self):
        self.button_image()
        self.button_bindings()


class App(CustomButton):
    def __init__(self, parent, row, column, rspan, cspan, **kwargs):
        CustomButton.__init__(self, parent, **kwargs)

        #  self.action = lambda: os.system("python modules/local/"+self.name+"/main.py")
        self.size = kwargs.get('size', 1)
        self.hsize = kwargs.get('hsize', 1)

        self.button_image()  # Creates Label
        self.button_text()  # Creates appname
        self.widgets = [self.label, self.appname]
        self.button_bindings()

        self.config(width=350 * self.size, height=255 * self.hsize,
                    bg=self.bg, highlightthickness=1, highlightbackground=self.bg)

        self.grid(row=row, column=column, rowspan=rspan, columnspan=cspan, padx=5, pady=5, sticky="nswe")

    def position_configure(self, row, column):
        self.grid(row=row, column=column)


class App_UnInstalled(CustomButton):
    def __init__(self, parent, row, column, rspan, cspan, **kwargs):
        CustomButton.__init__(self, parent, **kwargs)
        DownloadBar.__init__(self, self)

        self.action = lambda: self.download(self.name, self.type)
        self.size = kwargs.get('size', 1)
        self.hsize = kwargs.get('hsize', 1)
        self.bg = "lightgrey"
        self.bg_downloaded = kwargs.get('bg', 'grey')

        self.button_image()  # Creates Label
        self.button_text()  # Creates appname
        self.widgets = [self.label, self.appname]
        self.button_bindings()

        self.config(width=350 * self.size, height=255 * self.hsize,
                    bg=self.bg, highlightthickness=1, highlightbackground=self.bg)

        self.grid(row=row, column=column, rowspan=rspan, columnspan=cspan, padx=5, pady=5, sticky="nswe")

        for module in os.listdir('modules/' + self.type):
            if self.name in module:
                self.activate_application()

    def position_configure(self, row, column):
        self.grid(row=row, column=column)

    def download(self, modulename, moduletype):
        self.start(modulename, moduletype)


if __name__ == "__main__":
    # check_for_updates()
    app = SampleApp()
    app.mainloop()
