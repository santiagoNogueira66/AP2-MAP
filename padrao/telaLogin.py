import time
import padrao.telaPrincipal
import psycopg2
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, messagebox
from padrao.telaPrincipal import ProdutoView

class TelaLoginModel:

    @staticmethod
    def conectar_com_banco():
        try:
            conexao = psycopg2.connect(database='DBvendas', host='localhost', user='postgres', password='123456', port='5432')
            cursor = conexao.cursor()

            create = "CREATE TABLE IF NOT EXISTS usuarios(id serial PRIMARY KEY, nome_usuario varchar(255), senha varchar(255))"
            cursor.execute(create)

            return conexao, cursor

        except psycopg2.Error as err:
            print("erro ao conectar com o banco", err)
            return None, None

    @staticmethod
    def cadastrar_usuario(nome_usuario, senha):
        conexao, cursor = TelaLoginModel.conectar_com_banco()
        if conexao and cursor:
            try:
                insert = "INSERT INTO usuarios(nome_usuario, senha) VALUES (%s,%s)"
                cursor.execute(insert, (nome_usuario, senha))
                conexao.commit()

                msg = "usuario cadastrado com sucesso"
                messagebox.showinfo("sucesso", msg)

            except psycopg2.Error as err:
                print("erro ao inserir a senha e o usuario", err)

    @staticmethod
    def autenticar(nome_usuario, senha):
        conexao, cursor = TelaLoginModel.conectar_com_banco()
        if conexao and cursor:
            try:
                select = "SELECT nome_usuario, senha FROM usuarios WHERE nome_usuario = %s AND senha = %s"
                cursor.execute(select,(nome_usuario, senha))
                usuario = cursor.fetchone()
                if usuario:
                    messagebox.showinfo("sucesso", "autenticando")
                    root2 = tk.Toplevel(root)

                    #rode a tela principal dentro de root2
                    telaPrincipal = padrao.telaPrincipal.ProdutoView(root2)
                else:
                    messagebox.showinfo("erro", "acesso negado")
            except psycopg2.Error as err:
                print("erro ao exibir os dados do banco", err)

