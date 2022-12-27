#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import locale
import gettext

appName = 'm3u8maker'
dirLocation = os.path.join(os.path.realpath('locale'))

locale.bindtextdomain(appName, dirLocation)
locale.textdomain(appName)

gettext.bindtextdomain(appName, dirLocation)
gettext.textdomain(appName)
_ = gettext.gettext


global openFileName
openFileName = False


class Utils(QMainWindow):
    def __init__(self):
        super().__init__()


    def showPopup(self, popup, title=str, icon_type=int, msg=str):
        popup.setWindowTitle(title)
        popup.setIcon(popup.Icon(icon_type))
        popup.setText(msg)
        popup.show()


    def newFile(self, text_field):
        text_field.insertPlainText('#EXTM3U8')

    
    def openFile(self, text_field):
        userDir = os.path.expanduser('~/')
        openFile = QFileDialog()
        file_name = openFile.getOpenFileName(self, _('.m3u, .m3u8 Files'), userDir, _('Media files (*.m3u *.m3u8)'), options=openFile.DontUseNativeDialog)

        try:
            if file_name:
                global openFileName
                openFileName = file_name
                file = open(file_name[0], 'r')
                read_file = file.read()
                text_field.setPlainText('')
                text_field.insertPlainText(read_file)
        except FileNotFoundError:
            pass

    
    def saveFile(self, text_field):
        info = text_field.toPlainText()
        global openFileName
        if openFileName:
            file = open(openFileName[0], 'w')
            file.writelines(info)
            file.close()
        else:
            self.saveAs(text_field)

    
    def saveAs(self, text_field):
        userDir = os.path.expanduser('~/')
        info = text_field.toPlainText()
        saveFileAs = QFileDialog()
        saveFileAs.setDefaultSuffix('.m3u8')
        saveAs = saveFileAs.getSaveFileName(self, _('Save file as'), userDir, _('Media files (*.m3u *.m3u8)'), options=saveFileAs.DontUseNativeDialog)

        try:
            file = open(saveAs[0], 'w')
            file.writelines(info)
            file.close()
        except FileNotFoundError:
            pass


    def addInfo(self, id, name, churl, logourl, group, text_field, color):
        widgets_list = [id, name, churl, logourl]

        formated_text = f'\n\n#EXTINF:-1 tvg-id="{id.text()}" tvg="{logourl.text()}" group-title="{group.currentText()}", {name.text()}\n{churl.text()}'

        if not str(churl.text()).startswith(('http://', 'https://')) or not str(logourl.text()).startswith(('http://', 'https://')):

            churl_formated = 'http://' + churl.text()
            logourl_formated = 'http://' + logourl.text()

            formated_text = f'\n\n#EXTINF:-1 tvg-id="{id.text()}" tvg="{logourl_formated}" group-title="{group.currentText()}", {name.text()}\n{churl_formated}'

            text_field.setTextColor(color('blue'))
            text_field.insertPlainText(formated_text)
            text_field.setTextColor(color('black'))

            for widget in widgets_list:
                widget.setText('')
                group.setCurrentIndex(0)
            
        else:
            text_field.setTextColor(color('blue'))
            text_field.insertPlainText(formated_text)
            text_field.setTextColor(color('black'))
            
            for widget in widgets_list:
                widget.setText('')
                group.setCurrentIndex(0)

        
    def cleanFields(self, id, name, churl, logourl, group, text_field):
        widgets_list = [id, name, churl, logourl]
        for widget in widgets_list:
            widget.setText('')
            group.setCurrentIndex(0)
            text_field.setPlainText('')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    u = Utils()
    u.show()
    sys.exit(app.exec_())
    