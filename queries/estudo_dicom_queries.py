import datetime

from sqlalchemy import func

from dominios.db import EstudoDicomModel


class EstudoDicomQuery():

    def atualizaRegistro(self, studyinstanceuid, estudo_dicom, sessao):
        pass

    def buscaClientes(self, sessao):
        estudos = sessao.query(EstudoDicomModel).all()
        return estudos

    def buscaEstudoPorStudy(self, studyinstanceuid, sessao):
        estudo = sessao.query(EstudoDicomModel).filter_by(
            studyinstanceuid=studyinstanceuid).first()
        return estudo

    def addEstudo(self, sessao, estudo):
        sessao.add(estudo)

    def set_medico_solicitante(self, sessao, identificador_profissional_saude_solicitante, accessionnumber):
        estudo = sessao.query(EstudoDicomModel).filter_by(
            accessionnumber=accessionnumber).first()
        if estudo:
            estudo.identificador_profissional_saude_solicitante = identificador_profissional_saude_solicitante

    def get_acc_duplicados(self, sessao):
        hoje = datetime.datetime.now()
        exams = sessao.query(func.count('*'), EstudoDicomModel.accessionnumber, EstudoDicomModel.patientid,
                             EstudoDicomModel.patientbirthdate) \
            .filter(EstudoDicomModel.situacao == 'V') \
            .filter(EstudoDicomModel.accessionnumber is not None and EstudoDicomModel.accessionnumber != '') \
            .filter(EstudoDicomModel.situacao_laudo == 'N') \
            .filter(EstudoDicomModel.patientid is not None and EstudoDicomModel.patientid != '') \
            .filter(func.to_char(EstudoDicomModel.studydate, 'MMYYYY') == f'{hoje.month:02}{hoje.year}') \
            .group_by(EstudoDicomModel.accessionnumber, EstudoDicomModel.patientid, EstudoDicomModel.patientbirthdate) \
            .having(func.count('*') == 2).all()
        return exams

    def buscaEstudoPorAccession(self, sessao, accessionnumber):
        exams = sessao.query(EstudoDicomModel).filter_by(
            accessionnumber=accessionnumber).all()
        return exams
