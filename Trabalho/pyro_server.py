import Pyro4
import os

FILES_DIRECTORY = "D:\-files_p"


class Server(object):
    arquivosdisponiveis = []
    listainteresse = []
    usuario = []
    senha = []

    @Pyro4.expose
    def fazerupload(self, nome_arquivo, conteudo_arquivo):
        dir = FILES_DIRECTORY + "\\" + nome_arquivo
        with open(dir, 'w') as a:
            a.write(conteudo_arquivo)     

    @Pyro4.expose
    def consultar(self):
        return os.listdir(FILES_DIRECTORY)

    @Pyro4.expose
    def fazerdownload(self, nome_arquivo):
        dir = FILES_DIRECTORY + "\\" + nome_arquivo
        with open(dir, 'r') as a:
            return a.read()

    @Pyro4.expose
    def cadastra_usuario(self, usuario, senha):
        if(usuario != "" and senha != ""):
            Server.usuario.append(usuario)
            Server.senha.append(senha)
            return True
        else:
            print("Preencha todos os campos!")
            return False

    @Pyro4.expose
    def login_usuario(self, usuario, senha):
        if(usuario != "" and senha != ""):
            if(str(Server.senha[Server.usuario.index(usuario)]) == senha):
                return True
            else:
                return False

    @Pyro4.expose
    def recebe_interesse(self, nome_arquivo):
        self.listainteresse.append(nome_arquivo)

    @Pyro4.expose
    def consulta_interesse(self):
        return self.listainteresse

    @Pyro4.expose
    def cancelar_interesse(self, nome_arquivo):
        self.listainteresse.remove(nome_arquivo)


def startServer():
    server = Server()
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(server)
    ns.register("server", uri)
    print("Ready. object uri = ", uri)
    daemon.requestLoop()


if __name__ == "__main__":
    startServer()
