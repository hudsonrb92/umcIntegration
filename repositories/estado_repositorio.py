from queries import estado_queries

class EstadoRepositorio():
    def pega_estado_por_sigla(self,sessao, sigla):
        estado = estado_queries.EstadoQueries().pega_estado_por_sigla(sessao=sessao, sigla=sigla)
        return estado