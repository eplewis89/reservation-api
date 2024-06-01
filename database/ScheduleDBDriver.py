from database.DatabaseConnection import DatabaseConnection

class ScheduleDBDriver:
    def __init__(self, path) -> None:
        self.path = path
        self.connection = DatabaseConnection(path)

    def get_schedules(self):
        return self.connection.execute_fetch("SELECT * FROM schedules")
    
    def get_schedule(self, id):
        return self.connection.execute_fetch_one(f"SELECT * FROM schedules WHERE ScheduleID = {id}")
    
    def get_provider_schedule(self, id):
        return self.connection.execute_fetch(f"SELECT * FROM schedules WHERE ScheduleProvider = {id}")
    
    def create_schedule(self, data):
        sql = f"""INSERT INTO schedules
                (ScheduleStart,
                ScheduleEnd,
                ScheduleProvider)
            VALUES
                ('{data["ScheduleStart"]}',
                '{data["ScheduleEnd"]}',
                '{data["ScheduleProvider"]}')"""
        
        return self.connection.execute_commit(sql)
    
    def update_schedule(self, id, data):
        sql = f"""UPDATE schedules SET
                ScheduleStart = '{data["ScheduleStart"]}',
                ScheduleEnd = '{data["ScheduleEnd"]}',
                ScheduleProvider = '{data["ScheduleProvider"]}'
            WHERE
                ScheduleID = {id}"""
        
        return self.connection.execute_commit(sql)
    
    def delete_schedule(self, id):
        sql = f"""DELETE FROM schedules WHERE ScheduleID = {id}"""
        
        return self.connection.execute_commit(sql)