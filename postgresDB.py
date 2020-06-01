from database import CursorFromConnectionFromPool
from datetime import datetime
from estudo_dicom import EstudoDicom
from mongoDB import WorkListMV
from psycopg2 import Date


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
                    patientbirthdate = estudo['paciente_data_nascimento'].split(
                        '/')
                    patientbirthdate = f"{patientbirthdate[2]}{patientbirthdate[1]}{patientbirthdate[0]}"
                    # TRATAR STUDYDATE
                    atendimento_datahora = estudo['atendimento_datahora'].split(
                        ' ')
                    studydate = Date(int(estudo['atendimento_datahora'].split(' ')[0].split('/')[2]),
                                     int(estudo['atendimento_datahora'].split(
                                         ' ')[0].split('/')[1]),
                                     int(estudo['atendimento_datahora'].split(' ')[0].split('/')[0]))
                    studytime = estudo['atendimento_datahora'].split(' ')[1]

                    estudo_dicom = EstudoDicom()
                    estudo_dicom.studyinstanceuid = studyinstanceuid
                    estudo_dicom.studydate = studydate
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
                    estudo_dicom.studytime = studytime
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
            %s,'%s')"""
                               % (exame.accessionnumber, exame.patientname, exame.patientid,
                                  exame.patientsex, exame.patientbirthdate, exame.studyid,
                                  exame.studyinstanceuid, exame.studydescription, exame.modalitiesinstudy,
                                  exame.imagens_disponiveis, exame.origem_registro, exame.identificador_estabelecimento_saude,
                                  exame.studydate, exame.studytime))

            except Exception as e:
                print(f'Erro : {e}')
            else:
                hoje = hoje = datetime.now()
                print(
                    f"Paciente {exame.patientname} criado no RadiusTaas.\nProntuário {exame.patientid}")
                print(
                    f"Execução feita com sucesso -> {hoje.day}/{hoje.month}/{hoje.year} {hoje.hour}:{hoje.minute}:{hoje.second}")
                WorkListMV().update_to_created(exame.accessionnumber)
            finally:
                print('Fim da Execução')

    @staticmethod
    def relaciona_exame():
