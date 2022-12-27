#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from urllib.request import urlopen
from common import Utils
import os
import sys
import subprocess
import webbrowser
import locale
import gettext

__version__ = 0.2

appName = 'm3u8maker'
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


class M3u8Maker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.popup = QMessageBox()

        u = Utils()

        groupChannel = [_('FREE CHANNELS'), _('MOVIES CHANNELS'), _('SPORTS CHANNELS'), _('KID CHANNELS'), _('VARIETIES')]

        # Creating main menu
        self.mainMenu = QMenuBar()
        self.setMenuBar(self.mainMenu)

        # File menu
        self.fileMenu = QMenu(_('File'))
        self.fileMenu.addAction(QIcon('icons/menubar/new-file.png'), _('New File'), lambda: u.newFile(self.infoField), 'Ctrl+N')
        self.fileMenu.addAction(QIcon('icons/menubar/open-file.png'), _('Open File...'), lambda: u.openFile(self.infoField), 'Ctrl+O')
        self.fileMenu.addAction(QIcon('icons/menubar/save.png'), _('Save'), lambda: u.saveFile(self.infoField), 'Ctrl+S')
        self.fileMenu.addAction(QIcon('icons/menubar/save-as.png'), _('Save As...'), lambda: u.saveAs(self.infoField), 'Ctrl+Shift+S')
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(QIcon('icons/menubar/quit.png'), _('Quit'), lambda: sys.exit(self.destroy), 'Ctrl+Q')
        self.mainMenu.addMenu(self.fileMenu)

        # Help menu
        self.helpMenu = QMenu(_('Help'))
        self.helpMenu.addAction(QIcon('icons/menubar/check-update.png'), _('Check updates'), lambda: '', 'Ctrl+Shift+R')
        self.helpMenu.addAction(QIcon('icons/menubar/new-update.png'), _('New update available')).setDisabled(True)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(QIcon('icons/menubar/about.png'), _('About'), lambda: '', 'Ctrl+H')
        self.mainMenu.addMenu(self.helpMenu)

        # Setting layouts
        self.cw = QWidget()
        self.mainLayout = QVBoxLayout()
        self.hLayout1 = QHBoxLayout()
        self.hLayout2 = QHBoxLayout()
        self.vLayout = QVBoxLayout()

        self.cw.setLayout(self.mainLayout)

        self.setCentralWidget(self.cw)

        # Setting widgets
        self.channelIdLb = QLabel(_('CHANNEL ID'))
        self.channelIdtxt = QLineEdit()
        self.channelIdtxt.setPlaceholderText(_('Type channel id...'))

        self.channelNameLb = QLabel(_('CHANNEL NAME'))
        self.channelNametxt = QLineEdit()
        self.channelNametxt.setPlaceholderText(_('Type channel name...'))

        self.channelUrlLb = QLabel(_('CHANNEL URL'))
        self.channelUrltxt = QLineEdit()
        self.channelUrltxt.setPlaceholderText(_('Type channel url...'))

        self.logoUrlLb = QLabel(_('LOGO URL'))
        self.logoUrltxt = QLineEdit()
        self.logoUrltxt.setPlaceholderText(_('Type logo url...'))

        self.channelGroupLb = QLabel(_('CHANNEL GROUP'))
        self.channelGrouptxt = QComboBox()
        self.channelGrouptxt.setEditable(False)
        self.channelGrouptxt.addItems(groupChannel)

        self.btnAddInfo = QPushButton(_('ADD INFO'))
        self.btnAddInfo.clicked.connect(lambda: u.addInfo(self.channelIdtxt, self.channelNametxt, self.channelUrltxt, self.logoUrltxt, self.channelGrouptxt, self.infoField))

        self.infoField = QTextEdit()
        self.infoField.setPlaceholderText(_('All typed informations will be setting here...'))

        # Adding widgets to layouts
        self.mainLayout.addLayout(self.hLayout1)
        self.hLayout1.addWidget(self.channelIdLb)
        self.hLayout1.addWidget(self.channelIdtxt)
        self.hLayout1.addWidget(self.channelNameLb)
        self.hLayout1.addWidget(self.channelNametxt)
        self.hLayout1.addWidget(self.channelUrlLb)
        self.hLayout1.addWidget(self.channelUrltxt)

        self.mainLayout.addLayout(self.hLayout2)
        self.hLayout2.addWidget(self.logoUrlLb)
        self.hLayout2.addWidget(self.logoUrltxt)
        self.hLayout2.addWidget(self.channelGroupLb)
        self.hLayout2.addWidget(self.channelGrouptxt)
        self.hLayout2.addWidget(self.btnAddInfo)

        self.mainLayout.addWidget(self.infoField)

        self.setStyleSheet(open('themes/m3u8maker.css').read())

        # Keyboard shortcuts

        clean_fields = QShortcut('Ctrl+L', self)
        clean_fields.activated.connect(lambda: u.cleanFields(self.channelIdtxt, self.channelNametxt, self.channelUrltxt, self.logoUrltxt, self.channelGrouptxt, self.infoField))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = QTranslator()
    locale_ = QLocale().system().name()
    library = os.path.abspath('translations')
    translator.load(f'qt_{locale_}', library)
    win = M3u8Maker()
    win.setWindowTitle('M3u8 Maker')
    win.setWindowIcon(QIcon('icons/mm_logo.png'))
    win.resize(900, 650)
    win.show()
    app.installTranslator(translator)
    sys.exit(app.exec_())
