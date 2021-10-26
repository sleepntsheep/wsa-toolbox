import tkinter as tk
import time
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import urllib3
import subprocess
import requests

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
            text='Install APK',
        )

        b2 = Btn(
            self.parent,
            text='Open ADB Shell',
            command=self.adbShell
        )
    
        b3 = Btn(
            self.parent,
            text='Install aurora store (google play alternative)',
            command=lambda: self.installURL('https://files.auroraoss.com/AuroraStore/Stable/AuroraStore_4.0.7.apk')
        )

        b4 = Btn(
            self.parent,
            text='Install nova launcher',
            command=lambda: self.installURL('https://d-06.winudf.com/b/APK/Y29tLnRlc2xhY29pbHN3LmxhdW5jaGVyXzcwMDQ5XzFmNmIzMmU0?_fn=Tm92YSBMYXVuY2hlcl92Ny4wLjQ5X2Fwa3B1cmUuY29tLmFwaw&_p=Y29tLnRlc2xhY29pbHN3LmxhdW5jaGVy&am=hlzF95rRCIyp1GC2U_qQJQ&at=1635264415&k=22dbdd2e93eef4c7ec34d2222783875361797920')
        )

        self.status = tk.StringVar()
        self.status.set('Choose an action')

        tk.Label(
            self.parent,
            textvariable=self.status,
            bg='red',
            fg='white',
            width=60,
            height=2,
            ).pack(side='bottom')
    
    def installAPK(self):
        path = fd.askopenfilename(
            title='Choose apk file',
            initialdir='HOME',
            filetypes=[('Android Package', '*.apk')]
        )
        path = path.replace(' ', '\\ ')
        print(path)
        subprocess.call(('adb disconnect'))
        subprocess.call(('adb connect 127.0.0.1:58526'))
        self.apk(path)
        self.status.set('Finished Installing APK')

    def adbShell(self):
        subprocess.call(('adb disconnect'))
        subprocess.call(('adb connect 127.0.0.1:58526'))
        os.system('start cmd /k adb shell')
        self.status.set('Finished opening adb shell')

    def installURL(self, link, name='app'):
        subprocess.call(('adb disconnect'))
        subprocess.call(('adb connect 127.0.0.1:58526'))
        with urllib3.PoolManager() as http:
            r = http.request('GET', link)
            with open('aurora.apk', 'wb') as f:
                f.write(r.data)
        self.apk('aurora.apk')
        self.status.set('Finished installing '+name)
        
    def apk(self, path):
        p = subprocess.getoutput('adb install '+path)
        if 'Package com.aurora.store signatures do not match previously installed version; ignoring!]' in p:
            mb.showwarning('OK', 'Error: signatures do not match previously installed version, try again!')
        elif 'Success' in p:
            mb.showinfo('OK', 'Successfully installed ' + path)
        else:
            mb.showwarning('OK', p)
    
    # def downloadAppx(self):
    #     purl = 'https://www.microsoft.com/store/productId/9P3395VX91NR'


if __name__ == '__main__':
    WIDTH = 400
    HEIGHT = 500

    root = tk.Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.title('WSA toolbox')

    HOME = os.path.expanduser('~')
    
    app = App(root)
    app.pack(side='top', fill='both', expand=True)
    root.mainloop()