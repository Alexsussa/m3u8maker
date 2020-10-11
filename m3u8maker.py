#!/usr/bin/python3
# -*- encoding: utf-8-*-

from tkinter.ttk import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
from urllib.request import urlopen
from threading import Thread
import os
import sys
import subprocess
import webbrowser
import locale
import gettext

__version__ = 0.1

appName = 'm3u8maker'
dirLocation = os.path.join(os.path.realpath('locale'))

locale.bindtextdomain(appName, dirLocation)
locale.textdomain(appName)

gettext.bindtextdomain(appName, dirLocation)
gettext.textdomain(appName)
_ = gettext.gettext

groupTitles = [_('FREE CHANNELS'), _('MOVIE CHANNELS'), _('SPORTS CHANNELS'), _('KID CHANNELS'), _('VARIETIES')]

pid = os.getpid()
pidFile = '/tmp/m3u8maker'
if not os.path.isfile(pidFile):
    os.system(f'touch {pidFile}')
    os.system(f'echo {pid} >> {pidFile}')
else:
    sys.exit(-1)

global openFileName
openFileName = False


# Checks if there's a new software's version
def checkUpdates(event=None):
    window.unbind('<Enter>')
    linux_version = urlopen('https://www.dropbox.com/s/orvmo3ltilpodsb/m3u8Maker_Linux_Version.txt?dl=true').read()
    if float(linux_version) > float(__version__):
        question = askyesno(title='Status',
                            message=_("There's a new software version avaible to download.\nDownload it now?"))
        subprocess.call(['notify-send', _("There's a new software version avaible to download.\nDownload it now?")])
        if question == YES:
            webbrowser.open('https://github.com/Alexsussa/m3u8maker/releases')
        else:
            window.update()
            window.after(1800000, checkUpdates)


