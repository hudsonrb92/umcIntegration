from dominios.db import EstudoDicomModel
from queries.estudo_dicom_queries import EstudoDicomQuery
from datetime import datetime


class EstudoDicomRepositorio():
    def now(self):
        return (f'{datetime.now().day:02}/{datetime.now().month:02}/{datetime.now().year} {datetime.now().hour:02}:{datetime.now().minute:02}:{datetime.now().second:02}')

    def listar_estudo(self, sessao):
        query_estudo = EstudoDicomQuery()
        estudos = query_estudo.buscaClientes(sessao)
        return estudos

    def listar_estudo_por_acc(self, sessao, accessionnumber):
        estudo = EstudoDicomQuery().buscaEstudoPorAccession(sessao, accessionnumber)
        return estudo

    def listar_por_studyinstanceuid(self, sessao, studyinstanceuid):
        query = EstudoDicomQuery().buscaEstudoPorStudy(
            sessao=sessao, studyinstanceuid=studyinstanceuid)
        return query

    def add_estudo(self, sessao, estudo_dicom):
        novo_estudo = EstudoDicomModel(studyinstanceuid=estudo_dicom.studyinstanceuid, studydate=estudo_dicom.studydate,
                                       patientname=estudo_dicom.patientname, situacao_laudo=estudo_dicom.situacao_laudo,
                                       identificador_prioridade_estudo_dicom=estudo_dicom.identificador_prioridade_estudo_dicom,
                                       numero_exames_ris=estudo_dicom.numero_exames_ris, situacao=estudo_dicom.situacao,
                                       imagens_disponiveis=estudo_dicom.imagens_disponiveis,
                                       origem_registro=estudo_dicom.origem_registro,
                                       modalitiesinstudy=estudo_dicom.modalitiesinstudy,
                                       identificador_estabelecimento_saude=estudo_dicom.identificador_estabelecimento_saude,
                                       studytime=estudo_dicom.studytime, accessionnumber=estudo_dicom.accessionnumber,
                                       studydescription=estudo_dicom.studydescription, patientid=estudo_dicom.patientid,
                                       patientbirthdate=estudo_dicom.patientbirthdate, studyid=estudo_dicom.studyid)

        EstudoDicomQuery().addEstudo(sessao, novo_estudo)

    def set_medico_solicitante(self, sessao, identificador_profissional_saude_solicitante, accessionnumber):
        EstudoDicomQuery().set_medico_solicitante(sessao=sessao,
                                                  identificador_profissional_saude_solicitante=identificador_profissional_saude_solicitante,
                                                  accessionnumber=accessionnumber)

    def remove_acc_duplicador(self, sessao):
        estudies = EstudoDicomQuery().get_acc_duplicados(sessao=sessao)
        print(f'{self.now()} Numero de accessions duplicados = {len(estudies)}')
        for estudo in estudies:
            exame = self.listar_estudo_por_acc(
                sessao=sessao, accessionnumber=estudo.accessionnumber)
            print(f'{self.now()} Accesion duplicado = {estudo.accessionnumber}')
            if len(exame) == 2:
                estud1 = exame[0]
                estud2 = exame[1]

                if (estud1.imagens_disponiveis is True and estud2.imagens_disponiveis is False) or (
                        estud1.imagens_disponiveis is False and estud2.imagens_disponiveis is True):
                    print("Accession duplicado encontrado")
                    print(f"Paciente {estud1.patientname}")
                    if (estud1.imagens_disponiveis is False) and (estud1.situacao_laudo == 'N'):
                        estud1.situacao = 'T'
                    if (estud2.imagens_disponiveis is False) and (estud2.situacao_laudo == 'N'):
                        estud2.situacao = 'T'
                        sessao.commit()
