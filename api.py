from flask import Flask, render_template
from flask_restful import Api
from swagger_ui import api_doc

from config.configuration import Configuration
from database.DatabaseConnection import DatabaseConnection

from routes.providers import ProviderList, Provider
from routes.reservations import ReservationList, Reservation
from routes.schedules import ScheduleList, Schedule

application = Flask(__name__, template_folder="templates")

api_doc(application, config_path='./docs/api_spec.yml', url_prefix='/apidocs', title='API Documentation')

api = Api(application)

api.add_resource(ProviderList, "/api/providers")
api.add_resource(Provider, "/api/providers/<int:id>")

api.add_resource(ReservationList, "/api/reservations")
api.add_resource(Reservation, "/api/reservations/<int:id>")

api.add_resource(ScheduleList, "/api/schedules")
api.add_resource(Schedule, "/api/schedules/<int:id>")

@application.route('/')
def home():
    return render_template('home.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    try:
        DatabaseConnection(Configuration().get_path()).create_database()

        application.run(threaded=True, host='0.0.0.0')
    except:
        print("exited with an exception")
    finally:
        DatabaseConnection(Configuration().get_path()).close()
