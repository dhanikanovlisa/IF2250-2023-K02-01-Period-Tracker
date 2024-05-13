"""
article
"""
from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from Database import DBConnection
from Notification import Alarm
import style.Font as f
import style.Style as s
import Kalendar as calendar
import Settings as settings
import App as app
import ArticlePage as articlepage


class ArticleLayout(QMainWindow):
    """
    This a class of QMainWindow: article layout 
    """
    def __init__(self, *args, **kwargs):
        """
        This is a constructor for article layout window 
        """
        super().__init__(*args, **kwargs)
        # Set window
        self.aticle_window = None

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
        self.article()
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
        if self.aticle_window is None:
            self.aticle_window = app.MainWindow()
            self.aticle_window.showMaximized()
            self.close()

        else:
            self.aticle_window.close()  # Close window.
            self.aticle_window = None

    def go_to_kalendar(self):
        """
        This function sets calendar page as current window 
        """
        if self.aticle_window is None:
            self.aticle_window = calendar.Kalendar()
            self.aticle_window.showMaximized()
            self.close()

        else:
            self.aticle_window.close()  # Close window.
            self.aticle_window = None

    def go_to_settings(self):
        """
        This function sets settings page as current window 
        """
        if self.aticle_window is None:
            self.aticle_window = settings.SettingsLayout()
            self.aticle_window.showMaximized()
            self.close()

        else:
            self.aticle_window.close()  # Close window.
            self.aticle_window = None

    def go_to_article(self):
        """
        This function does nothing, current window already in article window 
        """

    def go_to_article_page(self, article_id):
        """
        This function sets article page as current window 
        """
        if self.aticle_window is None:
            self.aticle_window = articlepage.ArticlePage(article_id)
            self.aticle_window.showMaximized()
            self.close()

        else:
            self.aticle_window.close()  # Close window.
            self.aticle_window = None

    def select_all_summary(self):
        """
        Return all of the article summaries
        """
        get_summaries = QSqlQuery(DBConnection.get_instance())
        get_summaries.exec(
            """
            SELECT IDArticle, Title, Summary
            FROM Articles
            """
        )
        result = []
        while get_summaries.next():
            result.append({"id": get_summaries.value(0), "title": get_summaries.value(
                1), "summary": get_summaries.value(2)})
        return result

    def go_to_article_factory(self, article_id):
        """
        Make a function closure to go to an article
        """
        def go_to_article():
            self.go_to_article_page(article_id)
        return go_to_article

    def article(self):
        """
        This function sets the main layout of article page 
        """
        scroll_area = QScrollArea(self)
        scroll_content = QWidget(scroll_area)
        vbox = QVBoxLayout(self)

        # Article Label Text
        label_article = QLabel('Artikel', self)
        label_article.setFont(f.H1)
        label_article.setStyleSheet(s.h1)
        label_article.resize(150, 100)
        label_article.move(200, 20)

        # getting all article and its summary in database
        result = self.select_all_summary()

        y_offset = 125
        for article_summary in result:
            article_summary_new = {}
            article_summary_new["id"] = deepcopy(article_summary)["id"]
            # def go_to_this_article(): return self. go_to_article_page(article_id)
            frame = QFrame(self)
            frame.setMinimumSize(1050, 135)
            frame_layout = QVBoxLayout(frame)
            frame.setStyleSheet(s.card_frame)
            # getting the returned title from article
            button_card_title = QPushButton(article_summary['title'])
            button_card_title.move(200, y_offset)
            button_card_title.setFont(f.H2)
            button_card_title.setStyleSheet(s.button_card)
            button_card_title.resize(1050, 135)
            button_card_title.clicked.connect(
                self.go_to_article_factory(article_summary["id"]))

            button_card_preview = QPushButton(article_summary['summary'])
            button_card_preview.setStyleSheet(s.card_text)
            button_card_preview.setFont(f.paragraph_card)
            button_card_preview.move(210, y_offset + 30)
            button_card_preview.clicked.connect(
                self.go_to_article_factory(article_summary["id"]))
            # button_card_preview.clicked.connect(self.go_to_article_page())
            frame_layout.addWidget(button_card_title)
            frame_layout.addWidget(button_card_preview)
            vbox.addWidget(frame)
            y_offset += 150

        scrollbar = QScrollBar(self)
        scroll_content.setLayout(vbox)
        scroll_area.setWidget(scroll_content)
        # scrollwidget.setLayout(vbox)
        # scrollarea.setWidget(scrollwidget)
        scroll_area.setVerticalScrollBar(scrollbar)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setGeometry(200, 20, 1730, 850)
        scroll_area.setStyleSheet(s.scroll_area)
        scroll_area.move(190, 125)
