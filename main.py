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
            text='Install aurora store (google play alternative)',
            command=lambda: self.installURL('https://files.auroraoss.com/AuroraStore/Stable/AuroraStore_4.0.7.apk', name='AuroraStore')
        )
    
        b4 = Btn(
            self.parent,
            text='Lawnchair Launcher',
            command=lambda: self.installURL('https://www.apkmirror.com/wp-content/uploads/2021/02/15/60340e66272f7/ch.deletescape.lawnchair.ci_9.1_Alpha_3-9012942_minAPI21(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk?verify=1635584656-NL3vp38nggmOJpBvXe5Zt_ypjH80UiMqi7Q6m3S7z-Y', name='LawnchairLauncher')
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
        print(path)
        subprocess.call((f'{adbpath} disconnect'), shell=True)
        subprocess.call((f'{adbpath} connect 127.0.0.1:58526'), shell=True)
        self.apk(path)
        self.status.set('Finished Installing APK')

    def adbShell(self):
        global adbpath
        subprocess.call((f'{adbpath} disconnect'), shell=True)
        subprocess.call((f'{adbpath} connect 127.0.0.1:58526'), shell=True)
        os.system(f'start cmd /k {adbpath} shell')
        self.status.set('Finished opening adb shell')

    def installURL(self, link, name='app'):
        global adbpath
        subprocess.call((f'{adbpath} disconnect'), shell=True)
        subprocess.call((f'{adbpath} connect 127.0.0.1:58526'), shell=True)

        with urllib3.PoolManager() as http:
            r = http.request('GET', link)
            with open(name+'.apk', 'wb') as f:
                f.write(r.data)

        self.apk(name+'.apk')
        self.status.set('Finished installing '+name)
        
    def apk(self, path):
        global adbpath
        p = subprocess.getoutput(f'{adbpath} install "'+path+'"')
        if 'Package com.aurora.store signatures do not match previously installed version; ignoring!]' in p:
            mb.showwarning('OK', 'Error: signatures do not match previously installed version, try again!')
        elif 'Success' in p:
            mb.showinfo('OK', 'Successfully installed ' + path)
        else:
            mb.showwarning('OK', p)
    
    def installWSL(self):
        self.status.set('Downloading MSIXBUNDLE, do not inturrupt or close the program')
        self.parent.update()
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
        abspath = os.path.abspath('wsa.msixbundle')
        if text.endswith('.msixbundle'):
            url = url.split('"')[-1]
        with requests.get(url, stream=True) as r:
            with open(abspath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        self.status.set('Successfully Downloaded , installing')
        self.parent.update()
        os.system('start cmd /k powershell Add-AppxPackage -Path '+ abspath)
        self.status.set('Installed WSA')

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
