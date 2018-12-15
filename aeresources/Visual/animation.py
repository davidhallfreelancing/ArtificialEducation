import time
import math
import Tkinter as Tk


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Tk.Canvas.create_circle = _create_circle


class InstructionDot:
    def __init__(self, parent, box_holder, controller):
        self.hoverwidth = 2
        self.id = 0
        self.box_holder = box_holder
        self.controller = controller
        self.parent = parent
        self.canvas = parent.canvas
        self.status = "deselected"
        self.empty = "black"
        self.fill = "white"
        self.circle = None
        self.mcircle = None
        self.x = None
        self.y = None

    def update(self, x, y):
        self.x, self.y = x, y
        self.mcircle = self.canvas.create_circle(self.x, self.y, 10, fill=self.empty, outline=self.empty, width=1)
        self.circle = self.canvas.create_circle(x, y, 10, fill="", outline=self.fill, width=1)
        self.bind()

    def bind(self):
        #  Need on both to avoid mouse quickly going over dot and activating hover
        for circle in (self.circle, self.mcircle):
            self.canvas.tag_bind(circle, "<Enter>", self.hover)
            self.canvas.tag_bind(circle, "<Leave>", self.normal)
            self.canvas.tag_bind(circle, "<Button-1>", self.selected)

    def rebind(self):  # Used because circle is destroyed and recreated
        self.canvas.tag_bind(self.mcircle, "<Enter>", self.hover)
        self.canvas.tag_bind(self.mcircle, "<Leave>", self.normal)
        self.canvas.tag_bind(self.mcircle, "<Button-1>", self.selected)

    def hover(self, event):
        if False:
            # Just want to get rid of errors
            print(event)
        self.canvas.itemconfig(self.circle, width=2)

    def normal(self, event):
        if False:
            # Just want to get rid of errors
            print(event)

        if self.status == "selected":
            return

        self.canvas.itemconfig(self.circle, width=1)

    def selected(self, event):
        if self.status != "selected":

            self.parent.deselect_all()
            self.status = "selected"

            for x in range(2, 10):
                self.canvas.delete(self.mcircle)
                self.mcircle = self.canvas.create_circle(self.x, self.y, x, fill=self.fill, outline=self.fill, width=1)
                self.canvas.update()
                #time.sleep(.01)

            if event is not None:  # Was clicked by mouse
                self.parent.send_newpage(self.id)

    def deselect(self):
        self.status = "deselected"
        for x in range(2, 9):
            self.canvas.delete(self.mcircle)
            self.mcircle = self.canvas.create_circle(self.x, self.y, 12 - x, fill=self.fill, outline=self.fill, width=1)
            self.canvas.update()
            #time.sleep(.001)

        self.canvas.delete(self.mcircle)
        self.mcircle = self.canvas.create_circle(self.x, self.y, 8, fill=self.empty, outline=self.empty, width=1)
        self.canvas.itemconfig(self.mcircle, fill=self.empty)
        self.canvas.itemconfig(self.mcircle, outline=self.empty)

        self.rebind()


class InstructionBox:
    def __init__(self, canvas, box_holder, controller):
        self.canvas = canvas
        self.parent = box_holder
        self.graphics = []
        for i in range(0, 3):
            self.graphics.append(InstructionDot(self, box_holder, controller))
        self.update()

    def update(self):
        dots = float(len(self.graphics))
        remainder = (dots % 2) / 2
        inverse = abs(math.ceil(remainder - 1))
        adjustment = 25 * inverse
        formula = 500 + adjustment - (50 * (math.floor(dots / 2)))

        for i, eachdot in enumerate(self.graphics):
            x = formula + (50 * i - 1)
            eachdot.update(x, 25)
            eachdot.id = i

        self.graphics[0].selected(None)

    def deselect_all(self):
        for dot in self.graphics:
            if dot.status == "selected":
                dot.deselect()
                dot.normal(None)

    def send_newpage(self, selectedid):
        amount = abs(self.parent.currentpage - selectedid)
        gotopage = self.parent.pages[selectedid]
        self.parent.pageupdate(gotopage, amount)
