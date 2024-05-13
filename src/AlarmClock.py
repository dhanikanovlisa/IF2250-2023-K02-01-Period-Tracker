"""
AlarmClock
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AlarmClock(QObject):
    """
    A class for alarm 
    """
    alarm = pyqtSignal(QDateTime)
    array_alarm = []

    def __init__(self):
        """
        A constructor for alarmclock class
        """
        super().__init__()
        self.timer = None
        self.alarms = []

    def start(self):
        """
        This function starts the timer
        """
        if self.timer is not None:
            return
        self.timer = self.startTimer(1000)

    def stop(self, date_time):
        """
        This function stops the timer
        """
        if self.timer is None:
            return
        self.killTimer(self.timer)
        if (date_time not in self.array_alarm):
            self.array_alarm.append(date_time)
        self.timer = None

    def add_alarm(self, time):
        """
        This function adds alarm to the alarms
        """
        j = 0
        if time in self.array_alarm:
            print(self.array_alarm)
            print("here")
            self.stop(time)
            return
        if len(self.alarms) != 0:
            for i in range (len(self.alarms)):
                self.alarms.pop(0)
        for i in range (len(self.alarms)):
            if self.alarms[i] < time:
                j += 1
        if (j < len(self.alarms) and self.alarms[j] != time):
            self.alarms.insert(j, time)
        elif j == len(self.alarms):
            self.alarms.append(time)

    def timerEvent(self, ev):
        """
        This function check current daate and current time to emit the alarm
        """
        if ev.timerId() != self.timer:
            QObject.timerEvent(self, ev)
            return
        current = QDateTime.currentDateTime()
        while self.alarms and self.alarms[0] <= current:
            self.alarm.emit(self.alarms[0])
            self.alarms.pop(0)
 