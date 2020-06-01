from database import Database
from postgresDB import PostgresDB
from mongoDB import WorkListMV


exames_worklist = WorkListMV().get_exames_not_created()
estudos = PostgresDB.check_if_exists_on_radius(exames_worklist)

for estudo in estudos:
    PostgresDB.insert_on_db(estudo)
    WorkListMV.update_to_created(estudo.accessionnumber)
