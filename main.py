import tkinter as tk
from tkinter import filedialog as fd
import os

class Btn(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self['bg'] = '#191919'
        self['fg'] = '#cacaca'
        self['width'] = 20
        self['height'] = 2
        self.draw()

    def draw(self):
        self.pack(pady=8, anchor='center')

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        b1 = Btn(
            self.parent,
            command=self.installAPK,
            text='Install ADB',
        )

        b2 = Btn(
            self.parent,
            text='Open ADB Shell',
            command=self.adbShell
        )
        b2.pack()
    
    
    def installAPK(self):
        path = fd.askopenfilename(
            title='Choose apk file',
            initialdir='HOME',
            filetypes=[('Android Package', '*.apk')]
        )
        path = path.replace(' ', '\\ ')
        print(path)
        os.system('adb disconnect')
        os.system('adb connect 127.0.0.1:58526')
        os.system('adb install ' + path)

    def adbShell(self):

        os.system('adb disconnect')
        os.system('adb connect 127.0.0.1:58526')
        os.system('start cmd /k adb shell')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x500')
    root.title('WSA toolbox')

    HOME = os.path.expanduser('~')
    
    app = App(root)
    app.pack(side='top', fill='both', expand=True)
    root.mainloop()