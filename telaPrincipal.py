import psycopg2
import datetime
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox
from ttkthemes import ThemedStyle



class ProdutoModel:
    @staticmethod
    def conectar_com_banco():
        try:
            conexao = psycopg2.connect(database='DBvendas', host='localhost', user='postgres', password='123456',
                                       port='5432')
            cursor = conexao.cursor()
            return conexao, cursor
        except psycopg2.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return None, None

    @staticmethod
    def inserir_dados(dados, view_instance):
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                if all(dados):
                    insert = "INSERT INTO produtos(nome_produto, preco_produto, data_venda) VALUES (%s, %s ,%s)"
                    cursor.execute(insert, dados)
                    conexao.commit()
                    msg = "VENDA FINALIZADA!"
                    messagebox.showinfo("SUCESSO", msg)
                    # Atualizar a Treeview após a inserção de dados
                    view_instance.exibir_dados_do_banco()  # Chamar o método na instância existente da ProdutoView
                else:
                    msg = "PREÇO E NOME DO PRODUTO SÃO OBRIGATÓRIOS"
                    messagebox.showinfo("PREENCHA TODOS OS CAMPOS!", msg)
            except psycopg2.Error as err:
                print("Erro ao inserir dados no banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

    @staticmethod
    def obter_dados_do_banco():
       conexao , cursor = ProdutoModel.conectar_com_banco()
       if conexao and cursor:
           try:
               cursor.execute("SELECT * FROM produtos")
               return  cursor.fetchall()

           except psycopg2.Error as err:
               print("erro ao obter dados do banco", err)

           finally:
               if cursor:
                   cursor.close()
               if conexao:
                   conexao.close()

       else:
           print("Não foi possível conectar ao banco de dados.")
           return None

    @staticmethod
    def editar_dados(dados):
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                update = "UPDATE produtos SET nome_produto = %s, preco_produto = %s, data_venda = %s WHERE id = %s"
                cursor.execute(update, dados)
            except psycopg2.Error as err:
                   print("erro ao editar os dados do banco", err)

            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

class ProdutoView:
    def __init__(self, root):
        self.fontepadrao = ("Arial", "12")
        self.root = root
        self.root.configure(background="#514d4d")
        self.root.geometry("1300x600")
        self.root.resizable(True, True)
        # self.root.maxsize(width=1500, height=450)
        # self.root.minsize(width=800, height=400)

        self.primeiroContainer = Frame(root,bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.place(relx=0.20, rely=0.10, relwidth=0.5, relheight=0.50)

        self.segundoContainer = Frame(root,bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.segundoContainer["pady"] = 10
        self.segundoContainer.place(relx=0.20, rely=0.60, relwidth=0.50, relheight=0.30)

        self.titulo = Label(self.primeiroContainer, text="Gerenciamento de Vendas", bg="#081D3C", fg="white")
        self.titulo['font'] = ("Arial", "15", "bold", "italic")
        self.titulo.place(relx=0.5, rely=0.10, anchor="center")

        self.nomeProdutoLabel = Label(self.primeiroContainer, text="Nome do Produto", font=self.fontepadrao, bg="#081D3C", fg="white")
        self.nomeProdutoLabel.place(relx=0.20, rely=0.30, anchor="center")

        self.nomeProdutoEntry = Entry(self.primeiroContainer)
        self.nomeProdutoEntry["width"] = 50
        self.nomeProdutoEntry.place(relx=0.65, rely=0.30, anchor="center")

        self.precoProdutoLabel = Label(self.primeiroContainer, text="Preço do Produto", font=self.fontepadrao , bg="#081D3C", fg="white")
        self.precoProdutoLabel.place(relx=0.20, rely=0.45, anchor="center")

        self.precoProdutoEntry = Entry(self.primeiroContainer)
        self.precoProdutoEntry["width"] = 50
        self.precoProdutoEntry.place(relx=0.65, rely=0.45, anchor="center")

        self.dataAtual = datetime.datetime.now().strftime("%d/%m/%Y")

        self.dataLabel = Label(self.primeiroContainer, text="Data: " + self.dataAtual, font=("calibri", "15"), bg="#081D3C", fg="white")
        self.dataLabel.place(relx=0.6, rely=0.60, anchor="e")

        self.vender = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.vender["text"] = "Vender"
        self.vender["font"] = self.fontepadrao
        self.vender["width"] = 10
        self.vender.place(relx=0.20, rely=0.90, anchor="center")

        self.editar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.editar["text"] = "Editar"
        self.editar["font"] = self.fontepadrao
        self.editar["width"] = 10
        self.editar.place(relx=0.50, rely=0.90, anchor="center")

        self.excluir = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.excluir["text"] = "Excluir"
        self.excluir["font"] = self.fontepadrao
        self.excluir["width"] = 10
        self.excluir.place(relx=0.80, rely=0.90, anchor="center")

        style = ThemedStyle()
        style.configure("Treeview", background="#081D3C", foreground="white", fieldbackground="#081D3C")

        self.minha_lista = ttk.Treeview(self.segundoContainer, height=5, columns=("col1", "col2", "col3", "col4"))
        self.minha_lista.heading("col1", text="ID")
        self.minha_lista.heading("col2", text="Nome do produto")
        self.minha_lista.heading("col3", text="Preço do produto")
        self.minha_lista.heading("col4", text="Data da venda")

        self.minha_lista.column("col1", width=50, anchor=tk.CENTER)
        self.minha_lista.column("col2", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col3", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col4", width=100, anchor=tk.CENTER)
        self.minha_lista.pack(expand=True, fill=tk.BOTH)

        self.exibir_dados_do_banco()

    def exibir_dados_do_banco(self):
        dados_do_banco = ProdutoModel.obter_dados_do_banco()
        if dados_do_banco:
            for item in self.minha_lista.get_children():
                self.minha_lista.delete(item)
            for row in dados_do_banco:
                self.minha_lista.insert("", tk.END, values=row)

    def obter_dados(self):
        nome_produto = self.nomeProdutoEntry.get()
        preco_produto = self.precoProdutoEntry.get()
        data_venda = self.dataProdutoLabel["text"]

        dados = (nome_produto, preco_produto, data_venda)
        return dados

    def inserir_dados(self):
        dados = self.obter_dados()
        ProdutoController.inserir_dados(dados, self)

    def editar_dados(self):
        dados = self.obter_dados()
        ProdutoController.editar_dados(dados, self)


class ProdutoController:

    @staticmethod
    def inserir_dados(dados, view_instance):
        ProdutoModel.inserir_dados(dados, view_instance)

    @staticmethod
    def editar_dados(dados, view_instance):
        ProdutoModel.editar_dados(dados)


if __name__ == "__main__":
    root = tk.Tk()
    ProdutoView(root)
    root.mainloop()
