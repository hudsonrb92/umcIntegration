from dominios.db import ProfissionalSaudeModel


class ProfissionalSaudeQueries():
    def lista_por_identificador_pessoa(self, sessao, identificador_pessoa):
        profissional_saude = sessao.query(ProfissionalSaudeModel).filter_by(
            identificador_pessoa=identificador_pessoa).first()
        return profissional_saude

    def inserir_profissional_saude(self, profissional_saude, sessao):
        sessao.add(profissional_saude)

    def lista_profissional_por_registro(self, sessao, registro_conselho_trabalho, identificador_estado_conselho):
        profissional = sessao.query(ProfissionalSaudeModel).filter(
            ProfissionalSaudeModel.registro_conselho_trabalho == registro_conselho_trabalho).filter(
            ProfissionalSaudeModel.identificador_estado_conselho_trabalho == identificador_estado_conselho).filter(
            ProfissionalSaudeModel.ativo == True).first()
        return profissional
