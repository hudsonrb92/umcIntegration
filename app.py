from database import Database
from postgresDB import PostgresDB
from mongoDB import WorkListMV

Database.initialize(user="postgres", database="nimbus_taas",
                    port="5432", host="localhost")


exames_worklist = WorkListMV().get_exames_not_created()
estudos = PostgresDB.check_if_exists_on_radius(exames_worklist)

for estudo in estudos:
    print(estudos.to_json())
    PostgresDB.insert_on_db(estudo)
    WorkListMV.update_to_created(estudo.accessionnumber)

Database.close_all_connections()
