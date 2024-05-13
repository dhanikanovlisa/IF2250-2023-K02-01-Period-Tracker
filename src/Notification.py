"""
notification
"""
import winsound
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AlarmClock import AlarmClock
import style.Style as s

class Alarm:
    """
    This is a singleton class of Alarm 
    """
    instance = None
    timeout_signal = pyqtSignal()
    parent = None

    @staticmethod
    def get_instance(parent):
        """
        This function gets previous instace of alarm or construct a new one with different window 
        """
        if Alarm.instance is None:
            return Alarm(parent)
        else:
            Alarm.parent = parent
            return Alarm.instance

    def __init__(self, parent=None):
        """
        This is a constructor for alarm singleton class 
        """
        if Alarm.instance is None:
            self.array_date_time = []
            self.notification = QMessageBox(parent)
            self.timer = AlarmClock()
            self.timer.alarm.connect(self.send_notification_to_system)
            self.notification.setWindowTitle("Notification")
            self.notification.setStyleSheet(s.reminder_msg)
            self.notification.resize(500, 300)
            self.stop_button = self.notification.addButton("stop", QMessageBox.AcceptRole)
            self.stop_button.setStyleSheet(s.go_back_button)
            self.stop_button.clicked.connect(self.stop_audio)
            self.notification.setText("REMINDER")
            self.notification.setInformativeText(
                "Periode menstruasi Anda selanjutnya diprediksi akan dimulai besok!")
            Alarm.instance = self

    def send_notification_to_system(self):
        """
        This function sends notification to window that is opened 
        """
        try:
            winsound.PlaySound("snd/mixkit-casino-jackpot-alarm-and-coins-1991.wav",
                               winsound.SND_ASYNC)
        except:
            pass
        # sound = AudioSegment.from_file(, format="wav")
        # self.playback = play(sound)
        self.notification.move(QDesktopWidget().availableGeometry().center()
                               - self.notification.rect().center())
        self.notification.exec_()

    def stop_audio(self):
        """
        This function stops the alarm when the stop button is pushed 
        """
        try:
            winsound.PlaySound(None, winsound.SND_ASYNC)
        except:
            pass
        self.timer.stop(self.array_date_time[0])
    