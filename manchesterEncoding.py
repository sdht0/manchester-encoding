try:
    from Tkinter import *
    import tkFont
except ImportError as err:
    print ("error: %s. Tkinter library is required for using the GUI.") % err.message
    sys.exit(1)


class AutomataGUI:

    def __init__(self, root):
        self.root = root
        self.canvasitems = []
        self.initUI()
        self.inputField.insert(END, "hi there!")
        self.handleInputButton()

    def initUI(self):
        self.root.title("Manchester encoding")
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        ScreenRatioX = 0.7
        ScreenRatioY = 0.9
        self.FrameSizeX = int(ScreenSizeX * ScreenRatioX)
        self.FrameSizeY = int(ScreenSizeY * ScreenRatioY)
        FramePosX = (ScreenSizeX - self.FrameSizeX) / 2
        FramePosY = (ScreenSizeY - self.FrameSizeY) / 2
        padX = 10
        padY = 10
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX, self.FrameSizeY, FramePosX, FramePosY))
        self.root.resizable(width=False, height=False)

        parentFrame = Frame(self.root, width=int(self.FrameSizeX - 2 * padX), height=int(self.FrameSizeY - 2 * padY))
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)

        inputFrame = Frame(parentFrame)
        enterInputLabel = Label(inputFrame, text="Enter input string")
        self.inputField = Text(inputFrame, bg='white', width=40, height=10)
        encodedLabel = Label(inputFrame, text="Encoded Input")
        self.encodedField = Text(inputFrame, bg='white', width=40, height=10)
        self.encodedField.config(state=DISABLED)
        outputLabel = Label(inputFrame, text="Output")
        self.outputField = Text(inputFrame, bg='white', width=40, height=10)
        self.outputField.config(state=DISABLED)
        processInputButton = Button(inputFrame, text="Build", width=10, command=self.handleInputButton)
        enterInputLabel.grid(row=0, column=0, sticky=W)
        self.inputField.grid(row=1, column=0, sticky=W)
        encodedLabel.grid(row=0, column=1, sticky=W)
        self.encodedField.grid(row=1, column=1, sticky=W)
        outputLabel.grid(row=0, column=2, sticky=W)
        self.outputField.grid(row=1, column=2, sticky=W)
        processInputButton.grid(row=2, column=1, padx=5)

        self.statusLabel = Label(parentFrame)

        canvasFrame = Frame(parentFrame, width=int(self.FrameSizeX - 4 * padX), height=int(self.FrameSizeY - 2 * padY))
        self.cwidth = int(self.FrameSizeX - 4 * padX)
        self.cheight = int(self.FrameSizeY * 0.55)
        self.canvas = Canvas(canvasFrame, bg='#FFFFFF', width=self.cwidth, height=self.cheight, scrollregion=(0, 0, self.cwidth, self.cheight))
        hbar = Scrollbar(canvasFrame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.canvas.xview)
        vbar = Scrollbar(canvasFrame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasitems = []
        self.canvas.pack()

        self.bottomLabel = Label(parentFrame, text="Created by Siddhartha under Prof. A. Mustafi [Fundamentals of Data Comm., Dept. of CSE, BIT Mesra]")

        inputFrame.grid(row=0, column=0, sticky=W, padx=(50, 0))
        self.statusLabel.grid(row=1, column=0, sticky=W, padx=(50, 0))
        canvasFrame.grid(row=2, column=0, sticky=E+W+N+S)
        self.bottomLabel.grid(row=3, column=0, sticky=W, pady=10)

    def handleInputButton(self):
        try:
            inp = self.inputField.get(1.0, END)
            if inp == '':
                self.statusLabel.config(text="Detected empty regex!")
                return
            for item in self.canvasitems:
                self.canvas.delete(item)
            self.canvasitems = []
            self.encodedField.config(state=NORMAL)
            self.outputField.config(state=NORMAL)
            self.encodedField.delete(1.0, END)
            self.outputField.delete(1.0, END)
            Y11 = 30
            Y10 = 100
            Y21 = 150
            Y20 = 220
            Y31 = 270
            Y30 = 340
            xpos = 0
            xpos2 = 0
            width = 60
            prev = ""
            font = tkFont.Font(family="times", size=15)
            self.canvasitems.append(self.canvas.create_text(10, Y11 - 30, text="Clock:", font=font, anchor=NW))
            self.canvasitems.append(self.canvas.create_text(10, Y21 - 30, text="Input:", font=font, anchor=NW))
            self.canvasitems.append(self.canvas.create_text(10, Y31 - 30, text="Manchester Encoded Output:", font=font, anchor=NW))
            for ch in inp:
                nm = ord(ch)
                f = self.decToBin(nm)
                s = ""
                for i in range(1, 8 - len(f)):
                    s = s + "0"
                f = s + f
                if ch == "\n":
                    ch = "\\n"
                self.encodedField.insert(END, "%s\t-> %s\t-> %s\n" % (ch, nm, f))
                s2 = ""
                for i in range(len(f)):
                    if f[i] == "0":
                        s2 += "10"
                    if f[i] == "1":
                        s2 += "01"
                    self.canvasitems.append(self.canvas.create_line(xpos2, Y10, xpos2 + width / 2, Y10))
                    self.canvasitems.append(self.canvas.create_line(xpos2 + width / 2, Y10, xpos2 + width / 2, Y11))
                    self.canvasitems.append(self.canvas.create_line(xpos2 + width / 2, Y11, xpos2 + width, Y11))
                    xpos2 = xpos2 + width
                    self.canvasitems.append(self.canvas.create_line(xpos2, Y11, xpos2, Y10))
                    if f[i] == "0":
                        if prev == "1":
                            self.canvasitems.append(self.canvas.create_line(xpos, Y21, xpos, Y20))
                        self.canvasitems.append(self.canvas.create_line(xpos, Y20, xpos + width, Y20))
                        if prev == "0":
                            self.canvasitems.append(self.canvas.create_line(xpos, Y30, xpos, Y31))
                        self.canvasitems.append(self.canvas.create_line(xpos, Y31, xpos + width / 2, Y31))
                        self.canvasitems.append(self.canvas.create_line(xpos + width / 2, Y31, xpos + width / 2, Y30))
                        self.canvasitems.append(self.canvas.create_line(xpos + width / 2, Y30, xpos + width, Y30))
                    elif f[i] == "1":
                        if prev == "0":
                            self.canvasitems.append(self.canvas.create_line(xpos, Y21, xpos, Y20))
                        self.canvasitems.append(self.canvas.create_line(xpos, Y21, xpos + width, Y21))
                        if prev == "1":
                            self.canvasitems.append(self.canvas.create_line(xpos, Y31, xpos, Y30))
                        self.canvasitems.append(self.canvas.create_line(xpos, Y30, xpos + width / 2, Y30))
                        self.canvasitems.append(self.canvas.create_line(xpos + width / 2, Y30, xpos + width / 2, Y31))
                        self.canvasitems.append(self.canvas.create_line(xpos + width / 2, Y31, xpos + width, Y31))
                    xpos = xpos + width
                    prev = f[i]
                self.outputField.insert(END, "%s\n" % s2)
            self.encodedField.config(state=DISABLED)
            self.outputField.config(state=DISABLED)
            self.canvas.config(scrollregion=(0, 0, xpos, int(self.FrameSizeY * 0.5)))
        except BaseException as e:
            self.statusLabel.config(text="Failure: %s" % e)

    def decToBin(self, n):
        if n == 0:
            return ''
        else:
            return self.decToBin(n / 2) + str(n % 2)


def main():
    root = Tk()
    app = AutomataGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
