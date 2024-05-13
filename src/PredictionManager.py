"""
prediction manager
"""
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
from Database import DBConnection


def get_last_mens():
    """
    Return the last menstrual cycle date
    """
    last_mens_query = QSqlQuery(DBConnection.get_instance())
    last_mens_query.exec(
        """
        SELECT strftime("%Y", EndDate) Year, strftime("%m", EndDate) Month, 
        strftime('%d', EndDate) Day
        FROM (SELECT (datetime(EndSec, 'unixepoch', 'localtime')) EndDate
        FROM (SELECT (strftime("%s",StartDate, '+'||Duration||' days')) EndSec, 
        Duration, StartDate
        FROM MenstrualCycle
        ORDER BY EndSec DESC
        LIMIT 1
        ) AS ProcessedEnd) AS ProcessedEnd2;
        """
    )
    if not last_mens_query.next():
        return None
    return QDate(int(last_mens_query.value(0)),
                 int(last_mens_query.value(1)), int(last_mens_query.value(2)))


def get_prediction_range():
    """
    Return the prediction range from user settings
    """
    prediction_range_query = QSqlQuery(DBConnection.get_instance())
    prediction_range_query.exec(
        """
        SELECT PredictionRange
        FROM UserSetting
        LIMIT 1;
        """
    )
    prediction_range_query.next()
    return prediction_range_query.value(0)


class PredictionManager():
    """
    PredictionManager class"""
    def __init__(self):
        self.prediction = []

    def calculate_prediction(self):
        """
        Calculate the prediction of the next menstrual cycle
        """
        last_mens_cycle = get_last_mens()
        month_range = get_prediction_range()

        if last_mens_cycle is None:
            return None
        mens_cycle_interval = 27
        self.prediction.clear()
        self.prediction.append(last_mens_cycle.addDays(mens_cycle_interval))
        max_month = last_mens_cycle.month() + month_range
        while self.prediction[len(self.prediction)-1].month() < max_month:
            self.prediction.append(
                self.prediction[len(self.prediction)-1].addDays(mens_cycle_interval))
            if self.prediction[len(self.prediction)-1].month() == 1:
                max_month = max_month % 12

        prediction_dict = {}
        for _, val in enumerate(self.prediction):
            key = val
            prediction_dict[key] = 7
        return prediction_dict

    def get_day_before_mens(self):
        """
        Return the number of days before the next menstrual cycle
        """
        current_date = QDate.currentDate()
        if len(self.prediction) == 0:
            return None
        else:
            for i in range(len(self.prediction)):
                if current_date <= self.prediction[i]:
                    return current_date.daysTo(self.prediction[i])
            return -1*self.prediction[i].daysTo(current_date)
    