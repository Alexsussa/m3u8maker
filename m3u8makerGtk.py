#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from urllib.request import urlopen
from threading import Thread
import os
import sys
import subprocess
import webbrowser
import locale
import gettext

__version__ = 0.1

appName = 'm3u8makergtk'
dirLocation = os.path.join(os.path.realpath('locale'))

locale.bindtextdomain(appName, dirLocation)
locale.textdomain(appName)

gettext.bindtextdomain(appName, dirLocation)
gettext.textdomain(appName)
_ = gettext.gettext

"""pid = os.getpid()
pidFile = '/tmp/m3u8maker'
if not os.path.isfile(pidFile):
    os.system(f'touch {pidFile}')
    os.system(f'echo {pid} >> {pidFile}')
else:
    sys.exit(-1)"""

global openFileName
openFileName = False


class M3u8Maker:
    def __init__(self):
        self.txtID = builder.get_object('txtID')
        self.txtCName = builder.get_object('txtCName')
        self.txtUChannel = builder.get_object('txtUChannel')
        self.txtLUrl = builder.get_object('txtLUrl')
        self.scrolledWindow = builder.get_object('scrolledWindow')
        self.txtViewer = builder.get_object('txtViewer')
        self.txtBuffer = builder.get_object('txtBuffer')
        self.listCGroup = builder.get_object('listCGroup')
        self.bntNew = builder.get_object('bntNew')
        self.btnOpen = builder.get_object('btnOpen')
        self.btnSave = builder.get_object('btnSave')
        self.btnSaveAs = builder.get_object('btnSaveAs')
        self.btnQuit = builder.get_object('btnQuit')
        self.btnAbout = builder.get_object('btnAbout')
        self.status = builder.get_object('status')
        self.chooseListFile = builder.get_object('chooseListFile')
        self.saveListFile = builder.get_object('saveListFile')
        self.winAbout = builder.get_object('winAbout')
        self.askUpdates = builder.get_object('askUpdates')
        self.btnLink = builder.get_object('btnLink')
        self.winAbout.connect('response', lambda d, r: d.hide())
        #self.checkUpdates()

    def on_btnAddInfo_clicked(self, button):
        idTxt = self.txtID.get_text()
        logo = self.txtLUrl.get_text()
        group = self.listCGroup.get_active_text()
        channel = self.txtCName.get_text()
        url = self.txtUChannel.get_text()
        if channel == '' or url == '':
            self.status.set_markup(_('\n\n\nChannel Name and Channel Url cannot be empty.'))
            self.status.show()
        else:
            line = f'\n\n#EXTINF:-1 tvg-id="{idTxt}" tvg-logo="{logo}" group-title="{group}", {channel}\n{url}'
            self.txtBuffer.insert_at_cursor(line)
            self.txtID.set_text('')
            self.txtLUrl.set_text('')
            self.txtCName.set_text('')
            self.txtUChannel.set_text('')

    def on_bntNew_activate(self, button):
        self.txtBuffer.set_text('#EXTM3U')

    def on_btnOpen_activate(self, button):
        self.chooseListFile.show()

    def on_btnSave_activate(self, button):
        start_iter = self.txtBuffer.get_start_iter()
        end_iter = self.txtBuffer.get_end_iter()
        info = self.txtBuffer.get_text(start_iter, end_iter, True)
        global openFileName
        if openFileName:
            save = open(openFileName, 'w')
            save.writelines(info)
            save.close()
            # self.status.set_markup(_('\n\n\nCreate a new file by selecting File > New File.'))
        else:
            self.on_btnSaveAs_activate(button)

    def on_btnSaveAs_activate(self, button):
        self.saveListFile.show()

    def on_btnQuit_activate(self, button):
        Gtk.main_quit()

    def on_btnWarningOk_clicked(self, button):
        self.status.hide()

    def on_btnFileChooserOpen_clicked(self, button):
        searchList = self.chooseListFile.get_filename()
        if searchList:
            global openFileName
            openFileName = searchList
            openList = open(searchList)
            readlist = openList.read()
            self.txtBuffer.set_text('')
            self.txtBuffer.insert_at_cursor(readlist)
            self.chooseListFile.hide()

    def on_chooseListFile_file_activated(self, button):
        self.on_btnFileChooserOpen_clicked(button)
        
    def on_btnFileChooserCancel_clicked(self, button):
        self.chooseListFile.hide()

    def on_btnSaveFileSave_clicked(self, button):
        self.on_btnSaveAs_activate(button)
        start_iter = self.txtBuffer.get_start_iter()
        end_iter = self.txtBuffer.get_end_iter()
        info = self.txtBuffer.get_text(start_iter, end_iter, True)
        fileName = self.saveListFile.get_filename()
        global openFileName
        if fileName:
            save = open(fileName, 'w')
            save.writelines(info)
            save.close()
            self.saveListFile.hide()

    def on_saveListFile_file_activated(self, button):
        self.on_btnSaveFileSave_clicked(button)

    def on_btnSaveFileCancel_clicked(self, button):
        self.saveListFile.hide()

    def on_btnAbout_activate(self, button):
        self.winAbout.show()

    # Checks if there's a new software's version
    def checkUpdates(self):
        linux_version = urlopen('https://www.dropbox.com/s/orvmo3ltilpodsb/m3u8Maker_Linux_Version.txt?dl=true').read()
        if float(linux_version) > float(__version__):
            self.winAbout.show()
            self.btnLink.show()
            subprocess.call(['notify-send', _("There's a new software version available to download.\nBaixe agora!")])
            # webbrowser.open('https://github.com/Alexsussa/m3u8maker/releases')

    def on_btnCheckUpdates_activate(self, button):
        self.checkUpdates()

    def on_btnLink_clicked(self, button):
        Thread(target=webbrowser.open('https://github.com/Alexsussa/m3u8maker/releases')).start()
        self.winAbout.hide()


builder = Gtk.Builder()
builder.set_translation_domain(appName)
builder.add_from_file('m3u8makergtk.ui')
builder.connect_signals(M3u8Maker())
window = builder.get_object(appName)
window.show_all()
window.connect('destroy', Gtk.main_quit)
Gtk.main()
