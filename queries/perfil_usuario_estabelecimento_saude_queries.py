from dominios.db import PerfilUsuarioEstabelecimentoSaudeModel


class PerfilUsuarioEstabelecimentoSaudeQueries():
    def lista_perfil_por_identificador_usuario(self, sessao, identificador_usuario):
        perfil = sessao.query(PerfilUsuarioEstabelecimentoSaudeModel).filter_by(
            identificador_usuario=identificador_usuario).first()
        return perfil

    def insere_perfil(self,sessao, perfil_usuario):
        sessao.add(perfil_usuario)

    def busca_pues_por_userId(self, sessao, userId):
        pues_existent = sessao.query(PerfilUsuarioEstabelecimentoSaudeModel)\
            .filter(PerfilUsuarioEstabelecimentoSaudeModel.identificador_usuario == userId).first()
        return pues_existent