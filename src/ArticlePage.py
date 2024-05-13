""""
Article page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlQuery
from Notification import Alarm
import style.Font as f
import style.Style as s
import Kalendar as calendar
import Article as article
import App as app
import Settings as settings
from Database import DBConnection


class ArticlePage(QMainWindow):
    """
    This a class of QMainWindow: article page layout 
    """
    def __init__(self, article_id, *args, **kwargs):
        """
        This is a constructor for article page window 
        """
        super().__init__(*args, **kwargs)
        # Set window
        self.wdw = None
        self.article_id = article_id

        # Window Description
        self.setWindowTitle('Period Tracker')
        self.setWindowIcon(QIcon('img/icon/iconWindow.png'))
        self.setStyleSheet(s.bg_color)

        # Navigation Bar background
        label = QLabel(self)
        pixmap = QPixmap('img/navbar_bg.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        self.navigation_bar()
        self.article_page()
        self.show()
        self.alarm = Alarm.get_instance(self)

    def navigation_bar(self):
        """
        Navigation Bar
        """

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

    def go_to_home(self):
        """
        This function sets home page as current window 
        """
        if self.wdw is None:
            self.wdw = app.MainWindow()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_kalendar(self):
        """
        This function sets calendar page as current window 
        """
        if self.wdw is None:
            self.wdw = calendar.Kalendar()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_article(self):
        """
        This function sets article as current window 
        """
        if self.wdw is None:
            self.wdw = article.ArticleLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_settings(self):
        """
        This function sets settings page as current window 
        """
        if self.wdw is None:
            self.wdw = settings.SettingsLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def get_this_article(self):
        """
        This function the article title and content  
        """
        get_articles = QSqlQuery(DBConnection.get_instance())
        get_articles.prepare(
            """
            SELECT Title, Content
            FROM Articles
            WHERE IDArticle == ?
            """
        )
        get_articles.addBindValue(self.article_id)
        get_articles.exec()
        get_articles.next()
        return {"title": get_articles.value(0), "paragraph": get_articles.value(1)}

    def article_page(self):
        """
        This function sets the main layout of article page 
        """
        # go back button
        goback_button_ap = QPushButton(" Go Back", self)
        goback_button_ap.move(200, 10)
        goback_button_ap.setIcon(QIcon("img/icon/backarrow2.png"))
        goback_button_ap.setFont(f.button_text)
        goback_button_ap.resize(95, 30)
        goback_button_ap.setStyleSheet(s.go_back_button)
        goback_button_ap.clicked.connect(self.go_to_article)

        # getting article from database
        result = self.get_this_article()

        label_artikel_1 = QLabel(result["title"], self)
        label_artikel_1.setFont(f.H1)
        label_artikel_1.setStyleSheet(s.h1_settings)
        label_artikel_1.move(200, 60)
        label_artikel_1.resize(1500, 40)

        label_paragraph = QLabel(result["paragraph"], self)
        label_paragraph.setAlignment(Qt.AlignTop | Qt.AlignLeft | Qt.AlignJustify)
        label_paragraph.setFont(f.paragraph_card)
        label_paragraph.setStyleSheet(s.paragraph)
        label_paragraph.resize(1730, 800)
        label_paragraph.move(200, 110)
 