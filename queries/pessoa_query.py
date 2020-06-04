from dominios.db import PessoaModel


class PessoaQuery:
    def lista_pessoa_por_nome(self, nome, sessao):
        pessoa = sessao.query(PessoaModel).filter_by(nome=nome).all()
        return pessoa

    def insere_pessoa(self, pessoa, sessao):
        sessao.add(pessoa)
