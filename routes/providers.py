from flask_restful import Resource
from flask import request

from config.configuration import Configuration
from database.ProviderDBDriver import ProviderDBDriver

class ProviderList(Resource):
    def __init__(self):
        self.provider_driver = ProviderDBDriver(Configuration().get_path())

    def get(self):
        return self.provider_driver.get_providers()
    
    def post(self):
        self.provider_driver.create_provider(request.json)

        return { "status": 200, "message": "provider created" }

class Provider(Resource):
    def __init__(self):
        self.provider_driver = ProviderDBDriver(Configuration().get_path())

    def get(self, id):
        return self.provider_driver.get_provider(id)
    
    def put(self, id):
        self.provider_driver.update_provider(id, request.json)

        return { "status": 200, "message": "provider updated" }
    
    def delete(self, id):
        self.provider_driver.delete_provider(id)

        return { "status": 200, "message": "provider deleted" }
