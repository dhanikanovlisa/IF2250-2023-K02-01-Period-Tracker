from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from style import *

bg = '#F8F8F8'
bg_navbar = 'FFE7EC'
P1 = '#FFAEAD'
P2 = '#B1B0D8'
S1 = '9DBEE0'
text = '#193F65'

"""
Disini buat styling purpose, buat posisi dan set font diluars
"""

bg_color = """QMainWindow{
  background-color: #F8F8F8;
}"""

bg_color_widget = """QWidget{
  background-color: #F8F8F8;
}"""

h1_navbar = """QLabel{
    color: #193F65;
    background-color: #FFE7EC;
    font-size: 32px;
    font-weight: Bold;
}

"""

h1 = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 32px;
    font-weight: Bold;
}
"""
h1_settings = """QLabel{
    color: #193F65;
    background-color: transparent;
    font-size: 32px;
    font-weight: Bold;
}
"""

h2 = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 24px;
    font-weight: Bold;
}

"""
h1_welcome = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 64px;
    font-weight: Bold;
}"""

h1_navbar = """QLabel{
    color: #193F65;
    background-color: #FFE7EC;
    font-size: 32px;
    font-weight: Bold;
}

"""

p = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 10px;
}

"""
text = """QLabel{
            color: #193F65;
            background-color: #F8F8F8;
            font-size: 16px;
            font-weight: normal;
        }
"""
paragraph = """QLabel{
            color: #193F65;
            background-color: transparent;
            font-size:16px;
            font-weight: normal;
            text-align: left
            line-height: 1.5;
        }
"""
edit_button = """QPushButton{
                  color: #DE524D;
                  background-color: #F8F8F8;
                  font-size = 16px;
                  font-weight: normal;
                  border-radius: 5px;
                  text-align: left;
                  border-style: none;
              }
"""
button_small = """QPushButton{
            border-style: none;
            color: #193F65;
            background-color: #FFAEAD;
            border-radius: 5px;
            font-size: 14px;
          
          }
          QPushButton::hover{
            background-color: #B1B0D8;
          }
"""

edit_button = """QPushButton{
                  color: #DE524D;
                  background-color: #F8F8F8;
                  font-size = 16px;
                  font-weight: normal;
                  border-radius: 5px;
                  text-align: left;
                  border-style: none;
              }
"""
card_text = """QPushButton{
    color: #F8F8F8;
    background-color: transparent;
    font-size = 16px;
    font-weight: normal;
    text-align: left;
  }
  

"""
label_cycle = """QLabel{
    color: #193F65;
    background-color: #FFE7EC;
    font-size: 16px;
    font-weight: Bold;
    border-radius: 10px;
    padding:10px;

}
"""
button_card = """
          QPushButton{
            color: #FFE7EC;
            background-color: transparent;
            font-size: 24px;
            font-weight: Bold;
            text-align: left;
            border-style: none;
            border-radius: 5px;
          }
"""
card_frame = """
        QFrame {
            color: #FFE7EC;
            background-color: #9DBEE0;
            font-size: 24px;
            font-weight: Bold;
            text-align: left;
            border-style: none;
            border-radius: 5px;
        }
        QFrame::hover{
            background-color: #B1B0D8;
          }

"""

button_navbar = """
          QPushButton{
            border-style: none;
            color: #193F65;
            background-color: #FFE7EC;
            border-radius: 5px;
            font-weight: Bold;
            text-align: left;
          }
"""

button_normal = """
          QPushButton{
            border-style: none;
            color: #193F65;
            background-color: #FFAEAD;
            border-radius: 5px;
          }
          QPushButton::hover{
            background-color: #B1B0D8;
          }
"""

go_back_button = """
          QPushButton{
            background: #FFAEAD;
            border-radius: 5px;
            font-style: normal;
            font-weight: 700;
            font-size: 16px;
            line-height: 10px;
            color: #F8F8F8;
          }
          QPushButton::hover{
            background-color: #B1B0D8;
          }
"""

timeForm = """
          QTimeEdit{
            border-style: none;
            color: #FFAEAD;
            background-color: #FFE7EC;
            border: 2px solid #FFAEAD;
            border-radius: 10px;
            font-style: normal;
            font-weight: 700;
            line-height: 40px;
          }
"""


time_form = """
          QSpinBox{
            border-style: none;
            color: #193F65;
            background-color: #FFE7EC;
            border: 2px solid #FFAEAD;
            border-radius: 10px;
          }
"""

date_form = """QLineEdit{
            width: 500px;
            height: 200px;
            border-style: none;
            color: #FFAEAD;
            background-color: #FFE7EC;
            border: 1px solid #FFAEAD;
            border-radius: 7px;
            font-style: normal;
            font-weight: 700;
            line-height: 40px;
          }

"""
month_form = """
          QLineEdit{
            width: 241px;
            height: 74px;
            border-style: none;
            color: #FFAEAD;
            background-color: #FFE7EC;
            border: 2px solid #FFAEAD;
            border-radius: 10px;
            font-style: normal;
            font-weight: 700;
            line-height: 40px;
          }
""" 

shadow_purple_md = QGraphicsDropShadowEffect(blurRadius=5, offset=QPointF(2.0, 4.0),color=QColor(177,176,216,100))
shadow_purple_lg = QGraphicsDropShadowEffect(blurRadius=10, offset=QPointF(2.0, 6.0),color=QColor(177,176,216,100))

