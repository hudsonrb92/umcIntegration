from queries.estudo_dicom_queries import EstudoDicomQuery
from dominios.db import EstudoDicomModel

class EstudoDicomRepositorio():

    def listar_estudo(self, sessao):
        query_estudo = EstudoDicomQuery()
        estudos = query_estudo.buscaClientes(sessao)
        return estudos

    def listar_por_studyinstanceuid(self, sessao, studyinstanceuid):
        query = EstudoDicomQuery().buscaEstudoPorStudy(sessao=sessao, studyinstanceuid=studyinstanceuid)
        return query

    def add_estudo(self,sessao, estudo_dicom):
        novo_estudo = EstudoDicomModel(studyinstanceuid=estudo_dicom.studyinstanceuid, studydate=estudo_dicom.studydate,
                                       patientname=estudo_dicom.patientname, situacao_laudo=estudo_dicom.situacao_laudo,
                                       identificador_prioridade_estudo_dicom=estudo_dicom.identificador_prioridade_estudo_dicom,
                                       numero_exames_ris=estudo_dicom.numero_exames_ris, situacao=estudo_dicom.situacao,
                                       imagens_disponiveis=estudo_dicom.imagens_disponiveis,origem_registro=estudo_dicom.origem_registro)
        EstudoDicomQuery().addEstudo(sessao, novo_estudo)