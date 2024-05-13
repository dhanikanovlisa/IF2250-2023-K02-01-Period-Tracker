"""
kalender
"""
from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlQuery
import style.Font as f
import style.Style as s
from Notification import Alarm
import App as app
import Settings as settings
import Article as article
import SymptomForms as symptomforms
import PredictionManager as predictionManager
import ChangeMenstrualStatus as changeMenstrualStatus
from Database import DBConnection
from defaults import symptom_names, symptom_rates


class Kalendar(QMainWindow):
    """
    Kalendar
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
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        self.navigation_bar()
        self.menstrual_status()
        self.selected_date = QDate.currentDate()

        # Deals with rates and symptoms
        self.symptom_name_default = deepcopy(symptom_names)
        self.symptom_names = deepcopy(self.symptom_name_default)
        self.symptom_rate_default = deepcopy(symptom_rates)
        self.symptom_rates = deepcopy(self.symptom_rate_default)

        self.symptom_name_widgets = [
            QLabel(self) for i in enumerate(self.symptom_names)]

        self.symptom_rate_widgets = [
            QLabel(self) for i in enumerate(self.symptom_rates)]

        self.mens_symptoms()
        self.mens_symptoms_rate()
        # self.symptom_name_widgets = []
        # self.sypmtom_rate_widgets = []
        self.update_symptom_name_and_rate()
        self.kalendar()
        self.show()
        self.alarm = Alarm.get_instance(self)
        settings.SettingsLayout.set_alarm(self)

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

    def kalendar(self):
        """
        Calendar
        """
        # Title
        self.title_kalendar = QLabel('Kalender', self)
        self.title_kalendar.setFont(f.H1)
        self.title_kalendar.setStyleSheet(s.h1)
        self.title_kalendar.move(200, 20)
        self.title_kalendar.resize(200, 50)

        # Create calendar widget
        self.calendar = QCalendarWidget(self)

        # Set calendar size
        self.calendar.setFixedSize(650, 500)
        self.calendar.setVerticalHeaderFormat(0)
        self.calendar.move(200, 90)
        self.calendar.setFont(f.button_text)
        self.calendar.setStyleSheet(s.calendar)

        # Change menstrual cycle
        self.add_menstrual = QPushButton("+ Ubah Siklus Mens", self)
        self.add_menstrual.resize(150, 40)
        self.add_menstrual.move(700, 600)
        self.add_menstrual.setFont(f.button_text)
        self.add_menstrual.setStyleSheet(s.button_small)
        # add_menstrual.setGraphicsEffect(s.shadow_purple_md)
        self.add_menstrual.clicked.connect(self.go_to_change_status)

        # Layout Kalendar
        kalendar_layout = QVBoxLayout()
        kalendar_layout.addWidget(self.calendar)
        kalendar_layout.addWidget(self.add_menstrual)
        kalendar_layout.addWidget(self.title_kalendar)

        # Show Selected Date
        self.calendar.clicked[QDate].connect(self.show_date)
        date = self.calendar.selectedDate()

        self.display_date = QLabel(self)
        self.display_date.setFont(f.paragraph)
        self.display_date.setText(date.toString())
        self.display_date.move(870, 305)
        self.display_date.resize(410, 50)
        self.display_date.setAlignment(Qt.AlignCenter)
        self.display_date.setStyleSheet(
            """color: #193F65; font-size: 32px; font-weight: Bold;""")

        self.display_status_menstrual = QLabel(self)
        self.display_status_menstrual.setFont(f.paragraph)
        self.display_status_menstrual.move(200, 600)
        self.display_status_menstrual.resize(300, 50)
        self.display_status_menstrual.setStyleSheet(s.label_cycle)
        # self.display_status_menstrual.setGraphicsEffect(s.shadow_purple_md)

        # Connect to calendar when clicking dates
        self.calendar.clicked[QDate].connect(self.show_status_cycle)
        self.status_cycle, self.day_mens = self.check_cycle(date)

        # Displaying today's date info
        if self.status_cycle:
            text = "Menstruasi Hari ke-" + str(self.day_mens)
            self.display_status_menstrual.setText(text)
        else:
            self.display_status_menstrual.setText(
                "Tidak menstruasi hari ini <3")

    def update_symptom_name_and_rate(self):
        """
        Return the rates for the clicked date
        """
        date_to_select = self.selected_date.toString("yyyy-MM-dd")
        get_today_symptoms = QSqlQuery(DBConnection.get_instance())
        get_today_symptoms.prepare(
            """
            SELECT Name, Rate
            FROM MenstrualSymptoms
            WHERE Date == ? AND BuiltIn == 1;
            """
        )

        get_today_symptoms.addBindValue(date_to_select)
        get_today_symptoms.exec()
        symptom_name_temp = []
        symptom_rate_temp = []
        while get_today_symptoms.next():
            symptom_name_temp.append(get_today_symptoms.value(0))
            symptom_rate_temp.append(get_today_symptoms.value(1))

        # If results were found, use result. Else, use defaults
        if len(symptom_name_temp) > 0:
            self.symptom_names = symptom_name_temp.copy()
        else:
            self.symptom_names = self.symptom_name_default.copy()
        if len(symptom_rate_temp) > 0:
            self.symptom_rates = symptom_rate_temp.copy()
        else:
            self.symptom_rates = self.symptom_rate_default.copy()

        self.set_symptom_rate()
        self.set_symptom_name()


    def show_date(self, date):
        """
        show date
        """
        self.display_date.setText(date.toString())
        self.selected_date = date
        self.update_symptom_name_and_rate()

    def check_cycle(self, date):
        """
        check cycle
        """
        # Fetch all menstrual cycle from database
        cycle = {}

        get_all_cycle_query = QSqlQuery(DBConnection.get_instance())
        get_all_cycle_query.exec(
            """
            SELECT
            strftime("%Y", StartDate) Year,
            strftime("%m", StartDate) Month,
            strftime('%d', StartDate) Day,
            Duration
            FROM MenstrualCycle;
            """
        )

        while get_all_cycle_query.next():
            cycle[QDate(int(get_all_cycle_query.value(0)), int(get_all_cycle_query.value(
                1)), int(get_all_cycle_query.value(2)))] = int(get_all_cycle_query.value(3))

        # Get prediction cyclelength
        prediction_manager = predictionManager.PredictionManager()
        prediction = prediction_manager.calculate_prediction()

        # Insert start menstrual cycle that have been fetched from database
        day_mens = 0
        status_cycle = False
        if len(prediction_manager.prediction)!=0:
            cycle.update(prediction)

        # Displaying All Cycle + Prediction
        for start_date in cycle:
            get_start_date = start_date.day()
            for daterange in range(get_start_date, get_start_date + cycle[start_date]):
                if daterange > start_date.daysInMonth():
                    new_date = daterange % start_date.daysInMonth()
                    new_month = start_date.month() + 1
                else:
                    new_date = daterange
                    new_month = start_date.month()

                if (new_date == date.day() and new_month == date.month()
                and start_date.year() == date.year()):
                    status_cycle = True
                    day_mens = daterange - get_start_date + 1
                    break
        return status_cycle, day_mens

    def show_status_cycle(self, date):
        """
        show status cycle
        """
        status_cycle, day_mens = self.check_cycle(date)
        if status_cycle:
            text = "Menstruasi Hari ke-" + str(day_mens)
            self.display_status_menstrual.setText(text)
        else:
            self.display_status_menstrual.setText(
                "Tidak menstruasi hari ini <3")

    def menstrual_status(self):
        """
        menstry status
        """
        label = QLabel(self)
        pixmap = QPixmap('img/menstrual_status_bg.png')
        pixmap = pixmap.scaled(250, 250)
        label.setPixmap(pixmap)
        label.move(960, 20)
        label.resize(pixmap.width(), pixmap.height())

        day_before_mens, status = self.check_day_before_mens()

        day = QLabel(str(day_before_mens), self)
        day.setStyleSheet("color: #FFE7EC; font-size: 72px; font-weight: Bold")
        day.setFont(f.paragraph)
        day.resize(250, 185)
        day.move(960, 10)
        day.setAlignment(Qt.AlignCenter)

        label2 = QLabel(status, self)
        label2.setStyleSheet(
            "color: #FFE7EC; font-size: 16px; font-weight: Bold")
        label2.setFont(f.paragraph)
        label2.resize(250, 70)
        label2.move(960, 135)
        label2.setAlignment(Qt.AlignCenter)

    def check_day_before_mens(self):
        """
        check day before mens
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

    def mens_symptoms(self):
        """
        mens symptoms
        """
        label = QLabel(self)
        label.setStyleSheet("background-color: #FFE7EC; border-radius: 8px")
        label.setFont(f.paragraph)
        label.resize(410, 350)
        label.move(870, 280)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(176, 188, 216, 128))
        label.setGraphicsEffect(shadow)

        label2 = QLabel("Ada Gejala Apa Hari Ini?", self)
        label2.setStyleSheet("color: #193F65; font-size: 20px")
        label2.setFont(f.paragraph)
        label2.move(920, 375)
        label2.resize(370, 40)

        label3 = QLabel(self)
        label3.move(910, 420)
        label3.resize(360, 200)
        layout = QVBoxLayout()
        label3.setLayout(layout)

        for i, symptom_names in enumerate(self.symptom_names):
            if i >= 5:
                break
            self.symptom_name_widgets[i] = QLabel("-  " + symptom_names, self)
            self.symptom_name_widgets[i].setStyleSheet(
                ("color:  #193F65; font-size: 18px"))
            layout.addWidget(self.symptom_name_widgets[i])

        edit_button = QPushButton(self)
        edit_button.setIcon(QIcon("img/icon/edit.png"))
        edit_button.move(1195, 375)
        edit_button.resize(40, 40)
        edit_button.setStyleSheet(
            "background-color: #193F65; border-radius: 20px")
        edit_button.clicked.connect(self.go_to_symptoms_form)

    def mens_symptoms_rate(self):
        """
        mens symptoms rate
        """
        label = QLabel(self)
        label.move(910, 425)
        label.resize(330, 200)
        layout = QVBoxLayout()
        label.setLayout(layout)
        for _, widget in enumerate(self.symptom_rate_widgets):
            widget.setStyleSheet(("color:  #193F65; font-size: 18px"))
            widget.setAlignment(Qt.AlignRight)
            layout.addWidget(widget)

    def set_symptom_name(self):
        """
        set symptom name
        """
        for i, symptom_name in enumerate(self.symptom_names):
            if i >= 5:
                break
            self.symptom_name_widgets[i] = QLabel("-  " + symptom_name, self)
            self.symptom_name_widgets[i].setStyleSheet("color: rgba(0,0,0,0);")

    def set_symptom_rate(self):
        """
        set symptom rate
        """
        n_of_symptom_rate = len(self.symptom_rates)
        for i, rate_label in enumerate(self.symptom_rate_widgets):
            if n_of_symptom_rate - 1 < i or i >= 5:
                break
            rate_label.setText(str(self.symptom_rates[i])+"/5")

    def go_to_home(self):
        """
        go to home
        """
        if self.wdw is None:
            self.wdw = app.MainWindow()
            self.wdw.showMaximized()
            self.close()

        else:
            self.changeMenstrualStatus.close()
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_kalendar(self):
        """
        go to kalendar
        """

    def go_to_settings(self):
        """
        go to settings
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
        go to article
        """
        if self.wdw is None:
            self.wdw = article.ArticleLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_symptoms_form(self):
        """
        go to symptoms form
        """
        if self.wdw is None:
            self.wdw = symptomforms.SymptomForms(self.selected_date)
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()

    def go_to_change_status(self):
        """
        go to change status
        """
        if self.wdw is None:
            self.wdw = changeMenstrualStatus.MenstrualStatusForm(
                self.selected_date)
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()
