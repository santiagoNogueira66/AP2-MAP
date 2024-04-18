import mysql.connector
from mysql.connector import  errors
import tkinter as tk
import datetime
from tkinter import Frame, Label, Entry, Button


class ProdutoView:
    def __init__(self, root):
        self.fontepadrao = ("Arial", "10")
        self.root = root

        self.primeiroContainer = Frame(root)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(root)
        self.segundoContainer["padx"] = 20
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

        self.titulo = Label(self.primeiroContainer, text="Gerenciamento de Vendas")
        self.titulo['font'] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nomeProdutoLabel = Label(self.segundoContainer, text="Nome do Produto", font=self.fontepadrao)
        self.nomeProdutoLabel.pack(side=tk.LEFT)

        self.nomeProduto = Entry(self.segundoContainer)
        self.nomeProduto["width"] = 30
        self.nomeProduto.pack(side=tk.LEFT)

        self.precoProdutoLabel = Label(self.terceirocontainer, text="Preço do Produto", font=self.fontepadrao)
        self.precoProdutoLabel.pack(side=tk.LEFT)

        self.precoProduto = Entry(self.terceirocontainer)
        self.precoProduto["width"] = 30
        self.precoProduto.pack(side=tk.LEFT)

        self.dataLabel = Label(self.quartoContainer, text="Data", font=self.fontepadrao)
        self.dataLabel.pack(side=tk.LEFT)

        self.dataAtual = datetime.datetime.now().strftime("%y/%m/%d")
        self.dataProdutoLabel = Label(self.quartoContainer, text=self.dataAtual, font=self.fontepadrao)
        self.dataProdutoLabel.pack(side=tk.LEFT)

        self.vender = Button(self.quintoContainer)
        self.vender["text"] = "Vender"
        self.vender["width"] = 12
        self.vender["command"] = self.salvar_no_Banco
        self.vender.pack(pady = 10)

    def salvar_no_Banco(self):
        nome_produto = self.nomeProduto.get()
        preco_produto = self.precoProduto.get()
        data_venda = self.dataProdutoLabel["text"]
        ProdutoController.salvar_no_Banco(nome_produto, preco_produto, data_venda)


class ProdutoController:
    @staticmethod
    def salvar_no_Banco(nome_produto, preco_produto, data_venda):
     try:
        con = mysql.connector.connect(host='localhost',database='vendas',user='root',password='coxinha0p0p67')
        cursor = con.cursor()


        query = "insert into produtos(nome_produto, preco_produto, data_venda) values (%s, %s ,%s)"

        cursor.execute(query,(nome_produto, preco_produto, data_venda))

        con.commit()

        print(cursor.rowcount,"registros na tabela")

     except mysql.connector.Error as err:
      print("Erro ao inserir na tabela:", err)

     finally:
         if con.is_connected():
            cursor.close()
            con.close()
            print("conexão encerrada")

root = tk.Tk()
ProdutoView(root)
root.mainloop()

