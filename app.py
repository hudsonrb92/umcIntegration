from datetime import datetime

from dominios.db import EstudoDicomModel
from entidades.estudo_dicom import EstudoDicom
from entidades.perfil_usuario_estabelecimento_saude import PerfilUsuarioEstabelecimentoSaude
from entidades.pessoa import Pessoa
from entidades.profissional_saude import ProfissionalSaude
from entidades.usuario import Usuario
from fabricas import fabrica_conexao
from mongoDB import WorkListMV
from repositories.estado_repositorio import EstadoRepositorio
from repositories.estudo_dicom_repositorio import EstudoDicomRepositorio
from repositories.perfil_usuario_estabelecimento_saude_repositorio import PerfilUsuarioEstabelecimentoSaudeRepositorio
from repositories.pessoa_repositorio import PessoaRepositorio
from repositories.profissional_saude_repositorio import ProfissionalSaudeRepositorio
from repositories.usuario_repositorio import UsuarioRepositorio

exames_worklist = WorkListMV().get_exames_not_created()
fabrica = fabrica_conexao.FabricaConexao()
sessao = fabrica.criar_sessao()

for exame in exames_worklist:

    # Criação da variável de número de acesso para verificação da necessiadade ou não de criação no banco de dados
    accessionnumber = exame['accessionnumber']
    studyinstanceuid = exame['studyinstanceuid']
    # Checar se existe exame no radius_taas
    estudo = sessao.query(EstudoDicomModel).filter_by(accessionnumber=accessionnumber).first()
    studyinstanceuid_queried = sessao.query(EstudoDicomModel).filter_by(studyinstanceuid=studyinstanceuid).first()
    # Caso exame exista entao marcar no banco mongo como criado para que consulta nao o pegue novamente
    if estudo or studyinstanceuid_queried:
        print(f" Estudo encontrado ->> {exame['paciente_nome']} <<-")
        print(f" Accesion Number ->> {accessionnumber} <<-")
        WorkListMV().update_to_created(accessionnumber)
        continue

    # Criação de Variáveis
    status = exame['status']
    paciente_id = exame['paciente_id']
    paciente_nome = exame['paciente_nome']
    paciente_data_nascimento = exame['paciente_data_nascimento']
    patientbirthdate = f'{paciente_data_nascimento.split("/")[2]}{paciente_data_nascimento.split("/")[1]}{paciente_data_nascimento.split("/")[0]}'
    paciente_sexo = exame['paciente_sexo']
    atendimento_id = exame['atendimento_id']
    atendimento_datahora = exame['atendimento_datahora']
    atendimento_datahora_splitado = atendimento_datahora.split(' ')[0].split('/')
    studydate = f'{atendimento_datahora_splitado[2]}-{atendimento_datahora_splitado[1]}-{atendimento_datahora_splitado[0]}'
    studytime = atendimento_datahora.split(' ')[1]
    pedido_id = exame['pedido_id']
    pedido_datahora = exame['pedido_datahora']
    item_exame_id = exame['item_exame_id']

    # Como médico solicitante nome pode vir nulo as vezes é bom fazer uma consulta no banco da worklist para ver se ja tem o nome criado
    medico_solicitante_nome = exame['medico_solicitante_nome']
    medico_solicitante_conselho_uf = exame['medico_solicitante_conselho_uf']
    medico_solicitante_crm = exame['medico_solicitante_crm']

    # Caso exista crm e nome esteja nulo ou em branco fazer consulta no banco para ver se encontra algo a respeito
    if medico_solicitante_nome == None or medico_solicitante_nome == '' and medico_solicitante_crm != None and medico_solicitante_crm != '':
        medico_solicitante_nome = WorkListMV().get_doctor_name_by_crm(medico_solicitante_crm)

    procedimento_modalidade = exame['procedimento_modalidade']
    procedimento_nome = exame['procedimento_nome']
    accessionnumber = exame['accessionnumber']
    createdAt = exame['createdAt']

    print(f" Iniciao de criação de exame no banco.")
    print(f" Nome Paciente: {paciente_nome}")
    print(f" Modalidade {procedimento_modalidade}, exame {procedimento_nome}")
    # Com a lista de exames que não possuem cadastro no radius proximo passo é checar se existe o médico solicitante
    # Para isso vamos fazer a entidade pessoa primeiro

    # Caso médico solicitante tenha algum valor no campo passado do worklist é preciso fazer a consulta
    if medico_solicitante_crm:
        print(f" Procurando médico ->> CRM:{medico_solicitante_crm} Nome:{medico_solicitante_nome}<<- ")
        # Consulta é feita pelo número de CRM e Sigla do estado do CRM
        profissional_saude_solicitante_alchemy = ProfissionalSaudeRepositorio().listar_profissional_saude_por_registro(
            sessao=sessao, registro_conselho_trabalho=medico_solicitante_crm, sigla=medico_solicitante_conselho_uf)

    # Fazer consulta no banco caso médico
    if profissional_saude_solicitante_alchemy:
        identificador_medico_solicitante = profissional_saude_solicitante_alchemy.identificador
        print(f' Profissional de saude encontrado ->> {identificador_medico_solicitante} <<-')

    elif medico_solicitante_nome != None or medico_solicitante_nome != '':
        print(
            f' Médico não encontrado ->> {medico_solicitante_nome} <<- ->> {medico_solicitante_crm} <<- ->> {medico_solicitante_conselho_uf} <<-')
        # Cadastrar Nova Usuario Solicitante
        try:
            # Cadastra Pessoa
            #antes checar se ja existe pessoa com mesmo nome
            pessoa_entidade = Pessoa(nome=medico_solicitante_nome, ativa=True)
            pessoa_entidade.identificador_sexo = None
            pessoa_entidade.data_nascimento = None
            pessoa_entidade.identificador_raca = None
            pessoa_buscada = PessoaRepositorio().pega_pessoa_por_nome(pessoa_entidade.nome, sessao)
            if pessoa_buscada:
                identificador_nova_pessoa = pessoa_buscada['identificador']
                print(f" Pessoa Encontrada, sem necessidade de novo cadastro. {identificador_nova_pessoa}.")
            else:
                PessoaRepositorio().cadastra_pessoa(pessoa=pessoa_entidade, sessao=sessao)
                identificador_nova_pessoa = PessoaRepositorio().pega_pessoa_por_nome(sessao=sessao,
                                                                                     nome=WorkListMV().get_doctor_name_by_crm(
                                                                                         medico_solicitante_crm)).identificador
                print(f" Pessoa Cadastrada {identificador_nova_pessoa}.")

            # Cadastra Profissional De Saude
            identificador_estado_conselho_trabalho_novo = EstadoRepositorio().pega_estado_por_sigla(sessao=sessao,
                                                                                                    sigla=medico_solicitante_conselho_uf).identificador

            profissional_saude_entidade = ProfissionalSaude(identificador_pessoa=identificador_nova_pessoa,
                                                            identificador_tipo_conselho_trabalho=1,
                                                            identificador_estado_conselho_trabalho=identificador_estado_conselho_trabalho_novo,
                                                            registro_conselho_trabalho=medico_solicitante_crm,
                                                            ativo=True)
            profissional_saude_entidade.assinatura_digitalizada = None
            ProfissionalSaudeRepositorio().inserir_profissional_saude(sessao=sessao,
                                                                      profissional_saude=profissional_saude_entidade)
            identificador_medico_solicitante = ProfissionalSaudeRepositorio().listar_profissional_saude_por_registro(
                sessao=sessao, registro_conselho_trabalho=medico_solicitante_crm,
                sigla=medico_solicitante_conselho_uf)
            print(f" Profissional Saude Cadatrado.")
            login_solicitante = f'{medico_solicitante_conselho_uf.lower()}{medico_solicitante_crm}'
            senha_solicitante = f'{medico_solicitante_crm}'
            # Cadastra Usuario
            usuario_entidade = Usuario(login=login_solicitante, senha=senha_solicitante, ativo=True,
                                       administrador=False)
            usuario_entidade.identificador_pessoa = identificador_nova_pessoa
            UsuarioRepositorio().inserir_usuario(usuario=usuario_entidade, sessao=sessao)
            print(f" Usuario Cadastrado.")

            # Criar Perfil Usuario Estabelecimento De Saude
            hoje = datetime.now()
            data_inicial = f'{hoje.year}-{hoje.month}-{hoje.day}'
            perfil_usuario_estabelecimento_saude_entidade = PerfilUsuarioEstabelecimentoSaude(
                identificador_perfil='ROLE_MEDICO_SOLICITANTE', identificador_estabelecimento_saude=1,
                data_inicial=data_inicial)
            perfil_usuario_estabelecimento_saude_entidade.identificador_usuario = UsuarioRepositorio().busca_user_por_id_pessoa(
                identificador_pessoa=identificador_nova_pessoa, sessao=sessao).identificador
            perfil_usuario_estabelecimento_saude_entidade.data_final = data_inicial

            PerfilUsuarioEstabelecimentoSaudeRepositorio().insere_pues(sessao=sessao,
                                                                       perfil_usuario_estabelecumento_saude=perfil_usuario_estabelecimento_saude_entidade)
            print(f' Perfil usuário estabelecimento saude cadastrado.')
            sessao.commit()

        except Exception as e:
            print(e)
            sessao.rollback()

    try:
        print(" Criando entidade de estudo dicom.")
        estudo_dicom_entidade = EstudoDicom(studyinstanceuid=studyinstanceuid, studydate=studydate,
                                            patientname=paciente_nome, situacao_laudo='N',
                                            identificador_prioridade_estudo_dicom='R', numero_exames_ris=1,
                                            situacao='V',
                                            imagens_disponiveis=False, origem_registro='W')
        estudo_dicom_entidade.modalitiesinstudy = procedimento_modalidade
        estudo_dicom_entidade.identificador_estabelecimento_saude = 5
        estudo_dicom_entidade.studytime = studytime
        estudo_dicom_entidade.accessionnumber = accessionnumber
        estudo_dicom_entidade.studydescription = procedimento_nome
        estudo_dicom_entidade.patientid = paciente_id
        estudo_dicom_entidade.patientbirthdate = patientbirthdate
        estudo_dicom_entidade.studyid = item_exame_id

        print(" Persistindo informação no banco de dados.")
        EstudoDicomRepositorio().add_estudo(sessao=sessao, estudo_dicom=estudo_dicom_entidade)
        WorkListMV().update_to_created(accessionnumber)

        if identificador_medico_solicitante:
            print(" Atribuição de médico solicitante ao exame recem criado.")
            EstudoDicomRepositorio().set_medico_solicitante(sessao=sessao, accessionnumber=accessionnumber,
                                                            identificador_medico_solicitante=identificador_medico_solicitante)
            sessao.commit()
            print(' Atribuição feita.')

        sessao.commit()
    except Exception as e:
        print(e)
        sessao.rollback()
