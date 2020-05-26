from database import CursorFromConnectionFromPool
from datetime import datetime
from estudo_dicom import EstudoDicom
from mongoDB import WorkListMV
import psycopg2


class PostgresDB:

    @classmethod
    def check_if_exists_on_radius(cls, lista_de_exames):
        estudo_criados = []
        with CursorFromConnectionFromPool() as cursor:
            for estudo in lista_de_exames:
                cursor.execute(f"""
                select * from radius_taas.estudo_dicom where accessionnumber='{estudo['accessionnumber']}'
                """)
                exame = cursor.fetchone()

                # Caso exame não exista na tabela estudo Dicom cria-lo
                if exame is None:

                    accessionnumber = estudo['accessionnumber']
                    patientname = estudo['paciente_nome']
                    patientid = estudo['paciente_id']
                    patientsex = estudo['paciente_sexo']
                    studyid = estudo['item_exame_id']
                    studyinstanceuid = estudo['studyinstanceuid']
                    studydescription = estudo['procedimento_nome']
                    modalitiesinstudy = estudo['procedimento_modalidade']
                    # CAMPOS FIXOS
                    imagens_disponiveis = False
                    origem_registro = 'W'
                    identificador_estabelecimento_saude = 5
                    # TRASFORMAR DATA DE NASCIMENTO
                    patientbirthdate = datetime(int(estudo['paciente_data_nascimento'].split('/')[2]), int(
                        estudo['paciente_data_nascimento'].split('/')[1]), int(estudo['paciente_data_nascimento'].split('/')[0]))

                    # TRATAR STUDYDATE
                    atendimento_datahora = estudo['atendimento_datahora'].split(
                        ' ')
                    studyDateArr = atendimento_datahora[0].split('/')
                    studydate = str(studyDateArr[2] + '-' +
                                    studyDateArr[1] + '-' + studyDateArr[0])
                    studyDatePsy = psycopg2.Date(int(studyDateArr[2]), int(
                        studyDateArr[1]), int(studyDateArr[0]))
                    studyTime = atendimento_datahora[1]

                    estudo_dicom = EstudoDicom()
                    estudo_dicom.studyinstanceuid = studyinstanceuid
                    estudo_dicom.studydate = studyDatePsy
                    estudo_dicom.patientname = patientname
                    estudo_dicom.imagens_disponiveis = imagens_disponiveis
                    estudo_dicom.origem_registro = origem_registro
                    estudo_dicom.accessionnumber = accessionnumber
                    estudo_dicom.patientid = patientid
                    estudo_dicom.patientsex = patientsex
                    estudo_dicom.studyid = studyid
                    estudo_dicom.studydescription = studydescription
                    estudo_dicom.modalitiesinstudy = modalitiesinstudy
                    estudo_dicom.identificador_estabelecimento_saude = identificador_estabelecimento_saude
                    estudo_dicom.patientbirthdate = patientbirthdate
                    estudo_dicom.studytime = studyTime
                    estudo_criados.append(estudo_dicom)
                # Caso exista passa-lo para criado on radiusls
            return estudo_criados

    @staticmethod
    def insert_on_db(exame):
        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute("""
            INSERT INTO radius_taas.estudo_dicom
            (accessionnumber,
            patientname,
            patientid,
            patientsex,
            patientbirthdate,
            studyid,
            studyinstanceuid,
            studydescription,
            modalitiesinstudy,
            imagens_disponiveis,
            origem_registro,
            identificador_estabelecimento_saude,
            studydate,
            studytime)
            VALUES ('%s' ,'%s','%s' ,
            '%s' ,'%s' ,'%s' ,
            '%s' ,'%s' ,'%s' ,
            '%s','%s', %s,
            '%s','%s')"""
                               % (exame.accessionnumber, exame.patientname, exame.patientid,
                                  exame.patientsex, exame.patientbirthdate, exame.studyid,
                                  exame.studyinstanceuid, exame.studydescription, exame.modalitiesinstudy,
                                  exame.imagens_disponiveis, exame.origem_registro, exame.identificador_estabelecimento_saude,
                                  exame.studydate, exame.studytime))

            except Exception as e:
                print(e)
            else:
                WorkListMV().update_to_created(exame.accessionnumber)
            finally:
                print(
                    """
            INSERT INTO radius_taas.estudo_dicom
            (accessionnumber,
            patientname,
            patientid,
            patientsex,
            patientbirthdate,
            studyid,
            studyinstanceuid,
            studydescription,
            modalitiesinstudy,
            imagens_disponiveis,
            origem_registro,
            identificador_estabelecimento_saude,
            studydate,
            studytime)
            VALUES ('%s' ,'%s','%s' ,
            '%s' ,'%s' ,'%s' ,
            '%s' ,'%s' ,'%s' ,
            '%s','%s', %s,
            '%s','%s')"""
                    % (exame.accessionnumber, exame.patientname, exame.patientid,
                       exame.patientsex, exame.patientbirthdate.split(' ')[
                           0], exame.studyid,
                       exame.studyinstanceuid, exame.studydescription, exame.modalitiesinstudy,
                       exame.imagens_disponiveis, exame.origem_registro, exame.identificador_estabelecimento_saude,
                       exame.studydate, exame.studytime))
