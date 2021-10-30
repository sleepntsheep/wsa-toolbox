import tkinter as tk
import shutil
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import urllib3
import subprocess
import requests
import re
import sys

class Btn(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self['bg'] = '#191919'
        self['fg'] = '#cacaca'
        self['width'] = 50
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
            text='Install aurora store (play store alternative)',
            command=lambda: self.installURL('https://files.auroraoss.com/AuroraStore/Stable/AuroraStore_4.0.7.apk', name='AuroraStore')
        )
    
        b4 = Btn(
            self.parent,
            text='Installing F-Droid store',
            command=lambda: self.installURL('https://f-droid.org/F-Droid.apk', name='FDroid')
        )


        b5 = Btn(
            self.parent,
            text='Download+install WSA (Windows 11 stable/beta/dev) [need admin]',
            command=self.installWSL
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
        global adbpath
        path = fd.askopenfilename(
            title='Choose apk file',
            initialdir='HOME',
            filetypes=[('Android Package', '*.apk')]
        )
        self.updatestatus('Installing APK')
        self.apk(path)
        self.updatestatus('Finished Installing APK')

    def adbShell(self):
        global adbpath
        subprocess.call((f'{adbpath} disconnect'), shell=True)
        subprocess.call((f'{adbpath} connect 127.0.0.1:58526'), shell=True)
        os.system(f'start cmd /k {adbpath} shell')
        self.updatestatus('Opened adb shell')

    def installURL(self, link, name='app'):
        global adbpath
        if os.path.exists(f'./{name}.apk'):
            os.remove(f'./{name}.apk')
        self.updatestatus('Downloading apk')
        download(link, name+'.apk')
        self.updatestatus('Downloaded apk, installing')
        self.apk(name+'.apk')
        self.updatestatus('Finished installing '+name)
        
    def apk(self, path):
        global adbpath
        subprocess.call((f'{adbpath} disconnect'), shell=True)
        c = subprocess.getoutput(f'{adbpath} connect 127.0.0.1:58526')
        if 'unable to connect' in c:
            mb.showerror('OK', 'Unable to connect, enable developer mode and run WSA if you haven\'t')
            return self.updatestatus('Failed: make sure you opened WSA')
        p = subprocess.getoutput(f'{adbpath} install "'+path+'"')
        if 'Package com.aurora.store signatures do not match previously installed version; ignoring!]' in p:
            mb.showwarning('OK', 'Error: signatures do not match previously installed version, try again!')
        elif 'Success' in p:
            mb.showinfo('OK', 'Successfully installed ' + path)
        else:
            mb.showwarning('OK', p)
    
    def installWSL(self):
        answer = tk.messagebox.askokcancel(
            title = 'Confirmation',
            message = 'Make sure you ran this application as adminastrator',
        )
        if not answer:
            return
        purl = 'https://www.microsoft.com/store/productId/9P3395VX91NR'
        apiurl = 'https://store.rg-adguard.net/api/GetFiles'
        r = requests.post(apiurl, data={
            'type': 'url',
            'url': purl,
            'ring': 'WIS',
            'lang': 'en-US'
        })
        regex = re.search('\)\"><td><a href=\"(.*)\" rel=\"\w{10}\">(.*\.msixbundle)</a></td>', str(r.content))
        url = regex.group(1)
        text = regex.group(2)
        if text.endswith('.msixbundle'):
            url = url.split('"')[-1]
        self.updatestatus('Downloading, windows not responding is normal. Please wait')
        download(url, 'wsa.msixbundle')
        self.updatestatus('Successfully Downloaded , installing')
        os.system('start cmd /k powershell Add-AppxPackage -Path '+ abspath)
        self.updatestatus('Installed WSA')
    
    def updatestatus(self, text):
        self.status.set(text)
        self.parent.update()

def download(url, filename):
    with requests.get(url, stream=True) as r:
        with open(os.path.abspath(filename), 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    WIDTH = 400
    HEIGHT = 500
    try:
        adbpath = resource_path('./adb.exe')
    except :
        adbpath = resource_path('adb.exe')

    adbpath = os.path.abspath(adbpath)

    root = tk.Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.resizable(False, False)
    root.title('WSA toolbox')

    HOME = os.path.expanduser('~')
    
    app = App(root)
    app.pack(side='top', fill='both', expand=True)
    root.mainloop()
