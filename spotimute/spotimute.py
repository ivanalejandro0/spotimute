#!/usr/bin/env python
# encoding: utf-8
import sys
import signal

from PySide import QtCore, QtGui

from ui.ui_main import Ui_Spotimute
import ui.spotimute_rc  # noqa: this is needed to access qt resources


from audiomanager import AudioManager
from spotify import Spotify


class Spotimute(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Create and setup the UI
        self.ui = Ui_Spotimute()
        self.ui.setupUi(self)

        self._spotify = Spotify()
        self._audio = AudioManager()

        self._timer = QtCore.QTimer()
        self._timer.start(500)
        self._timer.timeout.connect(self._get_status)

        self._yes_style = 'background: red; color: white;'
        self._no_style = 'background: green; color: white;'
        self._last_song = None

        # Tray stuff
        self._icon_muted = QtGui.QIcon(':/images/flag-red.png')
        self._icon_unmuted = QtGui.QIcon(':/images/flag-green.png')
        self._tray_icon = self._icon_unmuted

        self.createActions()
        self.createTrayIcon()

        self.trayIcon.activated.connect(self._tray_icon_activated)
        self.trayIcon.show()

    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(Spotimute, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QtGui.QMessageBox.information(
                self, "Systray",
                "The program will keep running in the system tray. To "
                "terminate the program, choose <b>Quit</b> in the "
                "context menu of the system tray entry.")

            self._geometry = self.geometry()
            self.hide()
            event.ignore()

    def _set_tray_icon(self, muted=False):
        icon = None
        if muted:
            icon = self._icon_muted
        else:
            icon = self._icon_unmuted

        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self._tray_icon = icon
        # self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    def _tray_icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.isVisible():
                self._geometry = self.geometry()
                self.hide()
            else:
                self.showNormal()
                self.setGeometry(self._geometry)

        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self._show_tray_message()
        if reason == QtGui.QSystemTrayIcon.MiddleClick:
            pass

    def _show_tray_message(self):
        self.trayIcon.showMessage(
            "Test message", "message body maybe?",
            QtGui.QSystemTrayIcon.Information, 2 * 1000)

    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                                            triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                                            triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                                           triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self,
                                        triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self._set_tray_icon()
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def _get_status(self):
        is_blacklisted = self._spotify.is_blacklisted()

        title = self._spotify.get_title()

        if title != self._last_song and title != 'Spotify':
            self._last_song = title
            if is_blacklisted:
                title = 'Blacklisted! -> ' + title
            else:
                title = title.replace('Spotify - ', '')

            self.ui.lwSongs.addItem(title)
            self.ui.lblSongName.setText(title)

        mute = False
        if is_blacklisted:
            mute = True
            self.ui.lblBlacklisted.setText('  YES  ')
            self.ui.lblBlacklisted.setStyleSheet(self._yes_style)
            self._set_tray_icon(True)
        else:
            self.ui.lblBlacklisted.setStyleSheet(self._no_style)
            self.ui.lblBlacklisted.setText('  NO  ')
            self._set_tray_icon(False)

        if not self._audio.has_sink():
            self.ui.lblIsMuted.setText('  ???  ')
            self.ui.lblIsMuted.setStyleSheet('background: #FFFF00;')
            return

        if self.ui.cbAutoMute.isChecked():
            if mute:
                self._audio.mute()
            else:
                self._audio.unmute()

        if self._audio.is_muted():
            self.ui.lblIsMuted.setText('  YES  ')
            self.ui.lblIsMuted.setStyleSheet(self._yes_style)
        else:
            self.ui.lblIsMuted.setText('  NO  ')
            self.ui.lblIsMuted.setStyleSheet(self._no_style)

    def ask_user(self, title='', question=''):
        response, ok = QtGui.QInputDialog.getText(None, title, question)
        return response, ok

    def display_data(self, data):
        QtGui.QMessageBox.information(self, 'Incoming Data', data)


def main():
    app = QtGui.QApplication(sys.argv)

    window = Spotimute()
    window.show()

    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
