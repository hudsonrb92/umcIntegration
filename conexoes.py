from sshtunnel import SSHTunnelForwarder
from random import randint

class Conexoes:
    def __init__(self):
        self.elaudos = None
        self.campinas = None
    
    @staticmethod
    def get_radom_int():
        port = randint(5000,6000)
        if port != 5555:
            return port
        else:
            port = 5444
            return port

    @classmethod
    def open_umc(cls):
        cls.elaudos = SSHTunnelForwarder(
            'sistema.elaudos.com',
            ssh_username="ubuntu",
            ssh_pkey="E:/Dropbox/Querys/elaudos.pem",
            remote_bind_address=('127.0.0.1', 5432),
            local_bind_address=('127.0.0.1', 5555)
        )
        return cls.elaudos

    @classmethod
    def open_campinas(cls,**kwargs):
        cls.campinas = SSHTunnelForwarder(
            'hgc.erad.com.br',
            ssh_username="root",
            ssh_password="mtpP@$$admin",
            remote_bind_address=('127.0.0.1', 5432),
            **kwargs
        )
        return cls.campinas
    
    @classmethod
    def close_campinas(cls):
        return cls.campinas.stop()
    
    @classmethod
    def close_elaudos(cls):
        return cls.elaudos.close() 
    
    def __enter__(self):
        self.elaudos = self.elaudos.start()
        return self.elaudos

    def __exit__(self,exception_value,excp,excep_out):
        if exception_value:
            self.elaudos.stop()
            print("Erro de conexao")
        else:
            self.elaudos.stop()
            print("Saida Da Conexao.")