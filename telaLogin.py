from tkinter import *
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.containerUm = Frame(master)
        self.containerUm["pady"] = 10
        self.containerUm.pack()

        self.containerDois = Frame(master)
        self.containerDois["padx"] = 20
        self.containerDois.pack()

        self.containerTres = Frame(master)
        self.containerTres["padx"] = 20
        self.containerTres.pack()

        self.containerQuatro = Frame(master)
        self.containerQuatro["pady"] = 20
        self.containerQuatro.pack()

        self.titulo = Label(self.containerUm, text="Login")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.emailLabel = Label(self.containerDois, text="email", font=self.fontePadrao )
        self.emailLabel.pack(side=LEFT)

        self.email = Entry(self.containerDois)
        self.email["width"] = 30
        self.email["font"] = self.fontePadrao
        self.email.pack(side=LEFT)

        self.senhaLabel = Label(self.containerTres, text="senha", font=self.fontePadrao)
        self.senhaLabel.pack(side=LEFT)

        self.senha = Entry(self.containerTres)
        self.senha["width"] = 30
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.pack(side=LEFT)

        self.entrar = Button(self.containerQuatro)
        self.entrar["text"] = "Entrar"
        self.entrar["font"] = ("Calibri", "8")
        self.entrar["width"] = 12
        self.entrar["command"] = self.verificarSenha
        self.entrar.pack()

        self.mensagem = Label(self.containerQuatro, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def verificarSenha(self):
        usuario = self.email.get()
        senha = self.senha.get()
        if usuario == "email" and senha == "dev":
            self.mensagem["text"] = "Autenticado"
        else:
            self.mensagem["text"] = "Erro na autenticação"

root = Tk()
Application(root)
root.mainloop()