class TelaCadastroView:
    def __init__(self, root):
        self.fontePadrao = ("Arial", "12")
        self.root = root

        self.cadastro_window = tk.Toplevel(self.root) # Toplevel serve para criar janelas separadas da tela principal
        self.cadastro_window.title("Cadastro")
        self.cadastro_window.geometry("400x300")
        self.cadastro_window.resizable(False, False)
        self.cadastro_window.configure(background="#514d4d")

        self.primeiroContainer = Frame(self.cadastro_window, bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.primeiroContainer["pady"] = 10 #espaçamento interno na vertical
        self.primeiroContainer.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        self.titulo = Label(self.primeiroContainer, text="Cadastro", bg="#081D3C", fg="white")
        self.titulo["font"] = ("Arial", "15", "bold", "italic")
        self.titulo.place(relx=0.5, rely=0.1, anchor="center")

        self.usuarioLabel = Label(self.primeiroContainer, text="Usuário", font=self.fontePadrao, bg="#081D3C", fg="white")
        self.usuarioLabel.place(relx=0.5, rely=0.2, anchor="center")

        self.usuarioEntry = Entry(self.primeiroContainer, font=self.fontePadrao)
        self.usuarioEntry["width"] = 25
        self.usuarioEntry.place(relx=0.5, rely=0.3, anchor="center")

        self.senhaLabel = Label(self.primeiroContainer, text="Senha", font=self.fontePadrao, bg="#081D3C", fg="white")
        self.senhaLabel.place(relx=0.5, rely=0.5, anchor="center")

        self.senhaEntry = Entry(self.primeiroContainer, font=self.fontePadrao)
        self.senhaEntry["width"] = 25
        self.senhaEntry["show"] = "*"
        self.senhaEntry.place(relx=0.5, rely=0.6, anchor="center")

        self.cadastrar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.cadastrar["text"] = "Cadastrar"
        self.cadastrar["font"] = self.fontePadrao
        self.cadastrar["width"] = 10
        self.cadastrar["command"] = self.cadastrar_usuario
        self.cadastrar.place(relx=0.5, rely=0.9, anchor="center")

    def limpar_entrys(self):
        self.usuarioEntry.delete(0,tk.END)
        self.senhaEntry.delete(0, tk.END)

    def cadastrar_usuario(self):
        TelaLoginController.cadastrar_usuario(self.usuarioEntry, self.senhaEntry)
        self.cadastro_window.lift() # lift "prega" a tela de cadastro
        self.limpar_entrys() # passamos o zero e o end pra dizer que ele vai excluir do inicio ao final

class TelaLoginView:
    def __init__(self, root):
        self.fontePadrao = ("Arial", "20")
        self.fonteEntrys = ("Arial", "25")
        self.root = root
        self.root.title("Tela de login")
        self.root.configure(background="#514d4d")
        self.root.geometry("1000x500")
        self.root.resizable(False, False)

        self.primeiroContainer = Frame(root,bd=4,bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.place(relx=0.10, rely=0.10, relwidth=0.8,relheight=0.8)

        self.titulo = Label(self.primeiroContainer, text="Login", bg="#081D3C", fg="white")
        self.titulo["font"] = ("Arial", "15", "bold", "italic")
        self.titulo.place(relx=0.5, rely=0.10, anchor="center")

        self.usuarioLabel = Label(self.primeiroContainer, text="Usuário", font=self.fontePadrao, bg="#081D3C", fg="white")
        self.usuarioLabel.place(relx=0.20, rely=0.30, anchor="center")

        self.usuarioEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.usuarioEntry["width"] = 25
        self.usuarioEntry.place(relx=0.60, rely=0.30, anchor="center")

        self.senhaLabel = Label(self.primeiroContainer, text="Senha", font=self.fontePadrao, bg="#081D3C", fg="white")
        self.senhaLabel.place(relx=0.20, rely=0.55, anchor="center")

        self.senhaEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.senhaEntry["width"] = 25
        self.senhaEntry["show"] = "*"
        self.senhaEntry.place(relx=0.60, rely=0.55, anchor="center")

        self.entrar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.entrar["text"] = "Entrar"
        self.entrar["font"] = self.fontePadrao
        self.entrar["width"] = 10
        self.entrar["command"] = self.autenticar
        self.entrar.place(relx=0.5, rely=0.90, anchor="center")

        self.cadastroButton = Button(self.primeiroContainer, text="Cadastro", command=self.abrir_tela_cadastro, bd=2, bg="#7f8fff")
        self.cadastroButton["width"] = 10
        self.cadastroButton.place(relx=0.5, rely=0.75, anchor="center")

    def limpar_entrys(self):
        self.usuarioEntry.delete(0, tk.END) #passamos o zero e o end pra dizer que ele vai excluir do inicio ao final
        self.senhaEntry.delete(0, tk.END)

    def autenticar(self):
        TelaLoginController.autenticar(self.usuarioEntry, self.senhaEntry)
        self.limpar_entrys()

    def abrir_tela_cadastro(self):
        tela_cadastro = TelaCadastroView(self.root)

class TelaLoginController:

    @staticmethod
    def autenticar(usuarioEntry, senhaEntry):
        nome_usuario = usuarioEntry.get()
        senha = senhaEntry.get()

        TelaLoginModel.autenticar(nome_usuario, senha)

    @staticmethod
    def cadastrar_usuario(usuarioEntry, senhaEntry):
        nome_usuario = usuarioEntry.get()
        senha = senhaEntry.get()

        TelaLoginModel.cadastrar_usuario(nome_usuario, senha)

if __name__ == "__main__":
    root = tk.Tk()
    TelaLoginView(root)
    root.mainloop()