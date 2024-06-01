from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta

from config.configuration import Configuration
from database.ScheduleDBDriver import ScheduleDBDriver
from database.ReservationDBDriver import ReservationDBDriver

class ReservationList(Resource):
    def __init__(self):
        self.schedule_driver = ScheduleDBDriver(Configuration().get_path())
        self.reservation_driver = ReservationDBDriver(Configuration().get_path())
        self.time_format = "%Y-%m-%dT%H:%M:%S"

    def get(self):
        return self.reservation_driver.get_reservations()
    
    def post(self):
        message = ""
        can_schedule = False
        now = datetime.now()
        res_time = datetime.strptime(request.json["ReservationTime"], self.time_format)

        if res_time - now < timedelta(days=1):
            return { "status": 200, "message": "cannot schedule an appoinment less than 24 hours in advance" }

        reservations = self.reservation_driver.get_reservations()

        for res in reservations:
            r_time = datetime.strptime(res["ReservationTime"], self.time_format)
            delta = timedelta()
            
            # compute whether or not there's an appointment before or after
            if res_time < r_time:
                delta = r_time - res_time
            else:
                delta = res_time - r_time

            if delta < timedelta(minutes=15):
                return { "status": 200, "message": "reservation cannot be scheduled due to conflicting appointment" }

        schedules = self.schedule_driver.get_provider_schedule(request.json["ReservationProvider"])

        if message == "":
            for schedule in schedules:
                s_time_start = datetime.strptime(schedule["ScheduleStart"], self.time_format)
                s_time_end = datetime.strptime(schedule["ScheduleEnd"], self.time_format)
                
                if s_time_start < res_time < s_time_end:
                    can_schedule = True
                    break

        if can_schedule:
            self.reservation_driver.create_reservation(request.json)
            message = "reservation created successfully"
        else:
            message = "provider unavailable to take appointment"
        
        return { "status": 200, "message": message }

class Reservation(Resource):
    def __init__(self):
        self.reservation_driver = ReservationDBDriver(Configuration().get_path())
        self.time_format = "%Y-%m-%dT%H:%M:%S"

    def get(self, id):
        return self.reservation_driver.get_reservation(id)
    
    def put(self, id):
        reservation = self.get(id)

        now = datetime.now()
        res_time = reservation["ReservationTimeInserted"].split('.')[0]
        req_time = datetime.strptime(res_time, self.time_format)

        if now - req_time > timedelta(minutes=30):
            self.delete(id)
            message = "requested reservation expired"
        else:
            self.reservation_driver.update_reservation(id, request.json)
            message = "reservation confirmed"

        return { "status": 200, "message": message }
    
    def delete(self, id):
        self.reservation_driver.delete_reservation(id)

        return { "status": 200, "message": "reservation deleted" }
