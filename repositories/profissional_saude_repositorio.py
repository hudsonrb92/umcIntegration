from base64 import b64decode

from dominios.db import ProfissionalSaudeModel
from queries.estado_queries import EstadoQueries
from queries.profissional_saude_queries import ProfissionalSaudeQueries


class ProfissionalSaudeRepositorio():
    def inserir_profissional_saude(self, sessao, profissional_saude):
        if profissional_saude.assinatura_digitalizada:
            assinatura_decodada = b64decode(profissional_saude.assinatura_digitalizada)
        else:
            assinatura_decodada = profissional_saude.assinatura_digitalizada
        novo_profissional_saude = ProfissionalSaudeModel(identificador_pessoa=profissional_saude.identificador_pessoa,
                                                         identificador_tipo_conselho_trabalho=1,
                                                         identificador_estado_conselho_trabalho=profissional_saude.identificador_estado_conselho_trabalho,
                                                         registro_conselho_trabalho=profissional_saude.registro_conselho_trabalho,
                                                         ativo=profissional_saude.ativo,
                                                         assinatura_digitalizada=assinatura_decodada)
        ProfissionalSaudeQueries().inserir_profissional_saude(profissional_saude=novo_profissional_saude, sessao=sessao)

    def listar_profissional_saude(self, sessao, identificador_pessoa):
        profissional = ProfissionalSaudeQueries().lista_por_identificador_pessoa(sessao=sessao,
                                                                                 identificador_pessoa=identificador_pessoa)
        return profissional

    def listar_profissional_saude_por_registro(self, sessao, registro_conselho_trabalho, sigla):
        identificador_estado_conselho = EstadoQueries().pega_estado_por_sigla(sessao=sessao, sigla=sigla).identificador

        profissional = ProfissionalSaudeQueries().lista_profissional_por_registro(sessao,
                                                                                  registro_conselho_trabalho=registro_conselho_trabalho.upper(),
                                                                                  identificador_estado_conselho=identificador_estado_conselho)
        return profissional
