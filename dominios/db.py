from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, LargeBinary, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import now

from fabricas import fabrica_conexao

fabrica = fabrica_conexao.FabricaConexao()
engine = fabrica.conectar()

Base = declarative_base()


class Sexo(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'Sexo'

    identificador = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)


class PessoaModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'pessoa'

    identificador = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(DateTime, nullable=True)
    identificador_sexo = Column(Integer, nullable=True)
    identificador_raca = Column(Integer, nullable=True)
    ativa = Column(Boolean, nullable=False)


class AnexoEstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = 'anexo_estudo_dicom'

    identificador = Column(Integer, primary_key=True)
    identificador_estudo_dicom = Column(
        ForeignKey('radius_taas.estudo_dicom.identificador'))
    nome_arquivo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    conteudo_arquivo = Column(LargeBinary(16), nullable=False)
    estudo_dicom = relationship(
        "EstudoDicomModel", back_populates="anexo_estudo_dicom")


class AnotacaoEstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = 'anotacao_estudo_dicom'

    identificador = Column(Integer, primary_key=True)
    identificador_estudo_dicom = Column(ForeignKey(
        'radius_taas.estudo_dicom.identificador'), nullable=False)
    data_hora_registro = Column(DateTime, nullable=False)
    identificador_profissional_saude = Column(ForeignKey(
        'public.profissional_saude.identificador'), nullable=True)
    texto = Column(Text, nullable=False)
    origem = Column(String, nullable=False)
    estudo_dicom = relationship(
        "EstudoDicomModel", back_populates="anotacao_estudo_dicom")
    profissional_saude = relationship(
        "ProfissionalSaudeModel", back_populates="anotacao_estudo_dicom")


class EnderecoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'endereco'

    identificador = Column(Integer, primary_key=True)
    identificador_tipo_endereco = Column(Integer, nullable=False)
    logradouro = Column(String, nullable=False)
    complemento = Column(Text, nullable=True)
    bairro = Column(String, nullable=True)
    cep = Column(Integer, nullable=False)
    identificador_cidade = Column(Integer, ForeignKey('public.cidade.identificador'))
    ativo = Column(Boolean, nullable=False)


class EstabelecimentoSaudeModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'estabelecimento_saude'

    identificador = Column(Integer, primary_key=True)
    numero_cnes = Column(Integer, nullable=True)
    numero_cnpj = Column(Integer, nullable=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    identificador_endereco = Column(Integer, ForeignKey(
        'public.endereco.identificador'), nullable=False)
    endereco = relationship(EnderecoModel, backref=backref(
        "estabelecimento_saude", lazy="dynamic"))
    ativo = Column(Boolean, nullable=False)
    logotipo = Column(String, nullable=True)
    url_resultado_exames = Column(String, nullable=True)


class EstadoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'estado'

    identificador = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    codigo_ibge = Column(Integer, nullable=False)
    identificador_pais = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False)
    sigla = Column(String, nullable=False)
    estado_conselho_trabalho = relationship("ProfissionalSaudeModel",
                                            foreign_keys='ProfissionalSaudeModel.identificador_estado_conselho_trabalho',
                                            backref='estado_conselho_trabalho', lazy='dynamic')
    cidade = relationship("CidadeModel",
                          foreign_keys='CidadeModel.identificador_estado',
                          backref='cidade', lazy='dynamic')


class EstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = 'estudo_dicom'

    identificador = Column(Integer, primary_key=True)

    identificador_estabelecimento_saude = Column(Integer,
                                                 ForeignKey(
                                                     'public.estabelecimento_saude.identificador'),
                                                 nullable=False)
    estabelecimento_saude = relationship(EstabelecimentoSaudeModel,
                                         backref=backref('estudo_dicom', lazy='dynamic'))
    laudo_estudo_dicom = relationship(
        "LaudoEstudoDicomModel", back_populates="estudo_dicom")
    anotacao_estudo_dicom = relationship(
        AnotacaoEstudoDicomModel, back_populates="estudo_dicom")
    anexo_estudo_dicom = relationship(
        AnexoEstudoDicomModel, back_populates="estudo_dicom")

    identificador_convenio = Column(Integer(), ForeignKey(
        'radius_taas.convenio.identificador'), nullable=True)

    convenio = relationship("ConvenioModel", back_populates="estudo_dicom")

    identificador_prioridade_estudo_dicom = Column(Integer(),
                                                   ForeignKey(
                                                       'radius_taas.prioridade_estudo_dicom.identificador'),
                                                   nullable=False)
    prioridade_estudo_dicom = relationship("PrioridadeEstudoDicomModel", back_populates="estudo_dicom")

    identificador_profissional_saude_direcionado = Column(Integer(),
                                                          ForeignKey(
                                                              'public.profissional_saude.identificador'),
                                                          nullable=True)

    identificador_profissional_saude_operador = Column(Integer(),
                                                       ForeignKey(
                                                           'public.profissional_saude.identificador'),
                                                       nullable=True)

    identificador_profissional_saude_solicitante = Column(Integer(),
                                                          ForeignKey(
                                                              'public.profissional_saude.identificador'),
                                                          nullable=True)

    identificador_profissional_saude_validacao = Column(Integer(),
                                                        ForeignKey(
                                                            'public.profissional_saude.identificador'),
                                                        nullable=True)

    chave_primaria_origem = Column(Integer, nullable=True)

    studyinstanceuid = Column(String, nullable=False)

    studydate = Column(DateTime, nullable=False)

    studytime = Column(String, nullable=True)

    patientid = Column(String, nullable=True)

    patientname = Column(String, nullable=False)

    accessionnumber = Column(String, nullable=True)

    studydescription = Column(String, nullable=True)

    modalitiesinstudy = Column(String, nullable=True)

    data_hora_inclusao = Column(DateTime, nullable=False, default=now)

    data_hora_ultima_alteracao = Column(DateTime, nullable=True)

    situacao_laudo = Column(String, nullable=False)

    numero_exames_ris = Column(Integer, nullable=False)

    studyid = Column(String, nullable=True)

    patientsex = Column(String, nullable=True)

    patientbirthdate = Column(String, nullable=True)

    nome_operador = Column(String, nullable=True)

    numberofseries = Column(Integer, nullable=True)

    numberofinstances = Column(Integer, nullable=True)

    situacao = Column(String, nullable=False)

    nome_mae = Column(String, nullable=True)

    imagens_disponiveis = Column(Boolean, nullable=False)

    origem_registro = Column(String, nullable=False)

    data_hora_validacao = Column(DateTime, nullable=True)

    chave_primaria_origem_worklist = Column(Integer, nullable=True)


class LaudoEstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = 'laudo_estudo_dicom'

    identificador = Column(Integer, primary_key=True)
    identificador_estudo_dicom = Column(Integer, ForeignKey('radius_taas.estudo_dicom.identificador'),
                                        nullable=False)
    estudo_dicom = relationship(
        "EstudoDicomModel", back_populates="laudo_estudo_dicom")
    data_hora_emissao = Column(DateTime, nullable=False)
    identificador_profissional_saude = Column(Integer, ForeignKey('public.profissional_saude.identificador'),
                                              nullable=True)
    identificador_profissional_saude_revisor = Column(Integer,
                                                      ForeignKey(
                                                          'public.profissional_saude.identificador'),
                                                      nullable=True)
    texto = Column(Text, nullable=False)
    data_hora_revisao = Column(DateTime, nullable=False)
    situacao = Column(String, nullable=False)
    numero_exames_relacionados = Column(Integer, nullable=True)
    situacao_envio_his = Column(String, nullable=False)


class ProfissionalSaudeModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'profissional_saude'

    identificador = Column(Integer, primary_key=True)
    identificador_pessoa = Column(Integer, ForeignKey(
        'public.pessoa.identificador'), nullable=False)
    pessoa = relationship("PessoaModel", backref=backref(
        "profissional_saude", lazy="dynamic"))
    identificador_tipo_conselho_trabalho = Column(Integer, nullable=False)
    identificador_estado_conselho_trabalho = Column(
        Integer, ForeignKey('public.estado.identificador'), nullable=False)
    registro_conselho_trabalho = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)
    assinatura_digitalizada = Column(LargeBinary(16), nullable=True)

    executor_laudo = relationship('LaudoEstudoDicomModel',
                                  foreign_keys='LaudoEstudoDicomModel.identificador_profissional_saude',
                                  backref='executor_laudo', lazy='dynamic')

    revisor_laudo = relationship('LaudoEstudoDicomModel',
                                 foreign_keys='LaudoEstudoDicomModel.identificador_profissional_saude_revisor',
                                 backref='revisor_laudo', lazy='dynamic')

    anotacao_estudo_dicom = relationship(
        "AnotacaoEstudoDicomModel", back_populates="profissional_saude")



class UsuarioModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'usuario'

    identificador = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    administrador = Column(Boolean, nullable=False)
    identificador_pessoa = Column(Integer, ForeignKey(
        'public.pessoa.identificador'), nullable=False)
    pessoa = relationship(
        "PessoaModel", backref=backref("usuario", lazy="dynamic"))
    ativo = Column(Boolean, nullable=False)


class PerfilUsuarioEstabelecimentoSaudeModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "perfil_usuario_estabelecimento_saude"

    identificador_perfil = Column(String, nullable=False)
    identificador_usuario = Column(Integer, ForeignKey(
        'public.usuario.identificador'), nullable=False)
    identificador_estabelecimento_saude = Column(Integer, nullable=False)
    data_inicial = Column(Date, nullable=False, primary_key=True)
    data_final = Column(Date, nullable=True)


class PessoaEnderecoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "pessoa_endereco"

    identificador_pessoa = Column(Integer, nullable=False, primary_key=True)
    identificador_endereco = Column(Integer, nullable=False)
    identificador_tipo_uso_endereco = Column(String, nullable=False)
    ativa = Column(Boolean, nullable=False)


class CidadeModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "cidade"

    identificador = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    codigo_ibge = Column(Integer, nullable=False)
    identificador_estado = Column(Integer, ForeignKey(
        'public.estado.identificador'), nullable=False)
    ativa = Column(Boolean, nullable=False)


class EstabelecimentoSaudeContato(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "estabelecimento_saude_contato"

    identificador = Column(Integer, primary_key=True)
    identificador_estabelecimento_saude = Column(Integer, ForeignKey('public.estabelecimento_saude.identificador'),
                                                 nullable=False)
    identificador_tipo_contato = Column(String, nullable=False)
    contato = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)


class ModalidadeModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "modalidade"

    identificador = Column(Integer, primary_key=True)
    sigla = Column(String, nullable=False)
    descricao_original = Column(String, nullable=False)
    descricao_traduzida = Column(String, nullable=False)
    ativa = Column(Boolean, nullable=False)


class ModeloFraseModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "modelo_frase"

    identificador = Column(Integer, primary_key=True)
    identificador_estabelecimento_saude = Column(Integer, nullable=True)
    identificador_modalidade = Column(Integer, nullable=True)
    identificador_profissional_saude = Column(Integer, nullable=True)
    texto = Column(String, nullable=False)
    descricao = Column(String, nullable=False)


class ModeloLaudoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "modelo_laudo"

    identificador = Column(Integer, primary_key=True)
    identificador_estabelecimento_saude = Column(Integer, nullable=True)
    identificador_modalidade = Column(Integer, nullable=True)
    identificador_profissional_saude = Column(Integer, nullable=True)
    texto = Column(String, nullable=False)
    descricao = Column(String, nullable=False)


class ModeloLaudoUsuarioModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "modelo_laudo_usuario"

    identificador_modelo_laudo = Column(Integer, nullable=False, primary_key=True)
    identificador_usuario = Column(Integer, nullable=False)


class PaisModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "pais"
    identificador = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)


class ParametroConfiguracaoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "parametro_configuracao"

    identificador_estabelecimento_saude = Column(Integer, primary_key=True)
    chave = Column(String, nullable=False)
    valor = Column(String, nullable=False)


class PerfilModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "perfil"

    identificador = Column(String, nullable=False, primary_key=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)


class PessoaContatoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "pessoa_contato"

    identificador = Column(Integer, primary_key=True)
    identificador_pessoa = Column(Integer, ForeignKey('public.pessoa.identificador'), nullable=False)
    identificador_tipo_contato = Column(String, nullable=False)
    contato = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


class TipoConselhoTrabalhoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "tipo_conselho_trabalho"

    identificador = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


class TipoContatoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "tipo_contato"

    identificador = Column(String, primary_key=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)


class TipoEnderecoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "tipo_endereco"

    identificador = Column(String, primary_key=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


class TipoUsoEnderecoModel(Base):
    __table_args__ = {'schema': 'public'}
    __tablename__ = "tipo_uso_endereco"

    identificador = Column(String, primary_key=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


class AetitleEstabelecimentoSaude(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "aetitle_estabelecimento_saude"

    identificador = Column(String, nullable=False, primary_key=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


class ConvenioModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "convenio"

    identificador = Column(Integer, primary_key=True, nullable=False)
    razao_social = Column(String, nullable=True)
    nome_fantasia = Column(String, nullable=False)
    numero_cnpj = Column(String, nullable=True)
    numero_registro_ans = Column(Integer, nullable=False)
    identificador_estabelecimento_saude = Column(Integer, ForeignKey('public.estabelecimento_saude.identificador'), nullable=False)
    identificador_usuario = Column(Integer, nullable=True)
    estudo_dicom = relationship("EstudoDicomModel", back_populates="convenio", uselist=False)


class EmissaoLaudoEstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "emissao_laudo_estudo_dicom"

    identificador = Column(Integer, nullable=False, primary_key=True)
    identificador_estudo_dicom = Column(Integer, ForeignKey('radius_taas.estudo_dicom.identificador'), nullable=False)
    identificador_profissional_saude = Column(Integer, ForeignKey('public.profissional_saude.identificador'),
                                              nullable=False)
    data_hora_inicio = Column(DateTime)
    data_hora_ultima_alteracao = Column(DateTime)
    data_hora_termino = Column(DateTime)
    situacao = Column(String)


class ParametrosLaudoModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "parametros_laudo"

    identificador = Column(Integer, primary_key=True)
    endereco_rodape = Column(Boolean, nullable=False)
    espacamento_imagem_dados_cabecalho = Column(Integer, nullable=False)
    identificador_estabelecimento_saude = Column(Integer, nullable=True)
    logotipo_cabecalho = Column(Boolean, nullable=False)
    margem_direita = Column(Integer, nullable=False)
    margem_esquerda = Column(Integer, nullable=False)
    margem_inferior = Column(Integer, nullable=False)
    margem_superior = Column(Integer, nullable=False)
    espacamento_dados_exame_conteudo_laudo = Column(Integer, nullable=True)


class PrioridadeEstudoDicomModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "prioridade_estudo_dicom"

    identificador = Column(String, primary_key=True)
    descricao = Column(String, nullable=False)
    ordenacao = Column(Integer, nullable=False)
    estudo_dicom = relationship("EstudoDicomModel", back_populates="prioridade_estudo_dicom", uselist=False)


class RelatorioProdutividadeModel(Base):
    __table_args__ = {'schema': 'radius_taas'}
    __tablename__ = "relatorio_produtividade"

    identificador = Column(Integer, primary_key=True)
    data_hora_geracao = Column(DateTime, nullable=False)
    data_inicio_referencia = Column(Date, nullable=False, default=now())
    data_fim_referencia = Column(Date, nullable=False)
    identificador_estabelecimento_saude = Column(Integer, nullable=True)
    identificador_profissional_saude = Column(Integer, nullable=True)
    nome_arquivo = Column(String, nullable=False)
    conteudo = Column(LargeBinary)
