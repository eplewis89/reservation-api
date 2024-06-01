from database.DatabaseConnection import DatabaseConnection

class ProviderDBDriver:
    def __init__(self, path) -> None:
        self.path = path
        self.connection = DatabaseConnection(path)

    def get_providers(self):
        rows = self.connection.execute_fetch("SELECT * FROM providers")

        for row in rows:
            schedules = self.connection.execute_fetch(f"""SELECT * FROM schedules WHERE ScheduleProvider = {row["ProviderID"]}""")
            reservations = self.connection.execute_fetch(f"""SELECT * FROM reservations WHERE ReservationProvider = {row["ProviderID"]}""")

            row["ProviderSchedule"] = schedules
            row["ProviderReservations"] = reservations

        return rows
    
    def get_provider(self, id):
        return self.connection.execute_fetch_one(f"""SELECT * FROM providers WHERE ProviderID = {id}""")
    
    def create_provider(self, data):
        sql = f"""INSERT INTO providers
                (ProviderName,
                ProviderEmail,
                ProviderPhone)
            VALUES
                ('{data["ProviderName"]}',
                '{data["ProviderEmail"]}',
                '{data["ProviderPhone"]}')"""
        
        return self.connection.execute_commit(sql)
    
    def update_provider(self, id, data):
        sql = f"""UPDATE providers SET
                ProviderEmail = '{data["ProviderEmail"]}',
                ProviderPhone = '{data["ProviderPhone"]}'
            WHERE
                ProviderID = {id}"""
        
        return self.connection.execute_commit(sql)
    
    def delete_provider(self, id):
        sql = f"""DELETE FROM providers WHERE ProviderID = {id}"""
        
        return self.connection.execute_commit(sql)