class M3u8Maker:
    def __init__(self, master=None):

        self.c1 = Frame(master)
        self.c1['pady'] = 10
        self.c1['padx'] = 5
        self.c1.pack()

        self.c2 = Frame(master)
        self.c2.pack()

        self.c3 = Frame(master)
        self.c3.pack()

        self.c4 = Frame(master)
        self.c4.pack()

        self.c5 = Frame(master)
        self.c5.pack()

        windowMenu = Menu(window)

        file = Menu(windowMenu, tearoff=0)
        windowMenu.add_cascade(label=_('File'), menu=file)
        file.add_command(label=_('New File'), accelerator='Ctrl+N', command=lambda: self.newFile())
        file.add_command(label=_('Open File...'), accelerator='Ctrl+O', command=lambda: self.openFile())
        file.add_command(label=_('Save'), accelerator='Ctrl+S', command=lambda: self.save())
        file.add_command(label=_('Save As...'), accelerator='Shift+Ctrl+S', command=lambda: self.saveAs())
        file.add_separator()
        file.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=window.destroy)

        help = Menu(windowMenu, tearoff=0)
        windowMenu.add_cascade(label=_('Help'), menu=help)
        help.add_command(label=_('Check updates...'), accelerator='Alt+A',
                         command=lambda: Thread(target=checkUpdates).start())
        help.add_separator()
        help.add_command(label=_('About'), accelerator='Ctrl+H', command=self.about)

        window.config(menu=windowMenu)

        self.menuMouse = Menu(window, tearoff=0)
        self.menuMouse.add_command(label=_('Cut'))
        self.menuMouse.add_command(label=_('Copy'))
        self.menuMouse.add_command(label=_('Paste'))

        self.lbID = Label(self.c1, text='ID', fg='black')
        self.lbID.pack(side=LEFT, padx=2)
        self.txtID = Entry(self.c1, width=15, bg='white', fg='black', selectbackground='blue', selectforeground='white')
        self.txtID.pack(side=LEFT, padx=3)

        self.lbChannel = Label(self.c1, text=_('CHANNEL NAME'), fg='black')
        self.lbChannel.pack(side=LEFT, padx=3)
        self.txtChannel = Entry(self.c1, bg='white', fg='black', width=25, selectbackground='blue',
                                selectforeground='white')
        self.txtChannel.pack(side=LEFT, padx=3)

        self.lbUrl = Label(self.c1, text=_('URL CHANNEL'), fg='black')
        self.lbUrl.pack(side=LEFT, padx=3)
        self.txtUrl = Entry(self.c1, bg='white', fg='black', width=40, selectbackground='blue',
                            selectforeground='white')
        self.txtUrl.pack(side=LEFT, padx=3)

        self.lbLogo = Label(self.c2, text=_('LOGO URL'), fg='black')
        self.lbLogo.pack(side=LEFT, padx=3)
        self.txtLogo = Entry(self.c2, bg='white', fg='black', width=30, selectbackground='blue',
                             selectforeground='white')
        self.txtLogo.pack(side=LEFT, padx=3)

        self.lbGroup = Label(self.c2, text=_('CHANNELS GROUP'), fg='black')
        self.lbGroup.pack(side=LEFT, padx=3)
        self.txtGroup = Combobox(self.c2, background='white', foreground='black', values=groupTitles, width=25,
                                 state='readonly')
        self.txtGroup.pack(side=LEFT, padx=3)

        self.btnAddInfo = Button(self.c2, text=_('ADD INFO'), command=lambda: self.addInfo(), fg='black')
        self.btnAddInfo.pack(side=LEFT, padx=3)

        self.info = ScrolledText(self.c3, width=120, height=30, bg='white', fg='black', selectbackground='blue',
                                 selectforeground='white', undo=True)
        self.info.pack(pady=5)

        # keyboard shortcuts (binds)
        window.bind('<Button-3><ButtonRelease-3>', self.mousePopup)
        window.bind('<Control-n>', self.newFile)
        window.bind('<Control-N>', self.newFile)
        window.bind('<Control-o>', self.openFile)
        window.bind('<Control-O>', self.openFile)
        window.bind('<Control-s>', self.save)
        window.bind('<Control-S>', self.save)
        window.bind('<Control-Shift-p>', self.saveAs)
        window.bind('<Control-Shift-P>', self.saveAs)
        window.bind('<Control-q>', self.windowDestroy)
        window.bind('<Control-Q>', self.windowDestroy)
        window.bind('<Control-h>', self.about)
        window.bind('<Control-H>', self.about)
        window.bind('<Alt-a>', checkUpdates)
        window.bind('<Alt-A>', checkUpdates)
        window.bind('<Enter>', Thread(target=checkUpdates).start())
        window.bind_class('Text', '<Control-a>', self.selectAll)
        window.bind_class('Text', '<Control-A>', self.selectAll)

        # styles for Combobox
        style = Style()
        style.map('TCombobox', selectbackground=[('readonly', 'blue')])
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])

    def selectAll(self, event):
        event.widget.tag_add('sel', '1.0', 'end')
        return 'break'

    def newFile(self, event=None):
        self.info.delete(1.0, END)
        self.info.insert(INSERT, '#EXTM3U\n\n')

    def openFile(self, event=None):
        searchList = askopenfilename(title=_('M3U, M3U8 Files'), filetypes=[(_('IPTV List'), '*.m3u *.m3u8')],
                                     initialdir='~/')
        if searchList:
            global openFileName
            openFileName = searchList
            openList = open(searchList)
            readlist = openList.read()
            self.info.delete(1.0, END)
            self.info.insert(INSERT, readlist)

    def save(self, event=None):
        info = self.info.get(1.0, END)
        global openFileName
        if openFileName:
            save = open(openFileName, 'w')
            save.writelines(info)
            save.close()
            # showinfo(title=_('Status'), message=_('Create a new file by selecting File > New File'))
        else:
            self.saveAs()

    def saveAs(self, event=None):
        info = self.info.get(1.0, END)
        saveFileAs = asksaveasfile(mode='w', title=_('Save As'), filetypes=[(_('IPTV List'), '*.m3u *.m3u8')])
        if saveFileAs:
            saveFileAs.writelines(info)
            saveFileAs.close()

    def addInfo(self):
        idTxt = self.txtID.get()
        logo = self.txtLogo.get()
        group = self.txtGroup.get()
        channel = self.txtChannel.get()
        url = self.txtUrl.get()
        if channel == '' or url == '':
            showerror(title=_('Warning'), message=_('Channel Name or URL cannot be empty'))
        else:
            line = f'\n#EXTINF:-1 tvg-id="{idTxt}" tvg-logo="{logo}" group-title="{group}", {channel}\n{url}\n'
            self.info.insert(END, line)
            self.txtID.delete(0, END)
            self.txtLogo.delete(0, END)
            self.txtGroup.delete(0, END)
            self.txtChannel.delete(0, END)
            self.txtUrl.delete(0, END)

    def mousePopup(self, event):
        w = event.widget
        self.menuMouse.entryconfigure(_('Cut'), command=lambda: w.event_generate('<<Cut>>'))
        self.menuMouse.entryconfigure(_('Copy'), command=lambda: w.event_generate('<<Copy>>'))
        self.menuMouse.entryconfigure(_('Paste'), command=lambda: w.event_generate('<<Paste>>'))
        self.menuMouse.tk_popup(event.x_root, event.y_root)

    def windowDestroy(self, event=None):
        window.destroy()

    def about(self, event=None):
        popup = Toplevel()
        version = Label(popup, text='M3u8 Maker v0.1 (beta)', fg='black')
        version.pack(pady=10)
        img = PhotoImage(file='icons/mm_about.png')
        lbImg = Label(popup, image=img)
        lbImg.pack()
        lbImg.image = img
        github = Label(popup, text='GitHub', cursor='hand2', fg='blue')
        github.pack(pady=5)
        github.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/m3u8maker'))
        license = Label(popup, text=_('License'), cursor='hand2', fg='blue')
        license.pack(pady=5)
        license.bind('<Button-1>',
                     lambda e: webbrowser.open('https://github.com/Alexsussa/m3u8maker/blob/master/LICENSE'))
        creator = Label(popup, text=_('Developed by:'))
        creator.pack(pady=10)
        name = Label(popup, text='Alex Pinheiro', cursor='hand2', fg='blue')
        name.pack()
        name.bind('<Button-1>', lambda e: webbrowser.open('https://t.me/Alexsussa'))
        aboutlogo = PhotoImage(file='icons/mm_logo.png')
        popup.grab_set()
        popup.focus_force()
        popup.transient(window)
        wx = int((window.winfo_screenwidth()) // 2 - (400 // 2))
        wy = int((window.winfo_screenheight() // 2) - (350 // 2))
        popup.geometry(f'400x350+{wx}+{wy}')
        popup.resizable(False, False)
        popup.title(_('About M3u8 Maker'))
        popup.tk.call('wm', 'iconphoto', popup._w, aboutlogo)


window = Tk()
logo = PhotoImage(file='icons/mm_logo.png')
M3u8Maker(window)
window.tk.call('wm', 'iconphoto', window._w, logo)
window.title('M3u8 Maker')
window.geometry(f'1100x610')
window.mainloop()
if window.destroy or window.quit:
    os.unlink(pidFile)
