from database.DatabaseConnection import DatabaseConnection

from database.ProviderDBDriver import ProviderDBDriver
from database.ScheduleDBDriver import ScheduleDBDriver
from database.ReservationDBDriver import ReservationDBDriver

db_name = "testdatabase.db"
DatabaseConnection(db_name).create_database()

prov_data = {
    "ProviderName": "test provider",
    "ProviderEmail": "test@email.com",
    "ProviderPhone": "123-123-1234"
}

def test_provider(prov):
    # create
    id = prov.create_new_provider(prov_data)

    # retrieve all
    providers = prov.get_all_providers()
    print(providers)
    
    # update
    prov_data["ProviderName"] = "updated provider"
    id = prov.update_provider(id, prov_data)

    # retrieve updated
    provider = prov.get_provider_by_id(id)
    print(provider)

    # delete
    prov.delete_provider(id)

    # retrieve
    provider = prov.get_all_providers()
    print(provider)

def test_schedule(prov, sched):
    # create
    prov_data["ProviderName"] = "Dr. Available"
    id = prov.create_new_provider(prov_data)

def run_tests():
    prov = ProviderDBDriver(db_name)
    sched = ScheduleDBDriver(db_name)
    res = ReservationDBDriver(db_name)

    test_provider(prov)
    test_schedule(prov, sched)
