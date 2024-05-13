""" SymptomForms module """
from copy import deepcopy
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
from defaults import symptom_custom, symptoms


class SymptomForms(QMainWindow):
    """ Class  SymptomForms"""
    def __init__(self, date:QDate, *args, **kwargs):
        """
        Constructor
        """
        super().__init__(*args, **kwargs)
        # Temporary Data
        self.symptoms_built_in_default = deepcopy(symptoms)
        self.symptoms_built_in = deepcopy(self.symptoms_built_in_default)

        self.symptom_custom = symptom_custom.copy()
        self.symptom_group_boxes = []

        self.date = date.toString("yyyy-MM-dd")
        self.wdw = None
        self.setWindowTitle('Period Tracker')
        self.setWindowIcon(QIcon('./img/icon/iconWindow.png'))
        self.setStyleSheet(s.bg_color)
        self.input_sym_type = ""
        self.input_sym_desc = ""
        # Navigation Bar background
        label = QLabel(self)
        pixmap = QPixmap('img/navbar_bg.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())
        self.navigation_bar()
        self.fetch_from_database()
        self.symptom_forms()
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

    def display_data(self):
        """
        Displaying data
        """
        merged_symptom = self.symptoms_built_in + [self.symptom_custom]
        for i, symptom_group_box in enumerate(self.symptom_group_boxes):
            for button in symptom_group_box.findChildren(QRadioButton):
                if button.text() == str(merged_symptom[i]["rate"]):
                    button.setChecked(True)
                    break
        self.input_sym_type.setText(self.symptom_custom["name"])
        self.input_sym_desc.setText(self.symptom_custom["desc"])

    def sf_group_box(self, sym_type, pos_y):
        """
        Method for generating group box
        """
        groupbox = QGroupBox(sym_type, self)
        hbox = QHBoxLayout()
        groupbox.setFlat(True)
        groupbox.move(200, pos_y)
        groupbox.resize(400, 70)
        groupbox.setLayout(hbox)
        groupbox.setStyleSheet(s.sfgroupbox)

        for i in range(0, 6):
            radiobutton = QRadioButton(str(i), self)
            radiobutton.setStyleSheet(s.s_fradiobutton)
            hbox.addWidget(radiobutton)
        return groupbox

    def symptom_forms(self):
        """
        Method for generating symptom
        """
        button_back = QPushButton('< Go Back', self)
        button_back.move(200, 30)
        button_back.setStyleSheet(s.button_normal)
        button_back.clicked.connect(self.go_to_kalendar)

        self.symptom_group_boxes = [self.sf_group_box(
            symptom["name"], 80 + i * 70) for i, symptom in enumerate(
                self.symptoms_built_in + [
                    {"name": "Gejala Lain", "rate": self.symptom_custom["rate"]}])]
        # self.kram_perut_gb = self.sfGroupBox("KRAM PERUT", 80)
        # self.blood_flow_gb = self.sfGroupBox("BLOOD FLOW", 150)
        # self.mood_gb = self.sfGroupBox("MOOD", 220)
        # self.intensitas_olahraga_gb = self.sfGroupBox(
        #     "INTENSITAS OLAHRAGA", 290)
        # self.gejala_lain_gb = self.sfGroupBox("GEJALA LAIN", 360)

        label_sym_type = QLabel("Nama Gejala", self)
        label_sym_type.setStyleSheet(s.p)
        label_sym_type.move(205, 480)
        self.input_sym_type = QTextEdit(self)
        self.input_sym_type .setFixedHeight(40)
        self.input_sym_type .setFixedWidth(100)
        self.input_sym_type .setPlaceholderText("Text Field")
        self.input_sym_type .move(205, 510)
        self.input_sym_type .setStyleSheet(s.text_field)

        label_sym_desc = QLabel("Deskripsi", self)
        label_sym_desc.setStyleSheet(s.p)
        label_sym_desc.move(205, 550)
        self.input_sym_desc = QTextEdit(self)
        self.input_sym_desc.setPlaceholderText("Text Field")
        self.input_sym_desc.setFixedHeight(100)
        self.input_sym_desc.setFixedWidth(300)
        self.input_sym_desc.setAlignment(Qt.AlignTop)
        self.input_sym_desc.move(205, 580)
        self.input_sym_desc.setStyleSheet(s.text_field)

        button_done = QPushButton('Done', self)
        button_done.move(205, 690)
        button_done.setStyleSheet(s.button_normal)
        button_done.clicked.connect(self.get_selected_value)
        button_done.clicked.connect(self.go_to_kalendar)
        self.display_data()

    def get_selected_value(self):
        """
        Method to get selected value
        """
        selected_button = None
        for i, symptom_group_box in enumerate(self.symptom_group_boxes):
            if i >= 5:
                break
            for button in symptom_group_box.findChildren(QRadioButton):
                if button.isChecked():
                    selected_button = button
                    break

            if selected_button:
                self.symptoms_built_in[i]["rate"] = selected_button.text()
        for button in self.symptom_group_boxes[5].findChildren(QRadioButton):
            if button.isChecked():
                selected_button = button
                break

        if selected_button:
            self.symptom_custom["rate"] = selected_button.text()
        self.symptom_custom["name"] = self.input_sym_type.toPlainText()

        self.symptom_custom["desc"] = self.input_sym_desc.toPlainText()
        self.submit_to_database()

    def submit_to_database(self):
        """
        Method to submit to database
        """
        update_built_in_symptoms = QSqlQuery(DBConnection.get_instance())
        update_built_in_symptoms.prepare(
            """
            INSERT INTO MenstrualSymptoms
            VALUES (?, ?, 1, NULL, ?)
            ON CONFLICT (Date, Name, BuiltIn) DO UPDATE SET
                Rate = excluded.Rate;
            """
        )
        update_built_in_symptoms.addBindValue(
            [self.date for _ in enumerate(self.symptoms_built_in)])
        update_built_in_symptoms.addBindValue(
            [symptom["name"] for _, symptom in enumerate(self.symptoms_built_in)])
        update_built_in_symptoms.addBindValue(
            [symptom["rate"] for _, symptom in enumerate(self.symptoms_built_in)])
        update_built_in_symptoms.execBatch()

        update_custom_symptoms = QSqlQuery(DBConnection.get_instance())
        update_custom_symptoms.prepare(
            """
            INSERT INTO MenstrualSymptoms
            VALUES (?, ?, 0, ?, ?)
            ON CONFLICT (Date, Name, BuiltIn) DO UPDATE SET
                Desc = excluded.Desc,
                Rate = excluded.Rate;
            """
        )
        update_custom_symptoms.addBindValue(self.date)
        update_custom_symptoms.addBindValue(self.symptom_custom["name"])
        update_custom_symptoms.addBindValue(self.symptom_custom["desc"])
        update_custom_symptoms.addBindValue(self.symptom_custom["rate"])

        update_custom_symptoms.exec()

    def fetch_from_database(self):
        """
        Method to fetch from database
        """
        get_builtin_symptoms = QSqlQuery(DBConnection.get_instance())
        get_builtin_symptoms.prepare(
            """
            SELECT Name, Rate
            FROM MenstrualSymptoms
            WHERE BuiltIn == 1 AND Date == ?;
            """
        )
        get_builtin_symptoms.addBindValue(self.date)
        get_builtin_symptoms.exec()
        symptoms_built_in_temp = []
        while get_builtin_symptoms.next():
            symptoms_built_in_temp.append(
                {"name": get_builtin_symptoms.value(0), "rate": get_builtin_symptoms.value(1)})
        if len(symptoms_built_in_temp) > 0:
            self.symptoms_built_in = symptoms_built_in_temp.copy()

        get_custom_symptoms = QSqlQuery(DBConnection.get_instance())
        get_custom_symptoms.prepare(
            """
            SELECT Name, Desc, Rate
            FROM MenstrualSymptoms
            WHERE BuiltIn == 0 AND Date == ?
            LIMIT 1;
            """
        )
        get_custom_symptoms.addBindValue(self.date)
        get_custom_symptoms.exec()

        symptoms_custom_temp = []
        while get_custom_symptoms.next():
            symptoms_custom_temp.append({"name": get_custom_symptoms.value(
                0), "desc": get_custom_symptoms.value(1), "rate": get_custom_symptoms.value(2), })
        if len(symptoms_custom_temp) > 0:
            self.symptom_custom = symptoms_custom_temp[0]

    def go_to_kalendar(self):
        """ Go to calendar """
        if self.wdw is None:
            self.wdw = kalendar.Kalendar()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_home(self):
        """ Go to home """
        if self.wdw is None:
            self.wdw = app.MainWindow()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_settings(self):
        """ Go to settings """
        if self.wdw is None:
            self.wdw = settings.SettingsLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None

    def go_to_article(self):
        """ Go to article """
        if self.wdw is None:
            self.wdw = article.ArticleLayout()
            self.wdw.showMaximized()
            self.close()

        else:
            self.wdw.close()  # Close window.
            self.wdw = None
