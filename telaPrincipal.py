import psycopg2
import datetime
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox


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
    def salvar_no_Banco(dados, view_instance):
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

class ProdutoView:
    def __init__(self, root):
        self.fontepadrao = ("Arial", "12")
        self.root = root

        self.primeiroContainer = Frame(root)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(root)
        self.segundoContainer["padx"] = 20
        self.segundoContainer["pady"] = 10
        self.segundoContainer.pack()

        self.terceirocontainer = Frame(root)
        self.terceirocontainer["padx"] = 20
        self.terceirocontainer.pack()

        self.quartoContainer = Frame(root)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(root)
        self.quintoContainer["padx"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(root)
        self.sextoContainer["padx"] =20
        self.sextoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Gerenciamento de Vendas")
        self.titulo['font'] = ("Arial", "15", "bold")
        self.titulo.pack()

        self.nomeProdutoLabel = Label(self.segundoContainer, text="Nome do Produto", font=self.fontepadrao)
        self.nomeProdutoLabel.pack(side=tk.LEFT)

        self.nomeProdutoEntry = Entry(self.segundoContainer)
        self.nomeProdutoEntry["width"] = 50
        self.nomeProdutoEntry.pack(side=tk.LEFT)

        self.precoProdutoLabel = Label(self.terceirocontainer, text="Preço do Produto", font=self.fontepadrao)
        self.precoProdutoLabel.pack(side=tk.LEFT)

        self.precoProdutoEntry = Entry(self.terceirocontainer)
        self.precoProdutoEntry["width"] = 50
        self.precoProdutoEntry.pack(side=tk.LEFT)

        self.dataLabel = Label(self.quartoContainer, text="Data", font=("calibri", "15"))
        self.dataLabel.pack(side=tk.LEFT)

        self.dataAtual = datetime.datetime.now().strftime("%d/%m/%Y")
        self.dataProdutoLabel = Label(self.quartoContainer, text=self.dataAtual, font=("calibri", "15"))
        self.dataProdutoLabel.pack(side=tk.LEFT)

        self.vender = Button(self.quintoContainer)
        self.vender["text"] = "Vender"
        self.vender["font"] = ("Arial", "12")
        self.vender["width"] = 10
        self.vender["command"] = lambda:self.obter_dados(self)
        self.vender.pack(pady=10)

        self.minha_lista = ttk.Treeview(self.sextoContainer, height=5, columns=("col1","col2","col3","col4"))
        self.minha_lista.heading("col1", text="ID")
        self.minha_lista.heading("col2", text="Nome do produto")
        self.minha_lista.heading("col3", text="Preço do produto")
        self.minha_lista.heading("col4", text="Data da venda")

        self.minha_lista.column("col1", width=100, anchor=tk.CENTER)
        self.minha_lista.column("col2", width=200, anchor=tk.CENTER)
        self.minha_lista.column("col3", width=300, anchor=tk.CENTER)
        self.minha_lista.column("col4", width=400, anchor=tk.CENTER)
        self.minha_lista.pack(expand=True, fill=tk.BOTH)

        self.exibir_dados_do_banco()

    def exibir_dados_do_banco(self):
        dados_do_banco = ProdutoModel.obter_dados_do_banco()
        if dados_do_banco:
            for item in self.minha_lista.get_children():
                self.minha_lista.delete(item)
            for row in dados_do_banco:
                self.minha_lista.insert("", tk.END, values=row)

    def obter_dados(self, view_instance):
        nome_produto = self.nomeProdutoEntry.get()
        preco_produto = self.precoProdutoEntry.get()
        data_venda = self.dataProdutoLabel["text"]

        dados = (nome_produto, preco_produto, data_venda)
        ProdutoController.inserir_dados(dados, view_instance)


class ProdutoController:
    @staticmethod
    def inserir_dados(dados, view_instance):
        ProdutoModel.salvar_no_Banco(dados, view_instance)


if __name__ == "__main__":
    root = tk.Tk()
    ProdutoView(root)
    root.mainloop()
