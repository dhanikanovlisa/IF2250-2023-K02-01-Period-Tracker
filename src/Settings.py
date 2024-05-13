"""
settings
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlQuery
from Notification import Alarm
from Database import DBConnection
import style.Font as f
import style.Style as s
import Kalendar as calendar
import Article as article
import App as app
import PredictionManager as prediction


class SettingsLayout(QMainWindow):
    """
    Settings Layout for settings page 
    """
    def __init__(self, *args, **kwargs):
        """
        This is a constructor for settings layout window 
        """
        super().__init__(*args, **kwargs)
        self.settings_window = None
        self.setWindowTitle('Period Tracker')
        self.setWindowIcon(QIcon('img/icon/iconWindow.png'))
        self.setStyleSheet(s.bg_color)
        self.edit_mode_month = False
        self.edit_mode_time = False

        # Navigation Bar background
        label = QLabel(self)
        pixmap = QPixmap('img/navbar_bg.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        self.edit_mode_time = False
        self.edit_mode_month = False
        self.navigation_bar()
        self.settings()

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
        button_calendar = QPushButton('Kalender', self)
        button_calendar.setIcon(QIcon("img/icon/kalendar.png"))
        button_calendar.setFont(f.button_text)
        button_calendar.move(20, 200)
        button_calendar.setStyleSheet(s.button_navbar)
        button_calendar.resize(150, 30)
        button_calendar.clicked.connect(self.go_to_kalendar)

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
        This function calls home page
        """
        if self.settings_window is None:
            self.settings_window = app.MainWindow()
            self.settings_window.showMaximized()
            self.close()

        else:
            self.settings_window.close()  # Close window.
            self.settings_window = None

    def go_to_kalendar(self):
        """
        This function calls calendar page
        """
        if self.settings_window is None:
            self.settings_window = calendar.Kalendar()
            self.settings_window.showMaximized()
            self.close()

        else:
            self.settings_window.close()  # Close window.
            self.settings_window = None

    def go_to_settings(self):
        """
        This function does nothing because it's already in settings page 
        """

    def go_to_article(self):
        """
        This function calls article page
        """
        if self.settings_window is None:
            self.settings_window = article.ArticleLayout()
            self.settings_window.showMaximized()
            self.close()

        else:
            self.settings_window.close()  # Close window.
            self.settings_window = None

    def settings(self):
        """
        This is the main settings layout 
        """
        self.initialize_setting()

        # Settings Label Text
        label_settings = QLabel('Pengaturan', self)
        label_settings.setFont(f.H1)
        label_settings.setStyleSheet(s.h1_settings)
        label_settings.resize(200, 100)
        label_settings.move(200, 20)

        # Pengingat Label Text
        label_pengingat = QLabel('Atur Pengingat', self)
        label_pengingat.setFont(f.H2)
        label_pengingat.setStyleSheet(s.h2)
        label_pengingat.move(200, 125)
        label_pengingat.resize(200, 30)

        # Edit Button Time
        self.edit_button_time = QPushButton("Edit", self)
        self.edit_button_time.setIcon(QIcon("img/icon/editred.png"))
        self.edit_button_time.setFont(f.radio_button_text)
        self.edit_button_time.setStyleSheet(s.edit_button)
        self.edit_button_time.clicked.connect(self.toggle_edit_mode_time)
        self.edit_button_time.move(500, 125)

        # Time Edit
        self.time_input = QTimeEdit(self)
        self.time_input.setStyleSheet(s.timeForm)
        self.time_input.resize(65, 30)
        self.time_input.move(200, 175)
        self.time_input.setEnabled(False)

        # Calling the getter function for reminder time
        time = self.get_reminder_time()
        self.time_input.setTime(time)

        # Prediksi Label Text
        label_prediksi = QLabel('Atur Rentang Prediksi', self)
        label_prediksi.setFont(f.H2)
        label_prediksi.setStyleSheet(s.h2)
        label_prediksi.move(200, 225)
        label_prediksi.resize(300, 30)

        # Calling getter function for the prediction range
        range = self.get_prediction_range()

        self.month_range_input = QLineEdit(self)
        validator = QIntValidator()
        self.month_range_input.setValidator(validator)
        self.month_range_input.move(200, 275)
        self.month_range_input.setStyleSheet(s.month_form)
        self.month_range_input.setEnabled(False)
        if range == -1:
            self.month_range_input.setPlaceholderText("BULAN")
        else:
            self.month_range_input.setPlaceholderText(str(range))

        # Edit Button Month
        self.edit_button_month = QPushButton("Edit", self)
        self.edit_button_month.setIcon(QIcon("img/icon/editred.png"))
        self.edit_button_month.setFont(f.radio_button_text)
        self.edit_button_month.setStyleSheet(s.edit_button)
        self.edit_button_month.clicked.connect(self.toggle_edit_mode_month)
        self.edit_button_month.move(500, 225)

    def update_prediction_range(self):
        """
        Update the prediction range in the field to the database
        """
        try:
            new_prediction_range = int(self.month_range_input.text())
        except:
            return
        update_prediction_range_query = QSqlQuery(DBConnection.get_instance())
        update_prediction_range_query.prepare(
            """
            UPDATE UserSetting SET PredictionRange = ?;
            """
        )
        update_prediction_range_query.addBindValue(new_prediction_range)
        update_prediction_range_query.exec()

    def update_reminder_time(self):
        """
        Update the reminder time in the field to the database
        """
        time = self.time_input.time().toString("hh:mm")
        update_reminder_time_query = QSqlQuery(DBConnection.get_instance())
        update_reminder_time_query.prepare(
            """
            UPDATE UserSetting SET ReminderTime = ?;
            """
        )
        update_reminder_time_query.addBindValue(time)
        update_reminder_time_query.exec()

    @staticmethod
    def get_reminder_time():
        """
        Get the reminder time from the database
        """
        get_reminder_time_query = QSqlQuery(DBConnection.get_instance())
        get_reminder_time_query.exec(
            """
            SELECT strftime('%H', ReminderTime), strftime('%M', ReminderTime)
            FROM (SELECT ReminderTime FROM UserSetting LIMIT 1) as RT;
            """
        )
        get_reminder_time_query.next()
        return QTime(int(get_reminder_time_query.value(0)), int(get_reminder_time_query.value(1)))

    def get_prediction_range(self):
        """
        Get the prediction range from the database
        """
        get_prediction_range_query = QSqlQuery(DBConnection.get_instance())
        get_prediction_range_query.exec(
            """
            SELECT PredictionRange
            FROM UserSetting
            LIMIT 1;
            """
        )
        if get_prediction_range_query.next():
            return get_prediction_range_query.value(0)
        return -1


    def initialize_setting(self):
        """
        Make a new initial row for the user settings table if there isn't any
        """
        is_empty_query = QSqlQuery(DBConnection.get_instance())
        is_empty_query.exec(
            """
            SELECT COUNT(*)
            FROM UserSetting
            """
        )
        is_empty_query.next()
        is_empty = is_empty_query.value(0) == 0

        if not is_empty:
            return

        initialize_settings_query = QSqlQuery(DBConnection.get_instance())
        initialize_settings_query.exec(
            """
            INSERT INTO UserSetting(PredictionRange, ReminderTime)
            VALUES(0, '00:00');
            """
        )

    def toggle_edit_mode_time(self):
        """
        This function sets the edit button for time input 
        """
        self.edit_mode_time = not self.edit_mode_time
        if self.edit_mode_time:
            self.time_input.setEnabled(True)
            self.edit_button_time.setText("Save")
        else:
            self.update_reminder_time()
            self.time_input.setTime(self.get_reminder_time())
            self.set_alarm(self)
            self.time_input.setEnabled(False)
            self.edit_button_time.setText("Edit")

    def toggle_edit_mode_month(self):
        """
        This function sets the edit button for month range input 
        """
        self.edit_mode_month = not self.edit_mode_month
        if self.edit_mode_month:
            self.month_range_input.setEnabled(True)
            self.edit_button_month.setText("Save")
        else:
            self.update_prediction_range()
            self.month_range_input.setPlaceholderText(
                str(self.get_prediction_range()))
            self.month_range_input.setEnabled(False)
            self.edit_button_month.setText("Edit")

    @staticmethod
    def set_alarm(page):
        """
        This function sets the alarm through the whole page 
        """
        prediction_time = prediction.PredictionManager()
        prediction_array = prediction_time.calculate_prediction()
        if len(prediction_time.prediction) == 0:
            return
        start_date = next(iter(prediction_array))
        # date_fake = QDate(2023, 4, 20)
        prediction_date = start_date
        date = prediction_date.addDays(-1)
        reminder_time = SettingsLayout.get_reminder_time()
        time = QTime(reminder_time.hour(), reminder_time.minute(), 0)
        prediction_date_and_time = QDateTime()
        prediction_date_and_time.setDate(date)
        prediction_date_and_time.setTime(time)
        if (prediction_date_and_time in page.alarm.array_date_time):
            return 
        page.alarm.timer.start()
        page.alarm.timer.add_alarm(prediction_date_and_time)
        page.alarm.array_date_time.append(prediction_date_and_time)
     
