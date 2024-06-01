from flask_restful import Resource
from flask import request
from datetime import datetime

from config.configuration import Configuration
from database.ScheduleDBDriver import ScheduleDBDriver

class ScheduleList(Resource):
    def __init__(self):
        self.schedule_driver = ScheduleDBDriver(Configuration().get_path())
        self.time_format = "%Y-%m-%dT%H:%M:%S"

    def get(self):
        return self.schedule_driver.get_schedules()
    
    def post(self):
        s_time_start = datetime.strptime(request.json["ScheduleStart"], self.time_format)
        s_time_end = datetime.strptime(request.json["ScheduleEnd"], self.time_format)

        if s_time_start < s_time_end:
            self.schedule_driver.create_schedule(request.json)
            message = "schedule added"
        else:
            message = "start time has to become before end time"

        return { "status": 200, "message": message }

class Schedule(Resource):
    def __init__(self):
        self.schedule_driver = ScheduleDBDriver(Configuration().get_path())

    def get(self, id):
        return self.schedule_driver.get_schedule(id)
    
    def put(self, id):
        self.schedule_driver.update_schedule(id, request.json)

        return { "status": 200, "message": "schedule updated" }
    
    def delete(self, id):
        self.schedule_driver.delete_schedule(id)

        return { "status": 200, "message": "schedule deleted" }
