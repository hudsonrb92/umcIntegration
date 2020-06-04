from dominios.db import EstudoDicomModel
from entidades.pessoa import Pessoa
from fabricas import fabrica_conexao
from mongoDB import WorkListMV
from repositories.pessoa_repositorio import PessoaRepositorio
from repositories.profissional_saude_repositorio import ProfissionalSaudeRepositorio

exames_worklist = WorkListMV().get_exames_not_created()
fabrica = fabrica_conexao.FabricaConexao()
sessao = fabrica.criar_sessao()

for exame in exames_worklist:

    # Criação da variável de número de acesso para verificação da necessiadade ou não de criação no banco de dados
    accessionnumber = exame['accessionnumber']
    # Checar se existe exame no radius_taas
    estudo = sessao.query(EstudoDicomModel).filter_by(accessionnumber=accessionnumber).first()
    # Caso exame exista entao marcar no banco mongo como criado para que consulta nao o pegue novamente
    if estudo:
        WorkListMV().update_to_created(accessionnumber)
        continue

    # Criação de Variáveis
    status = exame['status']
    paciente_id = exame['paciente_id']
    paciente_nome = exame['paciente_nome']
    paciente_data_nascimento = exame['paciente_data_nascimento']
    paciente_sexo = exame['paciente_sexo']
    atendimento_id = exame['atendimento_id']
    atendimento_datahora = exame['atendimento_datahora']
    pedido_id = exame['pedido_id']
    pedido_datahora = exame['pedido_datahora']
    item_exame_id = exame['item_exame_id']
    medico_solicitante_nome = exame['medico_solicitante_nome']
    medico_solicitante_conselho_uf = exame['medico_solicitante_conselho_uf']
    medico_solicitante_crm = exame['medico_solicitante_crm']
    procedimento_modalidade = exame['procedimento_modalidade']
    procedimento_nome = exame['procedimento_nome']
    convenio_nome = exame['convenio_nome']
    convenio_codigo_ans = exame['convenio_codigo_ans']
    accessionnumber = exame['accessionnumber']
    studyinstanceuid = exame['studyinstanceuid']
    createdAt = exame['createdAt']
    created_on_radius = exame['created_on_radius']

    # Com a lista de exames que não possuem cadastro no radius proximo passo é checar se existe o médico solicitante
    # Para isso vamos fazer a entidade pessoa primeiro

    if medico_solicitante_crm:
        profissional_saude_solicitante_alchemy = ProfissionalSaudeRepositorio().listar_profissional_saude()