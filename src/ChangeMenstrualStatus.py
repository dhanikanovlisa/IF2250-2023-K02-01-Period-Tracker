"""
change menstrual status
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlQuery
from Notification import Alarm
import style.Font as f
import style.Style as s
import App as app
import Settings as settings
import Article as article
import Kalendar as kalendar
from Database import DBConnection


class MenstrualStatusForm(QMainWindow):
    """"
    Menstrual Status Form
    """
    def __init__(self, date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wdw = None
        self.setWindowTitle('Period Tracker')
        self.setWindowIcon(QIcon('img/icon/iconWindow.png'))
        self.setStyleSheet(s.bg_color)

        # Navigation Bar background
        label = QLabel(self)
        pixmap = QPixmap('img/navbar_bg.png')
        label.setPixmap(pixmap)
        self.selected_date = date
        self.new_date = self.selected_date
        self.new_interval = -1
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())
        self.navigation_bar()
        self.status_page_form()
        self.msg_box =""
        self.new_start_cycle=""
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

    def status_page_form(self):
        """
        Status Page Form
        """
        self.go_back_button = QPushButton(" Go Back", self)
        self.go_back_button.move(200, 10)
        self.go_back_button.setIcon(QIcon("img/icon/backarrow2.png"))
        self.go_back_button.setFont(f.button_text)
        self.go_back_button.resize(95, 30)
        self.go_back_button.setStyleSheet(s.go_back_button)
        self.go_back_button.clicked.connect(self.go_to_kalendar)

        # Ask for input corret menstrual cycle start date
        self.title = QLabel("Ubah Siklus Menstruasi Pada Bulan " + str(
            self.selected_date.month()) + " " + str(self.selected_date.year()), self)
        self.title.setFont(f.H1)
        self.title.setStyleSheet(s.h1)
        self.title.resize(1000, 50)
        self.title.move(200, 50)

        self.new_start_date = QLabel("Tanggal Mulai", self)
        self.new_start_date.setFont(f.paragraph)
        self.new_start_date.setStyleSheet(s.p)
        self.new_start_date.move(200, 150)

        self.new_interval = QLabel("Interval", self)
        self.new_interval.setFont(f.paragraph)
        self.new_interval.setStyleSheet(s.p)
        self.new_interval.move(350, 150)
        # Form Input Start Date For This Month
        self.edit_start_date = QLineEdit(self)
        validator = QIntValidator()
        self.edit_start_date.setValidator(validator)
        self.edit_start_date.move(200, 180)
        self.edit_start_date.setStyleSheet(s.date_form)
        self.edit_start_date.setEnabled(True)

        # Form Input Interval For This Month
        self.edit_interval = QLineEdit(self)
        validator = QIntValidator()
        self.edit_interval.setValidator(validator)
        self.edit_interval.move(350, 180)
        self.edit_interval.setStyleSheet(s.date_form)
        self.edit_interval.setEnabled(True)

        #Make dropdown whether to delete or add cycle
        self.delete_update = QComboBox(self)
        self.delete_update.addItem('Opsi')
        self.delete_update.addItem('Tambah Siklus')
        self.delete_update.addItem('Hapus Siklus')
        self.delete_update.setCurrentText('Pilih')
        self.delete_update.currentIndexChanged.connect(self.get_dropdown_info)
        self.delete_update.setStyleSheet(s.dropdown)
        self.delete_update.move(200, 100)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.move(200, 250)
        self.save_button.setFont(f.button_text)
        self.save_button.setStyleSheet(s.go_back_button)
        self.save_button.clicked.connect(self.save_input)

    def get_dropdown_info(self):
        """
        Get dropdown info
        """
        return self.delete_update.currentText()

    def insert_to_database(self):
        """
        Insert new menstrual cycle to database
        """
        if int(self.new_interval) <= 0:
            return False
        is_overlap_query = QSqlQuery(DBConnection.get_instance())
        is_overlap_query.prepare(
            """
            WITH InputDates AS (SELECT strftime('%s',?) 
            AS SecStartInput, strftime('%s',?, '+'||?||' day') AS SecEndInput)
            SELECT COUNT(*)
            FROM (
            SELECT strftime('%s',StartDate) SecStart, 
            strftime('%s',StartDate, '+'||Duration||' days') SecEnd, SecStartInput, SecEndInput
            FROM MenstrualCycle, InputDates
            )
            WHERE (SecStart <= SecStartInput AND SecEnd >= SecStartInput) OR 
            (SecStart <= SecEndInput AND SecEnd >= SecEndInput) OR (SecStart >= SecStartInput 
            AND SecEnd <= SecEndInput);
            """
        )

        is_overlap_query.addBindValue(self.new_date.toString("yyyy-MM-dd"))
        is_overlap_query.addBindValue(self.new_date.toString("yyyy-MM-dd"))
        is_overlap_query.addBindValue(str(self.new_interval))

        is_overlap_query.exec()
        is_overlap_query.next()
        is_overlap = is_overlap_query.value(0) > 0
        if is_overlap:
            return False

        insert_cycle_query = QSqlQuery(DBConnection.get_instance())
        insert_cycle_query.prepare(
            """
            INSERT INTO MenstrualCycle(StartDate, Duration)
            VALUES (? , ?);
            """
        )
        insert_cycle_query.addBindValue(self.new_date.toString("yyyy-MM-dd"))
        insert_cycle_query.addBindValue(int(self.new_interval))
        insert_cycle_query.exec()
        return True

    def delete_cycle(self, start_date: QDate, duration: int):
        """
        Delete cycles with the given date and duration
        """
        string_start_date = start_date.toString("yyyy-MM-dd")
        delete_cycle_query = QSqlQuery(DBConnection.get_instance())
        delete_cycle_query.prepare(
            """
            DELETE FROM MenstrualCycle
            WHERE StartDate == ? AND Duration == ?;
            """
        )

        delete_cycle_query.addBindValue(string_start_date)
        delete_cycle_query.addBindValue(duration)
        delete_cycle_query.exec()


    def save_input(self):
        """
        Save the input from the user to the database
        """
        self.new_start_cycle = self.edit_start_date.text()
        self.new_interval = self.edit_interval.text()
        days_month = self.selected_date.daysInMonth()
        get_month = self.selected_date.month()
        get_year = self.selected_date.year()
        self.msg_box = QMessageBox()
        self.msg_box.setFixedSize(500, 500)
        self.msg_box.setWindowTitle("Peringatan")
        self.msg_box.setDefaultButton(QMessageBox.Ok)
        get_current_index = self.get_dropdown_info()

        if self.new_start_cycle and self.new_interval:
            # If the input is a valid integer within the range, save to the database
            if (self.new_start_cycle.isdigit() and int(self.new_start_cycle) >= 1
            and int(self.new_start_cycle) < days_month):
                #Check the dropdown is it delete or add cycle
                if get_current_index == 'Hapus Siklus':
                    self.new_date = QDate(
                get_year, get_month, int(self.new_start_cycle))
                    self.new_interval = int(self.edit_interval.text())
                    self.delete_cycle(self.new_date, self.new_interval)
                    self.msg_box.setInformativeText(
                            "Berhasil menghapus siklus")
                    self.msg_box.exec_()
                elif get_current_index == 'Tambah Siklus':
                    # If the new start cycle input is the same as in the database
                    self.new_date = QDate(
                get_year, get_month, int(self.new_start_cycle))
                    self.new_interval = int(self.edit_interval.text())
                    if not self.insert_to_database():
                        self.msg_box.setInformativeText(
                            "Tidak bisa memasukan data karena siklus tidak mungkin terjadi")
                        self.msg_box.exec_()
                    else:
                        self.msg_box.setInformativeText(
                            "Berhasil mengubah siklus")
                        self.msg_box.exec_()
                else:
                    self.msg_box.setInformativeText(
                            "Anda belum memilih ingin menambah atau menghapus siklus")
                    self.msg_box.exec_()
            else:
                self.msg_box.setInformativeText(
                    "Tanggal berada di luar jangkauan bulan ini")
                self.msg_box.exec_()
        elif not self.new_start_cycle and not self.new_interval:
            self.msg_box.setInformativeText(
                "Anda mencoba menyimpan data dengan kedua form kosong")
            self.msg_box.exec_()
        elif not self.new_start_cycle and self.new_interval:
            self.msg_box.setInformativeText(
                "Form berisi tanggal mulai menstruasi kosong")
            self.msg_box.exec_()
        elif self.new_start_cycle and not self.new_interval:
            self.msg_box.setInformativeText(
                "Form berisi interval siklus menstruasi kosong")
            self.msg_box.exec_()
        settings.SettingsLayout.set_alarm(self)

    def go_to_home(self):
        """
        go to home page
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
        go to kalendar page
        """
        if self.wdw is None:
            self.wdw = kalendar.Kalendar()
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
        go to article page
        """
        if self.wdw is None:
            self.wdw = article.ArticleLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None
