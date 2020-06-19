from queries.estabelecimento_saude_queries import EstabelecimentoSaudeQueries


class EstabelecimentoSaudeRepositorio():
    def lista_estabelecimento(self,sessao, numero_cnpj):
        estabelecimento = EstabelecimentoSaudeQueries().pega_estabelecimento_por_cnpj(sessao=sessao, numero_cnpj=numero_cnpj)
        return estabelecimento

    def pega_primeiro_estabelecimento(self, sessao):
        estab = EstabelecimentoSaudeQueries().pega_primeiro_estab(sessao)
        return estab
