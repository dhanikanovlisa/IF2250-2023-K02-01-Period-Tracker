"""
database
"""
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DBConnection:
    """
    Singleton class representing the connection to the database
    """
    _conn: QSqlDatabase = None

    def __init__(self) -> None:
        # Initializing connection
        DBConnection._conn = QSqlDatabase.addDatabase("QSQLITE")
        DBConnection._conn.setDatabaseName("./db.sqlite")
        DBConnection._conn.open()

        # Initialize the tables
        create_settings_table_query = QSqlQuery(DBConnection._conn)
        create_settings_table_query.exec(
            """
            CREATE TABLE IF NOT EXISTS UserSetting (
                PredictionRange INTEGER NOT NULL,
                ReminderTime text
            );
            """
        )

        create_articles_table_query = QSqlQuery(DBConnection._conn)
        create_articles_table_query.exec(
            """
            CREATE TABLE IF NOT EXISTS Articles (
                IDArticle INTEGER PRIMARY KEY,
                Title text NOT NULL,
                Summary text NOT NULL,
                Content text NOT NULL
            );
            """
        )

        create_mens_table_cycle_query = QSqlQuery(DBConnection._conn)
        create_mens_table_cycle_query.exec(
            """
            CREATE TABLE IF NOT EXISTS MenstrualCycle (
                IDCycle INTEGER PRIMARY KEY,
                StartDate text NOT NULL,
                Duration INTEGER NOT NULL
            );
            """
        )

        create_mens_table_symptom_query = QSqlQuery(DBConnection._conn)
        create_mens_table_symptom_query.exec(
            """
            CREATE TABLE IF NOT EXISTS MenstrualSymptoms (
                Date text NOT NULL,
                Name text NOT NULL,
                BuiltIn INTEGER,
                Desc text,
                Rate INTEGER,
                PRIMARY KEY (Date, Name, BuiltIn)
            );
            """
        )

        is_setting_empty_query = QSqlQuery(DBConnection.get_instance())
        is_setting_empty_query.exec(
            """
            SELECT COUNT(*)
            FROM UserSetting;
            """
        )
        is_setting_empty_query.next()
        is_empty = is_setting_empty_query.value(0) == 0

        if not is_empty:
            return

        initialize_settings_query = QSqlQuery(DBConnection.get_instance())
        initialize_settings_query.exec(
            """
            INSERT INTO UserSetting(PredictionRange, ReminderTime)
            VALUES(0, '00:00');
            """
        )

        # insert_articles_query = QSqlQuery(DBConnection._conn)
        # print("Inserting mock articles", insert_articles_query.exec(
        #     """
        #     INSERT INTO Articles VALUES (NULL, "Article 0", "Summary 0", "Content 0");
        #     """
        # ))
        # print(insert_articles_query.lastError().databaseText())

    @staticmethod
    def delete_connection():
        """
        Close the connection in the instance. Should only be called when the application is exiting
        """
        DBConnection._conn.close()

    @staticmethod
    def get_instance():
        """
        Return a connection object that connects to the database used in the application
        """
        if DBConnection._conn is None:
            DBConnection()
        return DBConnection._conn
