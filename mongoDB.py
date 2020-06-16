from mongoengine import *
# Realizar conexao com banco de dados Mongo
connect('worklist-umc')


class Worklist(DynamicDocument):
    meta = {'collection': 'worklists'}


class WorkListMV():
    @staticmethod
    def get_exames_not_created():
        exames = Worklist.objects(
            Q(created_on_radius__exists=False) | Q(created_on_radius=False))
        return exames

    @staticmethod
    def update_to_created(accessionnumber):
        Worklist.objects(accessionnumber=accessionnumber).update(
            created_on_radius=True)

    @staticmethod
    def get_doctor_name_by_crm(crm):
       medico = Worklist.objects(Q(medico_solicitante_nome__exists=True) & Q(medico_solicitante_crm=f'{crm}'))
       if medico:
           return medico[0].medico_solicitante_nome