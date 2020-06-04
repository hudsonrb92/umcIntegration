from queries.estabelecimento_saude_queries import EstabelecimentoSaudeQueries


class EstabelecimentoSaudeRepositorio():
    def lista_estabelecimento(self,sessao, numero_cnpj):
        estabelecimento = EstabelecimentoSaudeQueries().pega_estabelecimento_por_cnpj(sessao=sessao, numero_cnpj=numero_cnpj)
        return estabelecimento