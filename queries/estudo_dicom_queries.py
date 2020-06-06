from dominios.db import EstudoDicomModel


class EstudoDicomQuery():

    def atualizaRegistro(self, studyinstanceuid, estudo_dicom, sessao):
        pass

    def buscaClientes(self, sessao):
        estudos = sessao.query(EstudoDicomModel).all()
        return estudos

    def buscaEstudoPorStudy(self, studyinstanceuid, sessao):
        estudo = sessao.query(EstudoDicomModel).filter_by(studyinstanceuid=studyinstanceuid).first()
        return estudo

    def addEstudo(self,sessao, estudo):
        sessao.add(estudo)

    def set_medico_solicitante(self,sessao, identificador_medico_solicitante, accessionnumber):
        estudo = sessao.query(EstudoDicomModel).filter_by(accessionnumber=accessionnumber).first()
        if estudo:
            estudo.identificador_profissional_saude_solicitante = identificador_medico_solicitante