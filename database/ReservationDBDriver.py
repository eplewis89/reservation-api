from datetime import datetime
from database.DatabaseConnection import DatabaseConnection

class ReservationDBDriver:
    def __init__(self, path) -> None:
        self.path = path
        self.connection = DatabaseConnection(path)

    def get_reservations(self):
        return self.connection.execute_fetch("SELECT * FROM reservations")
    
    def get_reservation(self, id):
        return self.connection.execute_fetch_one(f"SELECT * FROM reservations where ReservationID = {id}")
    
    def create_reservation(self, data):
        sql = f"""INSERT INTO reservations
                (ClientName,
                ClientPhone,
                ClientEmail,
                ReservationTime,
                ReservationTimeInserted,
                ReservationConfirmed,
                ReservationProvider)
            VALUES
                ('{data["ClientName"]}',
                '{data["ClientPhone"]}',
                '{data["ClientEmail"]}',
                '{data["ReservationTime"]}',
                '{datetime.now().isoformat()}',
                0,
                '{data["ReservationProvider"]}')"""
        
        return self.connection.execute_commit(sql)
    
    def update_reservation(self, id, data):
        sql = f"""UPDATE reservations SET
            ReservationConfirmed = 1
        WHERE
            ReservationID = {id}"""
        
        return self.connection.execute_commit(sql)
    
    def delete_reservation(self, id):
        sql = f"""DELETE FROM reservations WHERE ReservationID = {id}"""
        
        return self.connection.execute_commit(sql)