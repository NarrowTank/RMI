import Pyro4
import tkinter as tk

server = Pyro4.Proxy("PYRONAME:server")
arquivos = str(server.consultar())

def enviar_arquivo():
    tela_envia = tk.Tk()

    def confirma():
        if(entrada_nome.get() != "" and entrada_diretorio.get() != ""):
            diretorio = entrada_diretorio.get() + "\\" + entrada_nome.get()
            with open(diretorio, "r") as d:
                conteudo_arquivo = d.read()
                server.fazerupload(entrada_nome.get(), conteudo_arquivo)
            tela_envia.destroy()
        else:
            print("Campo Vazio!")

    tela_envia.geometry("300x200")
    label_nome = tk.Label(tela_envia, text="Nome do arquivo: ").place(x=10, y=40)
    entrada_nome = tk.Entry(tela_envia)
    entrada_nome.place(x=50, y=40)

    label_diretorio = tk.Label(tela_envia, text="Diretório: ").place(x=10, y=80)
    entrada_diretorio = tk.Entry(tela_envia)
    entrada_diretorio.place(x=40, y=80)

    botao_confirmar = tk.Button(tela_envia, text="Confirmar", width=10, command=confirma).place(x=200, y=150)
    tela_envia.mainloop()


def baixa_arquivo():
    tela_adiciona = tk.Tk()

    def confirma():
        if(entrada_arquivo.get() != ""):
            arquivo = server.fazerdownload(entrada_arquivo.get())
            with open(entrada_arquivo.get(), "w") as a:
                a.write(arquivo)
            tela_adiciona.destroy()
        else:
            print("Campo Vazio!")
        

    tela_adiciona.geometry("300x200")
    label_nome = tk.Label(tela_adiciona, text="Nome do arquivo: ").place(x=10, y=40)
    entrada_arquivo = tk.Entry(tela_adiciona)
    entrada_arquivo.place(x=50, y=40)

    botao_confirmar = tk.Button(tela_adiciona, text="Confirmar", width=10, command=confirma).place(x=200, y=150)

    tela_adiciona.mainloop()


def realiza_login():
    if(server.login_usuario(entrada_usuario.get(), entrada_senha.get())):
        menu_inicial.destroy()
        menu_principal = tk.Tk()
        

        menu_principal.title("Sistemas Distribuídos")
        menu_principal.geometry("600x400")
        
        label_arquivos = tk.Label(menu_principal, text="Arquivos disponíveis: ").place(x=30, y=20)
        label_interesses = tk.Label(menu_principal, text="Lista de Interesses: ").place(x=30, y=50)

        botao_baixar = tk.Button(menu_principal,
                                 text="Baixar",
                                 width=13,
                                 command=baixa_arquivo).place(x=490, y=360)

        botao_enviar = tk.Button(menu_principal,
                                 text="Enviar",
                                 width=13,
                                 command=enviar_arquivo).place(x=380, y=360)

        def recebe_interesse():
            tela_interesse = tk.Tk()

            def confirma():
                nome_arquivo = entrada_nome.get()
                server.recebe_interesse(nome_arquivo)
                tela_interesse.destroy()

            tela_interesse.geometry("300x200")
            label_nome = tk.Label(tela_interesse, text="Nome do arquivo: ").place(x=10, y=40)
            entrada_nome = tk.Entry(tela_interesse)
            entrada_nome.place(x=50, y=40)
            botao_confirma = tk.Button(tela_interesse, text= "Confirmar", width=10, command=confirma).place(x=200, y=150)

            tela_interesse.mainloop()

        botao_interesse = tk.Button(menu_principal,
                                 text="Interesses",
                                 width=13,
                                 command=recebe_interesse).place(x=270, y=360)
        
        def cancela_interesse():
            tela_cancela = tk.Tk()

            def confirma():
                nome_arquivo = entrada_nome.get()
                server.cancelar_interesse(nome_arquivo)
                tela_cancela.destroy()
            
            tela_cancela.geometry("300x200")
            label_nome = tk.Label(tela_cancela, text="Nome do arquivo: ").place(x=10, y=40)
            entrada_nome = tk.Entry(tela_cancela)
            entrada_nome.place(x=50, y=40)
            botao_confirma = tk.Button(tela_cancela, text= "Confirmar", width=10, command=confirma).place(x=200, y=150)

            tela_cancela.mainloop()

        botao_cancela = tk.Button(menu_principal,
                                 text="Cancelar",
                                 width=13,
                                 command=cancela_interesse).place(x=160, y=360)

        def atualiza_lista():
            arquivos = str(server.consultar())
            interesse = str(server.consulta_interesse())
            label_arquivos = tk.Label(menu_principal, text="Arquivos Disponíveis: " + arquivos).place(x=30, y=20)
            label_interesses = tk.Label(menu_principal, text="Lista de Interesses: " + interesse).place(x=30, y=50)

        botao_atualiza = tk.Button(menu_principal,
                                   text="Atualizar",
                                   width=13,
                                   command=atualiza_lista).place(x=50, y=360)

        menu_principal.mainloop()
    else:
        tela_erro = tk.Tk()
        tela_erro.geometry("300x150")
        tela_erro.title("Senha Incorreta")
        label_erro = tk.Label(tela_erro, text="Senha Incorreta!").place(x=120, y=30)
        botao_ok = tk.Button(tela_erro, text="Ok", width=10, command=tela_erro.destroy).place(x=120, y=80)

        tela_erro.mainloop()


def realiza_cadastro():
    if(server.cadastra_usuario(entrada_usuario.get(), entrada_senha.get())):
        tela_sucesso = tk.Tk()
        tela_sucesso.geometry("300x150")
        tela_sucesso.title("Cadastro Realizado")
        label_sucesso = tk.Label(tela_sucesso, text="Cadastro Realizado com sucesso!").place(x=80, y=30)
        botao_ok = tk.Button(tela_sucesso, text="Ok", width=10, command=tela_sucesso.destroy).place(x=120, y=80)

        tela_sucesso.mainloop()
    else:
        tela_erro = tk.Tk()
        tela_erro.geometry("300x150")
        tela_erro.title("Erro")
        label_erro = tk.Label(tela_erro, text="Preencha todos os campos!").place(x=120, y=30)
        botao_ok = tk.Button(tela_erro, text="Ok", width=10, command=tela_erro.destroy).place(x=120, y=80)

        tela_erro.mainloop()


menu_inicial = tk.Tk()

menu_inicial.title("Sistemas Distribuídos")
menu_inicial.geometry("400x400")

label_titulo = tk.Label(menu_inicial, text="Sistema distribuidos teste").place(x=125, y=10)

label_usuario = tk.Label(menu_inicial, text="Usuário:").place(x=100, y=100)
entrada_usuario = tk.Entry(menu_inicial)
entrada_usuario.place(x=150, y=100)

label_senha = tk.Label(menu_inicial, text="Senha:").place(x=100, y=150)
entrada_senha = tk.Entry(menu_inicial, width=20)
entrada_senha.place(x=150, y=150)

botao_login = tk.Button(menu_inicial, text='Login', width=30, command=realiza_login).place(x=100, y=250)
botao_cadastrar = tk.Button(menu_inicial, text='Cadastrar', width=13, command=realiza_cadastro).place(x=100, y=300)
botao_sair = tk.Button(menu_inicial, text='Sair', width=13,command=menu_inicial.destroy).place(x=220, y=300)

menu_inicial.mainloop()
