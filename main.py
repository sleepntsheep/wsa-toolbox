import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import urllib3
import subprocess

class Btn(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self['bg'] = '#191919'
        self['fg'] = '#cacaca'
        self['width'] = 40
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
    
        b3 = Btn(
            self.parent,
            text='Install aurora store (google play alternative)',
            command=self.auroraStore
        )
    
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
        self.apk(path)

    def adbShell(self):
        os.system('adb disconnect')
        os.system('adb connect 127.0.0.1:58526')
        os.system('start cmd /k adb shell')

    def auroraStore(self):
        link = 'https://files.auroraoss.com/AuroraStore/Stable/AuroraStore_4.0.7.apk'
        os.system('adb disconnect')
        os.system('adb connect 127.0.0.1:58526')
        with urllib3.PoolManager() as http:
            r = http.request('GET', link)
            with open('aurora.apk', 'wb') as f:
                f.write(r.data)
        self.apk('aurora.apk')
        
    def apk(self, path):
        p = subprocess.getoutput('adb install '+path)
        if 'Package com.aurora.store signatures do not match previously installed version; ignoring!]' in p:
            mb.showwarning('OK', 'Error: signatures do not match previously installed version, try again!')
        elif 'Success' in p:
            mb.showinfo('OK', 'Successfully installed ' + path)
        else:
            mb.showwarning('OK', p)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x500')
    root.title('WSA toolbox')

    HOME = os.path.expanduser('~')
    
    app = App(root)
    app.pack(side='top', fill='both', expand=True)
    root.mainloop()