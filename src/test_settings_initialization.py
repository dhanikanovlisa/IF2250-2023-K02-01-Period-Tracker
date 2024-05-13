"""
Test getting latest menstrual cycle
"""
import pytest
from Database import DBConnection
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlQuery, QSqlDatabase


# @pytest.fixture
# def initialize_database():
#     """
#     Get the database instance
#     """
#     return DBConnection.get_instance()


def test_prediction_range_initialization():
    """
    Check if the prediction range is initialized with 0
    """
    get_prediction_range_query = QSqlQuery(DBConnection.get_instance())
    get_prediction_range_query.exec(
        """
        SELECT PredictionRange
        FROM UserSetting
        LIMIT 1;
        """
    )

    get_prediction_range_query.next()

    assert get_prediction_range_query.value(0) == 0


def test_alarm_time_initialization():
    """
    Initialize alarm test
    """
    get_alarm_time_query = QSqlQuery(DBConnection.get_instance())
    get_alarm_time_query.exec(
        """
        SELECT strftime("%M", ReminderTime), strftime("%H", ReminderTime)
        FROM UserSetting
        LIMIT 1;
        """
    )

    get_alarm_time_query.next()

    assert get_alarm_time_query.value(
        0) == '00' and get_alarm_time_query.value(1) == '00'
