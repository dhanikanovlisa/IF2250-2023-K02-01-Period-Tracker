"""
APP
"""
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Notification import Alarm
from Database import DBConnection
import Kalendar as calendar
import Settings as settings
import Article as article
import style.Font as f
import style.Style as s
import PredictionManager as predictionManager


class SplashScreen(QSplashScreen):
    """
    Loading splash screen, for now masih di disable
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlag(Qt.FramelessWindowHint)

        load_splash_image = QPixmap('img/splashscreen.png')
        self.setPixmap(load_splash_image)

        self.p_bar = QProgressBar(self)
        self.p_bar.setFont(f.button_text)
        self.p_bar.setStyleSheet(s.progress_bar)
        self.p_bar.move(420, 470)
        self.p_bar.setGraphicsEffect(s.shadow_purple_lg)

    def progress(self):
        """
        progress
        """
        for i in range(100):
            time.sleep(0.0000000001)
            self.p_bar.setValue(i)


class MainWindow(QMainWindow):
    """
    Main Window
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wdw = None
        self.setWindowTitle('Period Tracker')
        self.setWindowIcon(QIcon('img/icon/iconWindow.png'))
        self.setStyleSheet(s.bg_color)

        # Navigation Bar background
        label = QLabel(self)
        pixmap = QPixmap('img/navbar_bg.png')
        pixmap = QPixmap('img/navbar_bg.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        self.navigation_bar()
        self.welcome_text()
        self.menstrual_status()
        self.show()

        # Initialize database
        DBConnection.get_instance()

        self.alarm = Alarm.get_instance(self)
        settings.SettingsLayout.set_alarm(self)

    def menstrual_status(self):
        """
        Menstrual status
        """
        label = QLabel(self)
        pixmap = QPixmap('img/menstrual_status_bg.png')
        pixmap = pixmap.scaled(500, 500)
        label.setPixmap(pixmap)
        label.move(400, 100)
        label.resize(pixmap.width(), pixmap.height())

        day_before_mens, status = self.check_day_before_mens()

        day = QLabel(str(day_before_mens), self)
        day.setStyleSheet("color: #FFE7EC; font-size: 164px; font-weight: Bold")
        day.setFont(f.paragraph)
        day.resize(500, 275)
        day.move(400, 120)
        day.setAlignment(Qt.AlignCenter)

        label2 = QLabel(status, self)
        label2.setStyleSheet(
            "color: #FFE7EC; font-size: 32px; font-weight: Bold")
        label2.setFont(f.paragraph)
        label2.resize(500, 70)
        label2.move(400, 375)
        label2.setAlignment(Qt.AlignCenter)

    def check_day_before_mens(self):
        """
        Method to check day before mens
        """
        predictionmanager = predictionManager.PredictionManager()
        predictionmanager.calculate_prediction()
        day_before_mens = predictionmanager.get_day_before_mens()
        if day_before_mens is None:
            return "", ""
        elif day_before_mens <= 0:
            return "?", "Anda mungkin akan\n mengalami menstruasi\nhari ini"
        else:
            return day_before_mens, "Hari Sampai Siklus\nMenstruasi Berikutnya"

    def welcome_text(self):
        """
        Welcome label
        """
        label = QLabel("WELCOME",self)
        label.move(400, 600)
        label.resize(500,70)
        label.setStyleSheet(s.h1_welcome)
        label.setAlignment(Qt.AlignCenter)


    def navigation_bar(self):
        """
        Navigation Bar
        """
        #widget = QWidget()
        layout = QVBoxLayout()
        # widget.setLayout(layout)
        # Period Tracker Label Text
        label1 = QLabel('Period\nTracker', self)
        label1.setFont(f.H1)
        label1.setStyleSheet(s.h1_navbar)
        label1.resize(150, 100)
        label1.move(20, 20)

        # Button Beranda/Home
        button_home = QPushButton('Beranda', self)
        button_home.setIcon(QIcon("img/icon/home.png"))
        button_home.setFont(f.button_text)
        button_home.move(20, 150)
        button_home.resize(150, 30)
        button_home.setStyleSheet(s.button_navbar)
        button_home.clicked.connect(self.go_to_home)

        # Button Kalendar
        button_kalendar = QPushButton('Kalender', self)
        button_kalendar.setIcon(QIcon("img/icon/kalendar.png"))
        button_kalendar.setFont(f.button_text)
        button_kalendar.move(20, 200)
        button_kalendar.setStyleSheet(s.button_navbar)
        button_kalendar.resize(150, 30)
        button_kalendar.clicked.connect(self.go_to_kalendar)

        # Button Artikel
        button_artikel = QPushButton('Artikel', self)
        button_artikel.setIcon(QIcon("img/icon/artikel.png"))
        button_artikel.setFont(f.button_text)
        button_artikel.move(20, 250)
        button_artikel.setStyleSheet(s.button_navbar)
        button_artikel.clicked.connect(self.go_to_article)

        # Button Pengaturan
        button_pengaturan = QPushButton('Pengaturan', self)
        button_pengaturan.setIcon(QIcon("img/icon/settings.png"))
        button_pengaturan.setFont(f.button_text)
        button_pengaturan.move(20, 300)
        button_pengaturan.setStyleSheet(s.button_navbar)
        button_pengaturan.resize(150, 30)
        button_pengaturan.clicked.connect(self.go_to_settings)

        layout.addWidget(label1)
        layout.addWidget(button_home)
        layout.addWidget(button_kalendar)
        layout.addWidget(button_artikel)
        layout.addWidget(button_pengaturan)

    def go_to_home(self):
        """
        go to home page 
        """
        if self.wdw is None:
            self.wdw = MainWindow()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_kalendar(self):
        """
        go to calendar page
        """
        if self.wdw is None:
            self.wdw = calendar.Kalendar()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_settings(self):
        """
        go to settings page
        """
        if self.wdw is None:
            self.wdw = settings.SettingsLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_article(self):
        """
        go to article window
        """
        if self.wdw is None:
            self.wdw = article.ArticleLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None


if __name__ == '__main__':

    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    splash.progress()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