calendar = """QCalendarWidget QToolButton {
          color: #193F65;
          font-size: 20px;
          icon-size: 28px, 28px;
          
        }
        QCalendarWidget QMenu {
          width: 150px;
          font-size = 20px;
          left: 20px;
          color: #F8F8F8;
          background-color: #b1b0d8;
          border-radius: 10px;
        }
        QCalendarWidget QSpinBox { 
          width: 50px; 
          color: #193F65; 
          background-color: #F8F8F8;
          selection-background-color: #b1b0d8;
          selection-color: #193F65;
        }
        QCalendarWidget QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right;  width:30px; }
        QCalendarWidget QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right;  width:30px;}
        QCalendarWidget QSpinBox::up-arrow { width:20px;  height:20px; }
        QCalendarWidget QSpinBox::down-arrow { width:20px;  height:20px; }
        
        /* header row */
        QCalendarWidget QWidget { alternate-background-color: #FFE7EC; }
        
        /* normal days */
        QCalendarWidget QAbstractItemView:enabled 
        {
          color: #193F65;  
          background-color: #FFF;  
          selection-background-color: #b1b0d8; 
          selection-color: #F8F8F8; 
        }
        
        /* days in other months */
        /* navigation bar */
        QCalendarWidget QWidget#qt_calendar_navigationbar
        { 
            color: #193F65;
              background-color: #FFE7EC;
              border:2px solid #FFE7EC;
              border-bottom: 0px;
              border-top-left-radius: 5px;
              border-top-right-radius: 5px;
        }
        QCalendarWidget QWidget#qt_calendar_prevmonth, QWidget#qt_calendar_nextmonth{
              border:none;
              qproperty-icon:none;
              
              min-width:20px;
              max-width:20px;
              min-height:20px;
              max-height:20px;
              
              border-radius:5px;
              background-color:transparent;
              padding:5px;
            }
          QCalendarWidget QWidget#qt_calendar_prevmonth{
            qproperty-icon:url("img/arrow_kiri.png");
          }
          
          QCalendarWidget QWidget#qt_calendar_prevmonth:hover{
            background-color: #B1B0D8;
          }
          QCalendarWidget QWidget#qt_calendar_nextmonth{
            qproperty-icon:url("img/arrow_kanan.png");
          }
          
          
          QCalendarWidget QWidget#qt_calendar_nextmonth:hover{
            background-color: #B1B0D8;
          }
          
          QCalendarWidget QWidget#qt_calendar_yearbutton{
            color:#000;
            margin:5px;
            border-radius: 5px;
            font-size: 16px;
            padding: 0 10px;
          }
          
          QCalendarWidget QWidget#qt_calendar_monthbutton{
            width:150px;
            color:#193F65;
            font-size: 24px;
            border-radius: 5px;
            text-align:center;
          }
          
          QCalendarWidget QWidget#qt_calendar_monthbutton:hover{
           background-color: #B1B0D8;
          }
          
          QCalendarWidget QWidget#qt_calendar_yearbutton{
            width:100px;
            height: 30px;
            color:#193F65;
            font-size: 24px;
            border-radius: 5px;
            text-align:center;
          }
          
          QCalendarWidget QWidget#qt_calendar_yearbutton:hover{
            background-color: #B1B0D8;
          }
          
          QCalendarWidget QWidget#qt_calendar_yearedit{
            color: #193F65;
            height: 200px;
            width: 80px;
            background: #FFF;
            font-size: 20px;
            
          }

"""
          
scroll_area = """
          QScrollArea {
            border: none;
            background-color: #F8F8F8;
          }
"""

reminder_msg = """
          QMessageBox {
            border-style: none;
            color: #FFAEAD;
            background-color: #FFE7EC;
          }
          QMessageBox QLabel {
            color: #FFAEAD;
            background-color: #FFE7EC;
            font-weight: 700;
            text-align: center;
          }
"""
sfgroupbox = """QGroupBox{
            font-size: 13px;
            border:none;
            background: #F8F8F8;
            color: #193F65;
            font-weight: Bold;
          }

"""

s_fradiobutton = """QRadioButton{
            background: #F8F8F8;
            color: #193F65;
          }

"""

text_field = """QTextEdit{
            border-radius: 5px;
            border: 1px solid #FFAEAD;
            padding: 8px 8px;
            background-color: #FFE7EC;
            color: #FFAEAD;
          }
          QLineEdit:focus {
            border: 2px solid #FFAEAD;
          }

"""
h3 = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 13px;
    font-weight: Bold;
}

"""

p = """QLabel{
    color: #193F65;
    background-color: #F8F8F8;
    font-size: 10px;
}
"""

progress_bar = """QProgressBar{
                background-color: #FFF;
                color: #193F65;
                border-style: none;
                border-radius: 5px;
                text-align: center;
                font-size: 14px;
                }
                QProgressBar::chunk{
                  background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(232, 214, 255, 255), stop:1 rgba(157, 190, 224, 255));
                  border-radius: 5px;
                  border-style: none;
                }
"""

dropdown = """QComboBox {
                background-color: #FFE7EC;
                color: #193F65;
                border: 1px solid #FFAEAD;
                padding: 5px;
                border-radius: 5px;
            }


            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
                background-color:  #FFE7EC;
                color: #193F65;
            }
"""