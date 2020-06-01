import hashlib
from datetime import datetime

from psycopg2 import Date

from dominios.db import EstudoDicomModel, ProfissionalSaudeModel, PessoaModel, UsuarioModel, \
    PerfilUsuarioEstabelecimentoSaudeModel, EstadoModel
from estudo_dicom import EstudoDicom
from fabricas.fabrica_conexao import FabricaConexao
from mongoDB import WorkListMV


class PostgresDB:

    @classmethod
    def check_if_exists_on_radius(cls, lista_de_exames):
        estudo_criados = []
        for estudo in lista_de_exames:
            fabrica = FabricaConexao()
            sessao = fabrica.criar_sessao()
            exame = sessao.query(EstudoDicomModel).filter_by(accessionnumber=estudo['accessionnumber']).first()

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
                medico_solicitante_nome = estudo['medico_solicitante_nome']
                medico_solicitante_conselho_uf = estudo['medico_solicitante_conselho_uf']
                medico_solicitante_crm = estudo['medico_solicitante_crm']
                convenio_nome = estudo['convenio_nome']
                convenio_codigo_ans = estudo['convenio_codigo_ans']

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
                estudo_dicom.medico_solicitante_nome = medico_solicitante_nome
                estudo_dicom.medico_solicitante_conselho_uf = medico_solicitante_conselho_uf
                estudo_dicom.medico_solicitante_crm = medico_solicitante_crm
                estudo_dicom.convenio_nome = convenio_nome
                estudo_dicom.convenio_codigo_ans = convenio_codigo_ans
                estudo_criados.append(estudo_dicom)
            # Caso exista passa-lo para criado on radiusls
        sessao.close()
        return estudo_criados

    @staticmethod
    def insert_on_db(exame):
        fabrica = FabricaConexao()
        sessao = fabrica.criar_sessao()
        if exame.medico_solicitante_nome:
            identificador_profissional_saude_solicitante = sessao.query(ProfissionalSaudeModel).filter(
                ProfissionalSaudeModel.registro_conselho_trabalho == exame.medico_solicitante_conselho_uf).filter(
                ProfissionalSaudeModel.identificador_pessoa == PessoaModel.identificador).filter(
                PessoaModel.nome == exame.medico_solicitante_nome).first().identificador
        else:
            try:
                nova_pessoa_soliciante = PessoaModel(nome=exame.medico_solicitante_nome, ativo=True)
                sessao.add(nova_pessoa_soliciante)
                sessao.commit()
                print(f"Entidade Pessoa Criada! {exame.medico_solicitante_nome}")
            except Exception as e:
                print(e)
                sessao.rollback()

            try:
                identificador_pessoa_solicitante_nova = nova_pessoa_soliciante.identificador
                identificador_estado_novo_medico_solicitante = sessao.query(EstadoModel).filter_by(
                    sigla=exame.medico_solicitante_conselho_uf).first().identificador
                novo_profissional_saude_solicitante = ProfissionalSaudeModel(
                    identificador_pessoa=identificador_pessoa_solicitante_nova, identificador_tipo_conselho_trabalho=1,
                    identificador_estado_conselho_trabalho=identificador_estado_novo_medico_solicitante,
                    registro_conselho_trabalho=exame.medico_solicitante_crm, ativo=True)
                sessao.add(novo_profissional_saude_solicitante)
                sessao.commit()
                print(f"Entidade Profissional Saude Criada! {exame.medico_solicitante_crm}")
            except Exception as e:
                print(e)
                sessao.rollback()

            try:
                login_solicitante = f"{str(exame.medico_solicitante_conselho_uf).lower()}{exame.medico_solicitante_crm}"
                senha_solicitante = f"{exame.medico_solicitante_crm}"
                senha_hasheada = hashlib.md5(senha_solicitante.encode('utf')).hexdigest()
                novo_usuario_solicitante = UsuarioModel(login=login_solicitante, senha=senha_hasheada, administrador=False,
                                                        identificador_pessoa=identificador_pessoa_solicitante_nova,
                                                        ativo=True)
                sessao.add(novo_usuario_solicitante)
                sessao.commit()
                print(f"Entidade Usuario Criado!")
            except Exception as e:
                print(e)
                sessao.rollback()

            try:
                identificador_usuario_solicitante = novo_usuario_solicitante.identificador
                hoje = datetime.now()
                hoje_str = f"{hoje.year}-{hoje.month}-{hoje.day}"
                novo_perfil_usuario_estabelecimento_saude_solicitante = PerfilUsuarioEstabelecimentoSaudeModel(
                    identificador_perfil='ROLE_MEDICO_SOLICITANTE', identificador_usuario=identificador_usuario_solicitante,
                    identificador_estelecimento_saude=5, data_inicial=hoje_str, data_final=hoje_str)
                sessao.add(novo_perfil_usuario_estabelecimento_saude_solicitante)
                sessao.commit()
                print(f"Entidade Perfil Usuario Estelecimento Saude Criado")
            except Exception as e:
                print(e)
                sessao.rollback()

        novo_estudo = EstudoDicomModel(accessionnumber=exame.accessionnumber, patientname=exame.patientname,
                                       patientid=exame.patientid, patientsex=exame.patientsex,
                                       patientbirthdate=exame.patientbirthdate, studyid=exame.studyid,
                                       studyinstanceuid=exame.studyinstanceuid, studydescription=exame.studydescription,
                                       modalitiesinstudy=exame.modalitiesinstudy,
                                       imagens_disponiveis=exame.imagens_disponiveis,
                                       origem_registro=exame.origem_registro,
                                       identificador_estabelecimento_saude=exame.identificador_estabelecimento_saude,
                                       studydate=exame.studydate, studytime=exame.studytime,
                                       identificador_profissional_saude_solicitante=identificador_profissional_saude_solicitante)

        try:
            sessao.add(novo_estudo)
            hoje = datetime.now()
            print(f"Paciente {exame.patientname} criado no RadiusTaas.\nProntuário {exame.patientid}")
            print(
                f"Execução feita com sucesso -> {hoje.day}/{hoje.month}/{hoje.year} {hoje.hour}:{hoje.minute}:{hoje.second}")

        except Exception as e:
            print(e)
            sessao.rollback()
        else:
            sessao.commit()
            exame_criado = sessao.query(EstudoDicomModel).filter_by(accessionnumber=exame.accessionnumber).first()
            if exame_criado:
                WorkListMV().update_to_created(accessionnumber=exame.accessionnumber)
        finally:
            print('Fim da Execução')
            sessao.close()
