import json
import sqlite3


class DatabaseConnection:
    # initialization
    def __init__(self, path) -> None:
        self.path = path
        self.connection = None
        self.cursor = None

        self.connect()
    
    def dict_factory(self, cursor, row):
        data = {}

        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]

        return data
    
    # connection to database
    def connect(self) -> bool:
        try:
            self.connection = sqlite3.connect(self.path)
            self.connection.row_factory = self.dict_factory
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print("Couldn't connect to the database; is the path correct? Error: {e}")
            return False
    
    # close database
    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except sqlite3.Error as e:
            print("Couldn't disconnect the database; is it connected? Error: {e}")
    
    # execute a sql command and do not return any results
    def execute_commit(self, sql):
        if (self.connect):
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid
    
    # database query and fetch results
    def execute_fetch(self, sql):
        if (self.connect):
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
    
    # database query and fetch one result
    def execute_fetch_one(self, sql):
        if (self.connect):
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
    
    # database standup
    def create_database(self):
        self.create_providers()
        self.create_schedule()
        self.create_reservations()

    def create_providers(self):
        sql = """CREATE TABLE IF NOT EXISTS providers (
            ProviderID INTEGER PRIMARY KEY, 
            ProviderName TEXT, 
            ProviderEmail TEXT, 
            ProviderPhone TEXT)"""
        
        self.execute_commit(sql)

    def create_schedule(self):
        sql = """CREATE TABLE IF NOT EXISTS schedules (
            ScheduleID INTEGER PRIMARY KEY,
            ScheduleStart TEXT,
            ScheduleEnd TEXT,
            ScheduleProvider INTEGER,
            FOREIGN KEY (ScheduleProvider) REFERENCES providers(ProviderID))"""
        
        self.execute_commit(sql)

    def create_reservations(self):
        sql = """CREATE TABLE IF NOT EXISTS reservations (
            ReservationID INTEGER PRIMARY KEY, 
            ClientName TEXT,
            ClientPhone TEXT,
            ClientEmail TEXT,
            ReservationTime TEXT,
            ReservationTimeInserted TEXT,
            ReservationConfirmed BOOLEAN NOT NULL CHECK (ReservationConfirmed IN (0, 1)),
            ReservationProvider INTEGER,
            FOREIGN KEY (ReservationProvider) REFERENCES providers(ProviderID))"""
        
        self.execute_commit(sql)

    # database teardown
    def delete_tables(self):
        tables = self.execute_fetch("SELECT name FROM sqlite_schema WHERE type='table';")

        for table in tables:
            sql = f"DROP TABLE {table}"
            self.execute_commit(sql)

        self.close()
