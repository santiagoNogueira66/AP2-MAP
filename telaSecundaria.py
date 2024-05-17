import time
import psycopg2
import datetime
import webbrowser
import padrao.relatorioDeLucro
from padrao.relatorioDeLucro import RelatorioModel
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox
from ttkthemes import ThemedStyle


class GastosModel:
    @staticmethod
    def conectar_com_banco():
        try:
            conexao = psycopg2.connect(database='DBvendas', host='localhost', user='postgres', password='123456',
                                       port='5432')
            cursor = conexao.cursor()

            create = "CREATE TABLE IF NOT EXISTS gastos (id SERIAL PRIMARY KEY, nome_gasto VARCHAR(255) NOT NULL, valor_gasto DECIMAL NOT NULL, data_gasto VARCHAR(255))"

            cursor.execute(create)

            return conexao, cursor

        except psycopg2.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return None, None

    @staticmethod
    def inserir_gastos(gastos, view_instance):
        conexao, cursor =  GastosModel.conectar_com_banco()
        if conexao and cursor:
            try:
                if all(gastos):
                    insert = "INSERT INTO gastos(nome_gasto, valor_gasto, data_gasto) VALUES (%s, %s ,%s)"
                    cursor.execute(insert, gastos)
                    conexao.commit()
                    msg = "Gastos Registrados!"
                    messagebox.showinfo("SUCESSO", msg)
                    view_instance.exibir_dados_do_banco()
                else:
                    msg = "valor e nome dos gastos são obrigatórios"
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
       conexao , cursor = GastosModel.conectar_com_banco()
       if conexao and cursor:
           try:
               cursor.execute("SELECT * FROM gastos")
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
    def editar_gastos(gastos_atualizados, view_instance):
        conexao, cursor = GastosModel.conectar_com_banco()
        if conexao and cursor:
            try:
                update = "UPDATE gastos SET nome_gasto= %s, valor_gasto= %s, data_gasto=%s WHERE id = %s"
                cursor.execute(update, gastos_atualizados)
                conexao.commit()
                view_instance.exibir_dados_do_banco()
            except psycopg2.Error as err:
                print("Erro ao editar os dados do banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

    @staticmethod
    def excluir_gastos(gastos):
        conexao, cursor = GastosModel.conectar_com_banco()
        if conexao and cursor:
            try:
                id_gastos = gastos[0]
                delete = "DELETE FROM gastos WHERE id = %s"
                cursor.execute(delete, (id_gastos,))
                conexao.commit()
            except psycopg2.Error as err:
                print("Erro ao excluir dados do banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

    @staticmethod
    def calcular_lucro():
        RelatorioModel.gerar_relatorio_pdf()
        time.sleep(2)
        GastosModel.abrir_pdf()

    @staticmethod
    def abrir_pdf():
        webbrowser.open("relatorio.pdf")

class GastosView:
    def __init__(self, root):
        self.fontepadrao = ("Arial", "20")
        self.fonteEntrys = ("Arail", "25")
        self.root = root
        self.root.title("Gerenciamento de Gastos em uma casa de ração")
        self.root.configure(background="#514d4d")
        self.root.geometry("1300x600")
        self.root.resizable(True, True)

        self.primeiroContainer = Frame(root, bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.place(relx=0.10, rely=0.10, relwidth=0.8, relheight=0.60)

        self.segundoContainer = Frame(root, bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.segundoContainer["pady"] = 10
        self.segundoContainer.place(relx=0.10, rely=0.70, relwidth=0.80, relheight=0.30)

        self.titulo = Label(self.primeiroContainer, text="Gerenciamento de Gastos", bg="#081D3C", fg="white")
        self.titulo['font'] = ("Arial", "15", "bold", "italic")
        self.titulo.place(relx=0.5, rely=0.10, anchor="center")

        self.nomeGastoLabel = Label(self.primeiroContainer, text="Nome do Gasto", font=self.fontepadrao, bg="#081D3C", fg="white")
        self.nomeGastoLabel.place(relx=0.20, rely=0.30, anchor="center")

        self.nomeGastoEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.nomeGastoEntry["width"] = 25
        self.nomeGastoEntry.place(relx=0.65, rely=0.30, anchor="center")

        self.precoGastoLabel = Label(self.primeiroContainer, text="Valor do Gasto", font=self.fontepadrao , bg="#081D3C", fg="white")
        self.precoGastoLabel.place(relx=0.20, rely=0.45, anchor="center")

        self.precoGastoEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.precoGastoEntry["width"] = 25
        self.precoGastoEntry.place(relx=0.65, rely=0.50, anchor="center")

        self.dataAtual = datetime.datetime.now().strftime("%d/%m/%Y")

        self.dataLabel = Label(self.primeiroContainer, text="Data: " + self.dataAtual, font=("calibri", "25"), bg="#081D3C", fg="white")
        self.dataLabel.place(relx=0.6, rely=0.70, anchor="e")

        self.gastar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.gastar["text"] = "Gastar"
        self.gastar["font"] = self.fontepadrao
        self.gastar["width"] = 10
        self.gastar["command"] = lambda: self.inserir_gastos(self)
        self.gastar.place(relx=0.1, rely=0.9, anchor="center")

        self.editar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.editar["text"] = "Editar"
        self.editar["font"] = self.fontepadrao
        self.editar["width"] = 10
        self.editar["command"] = self.editar_gastos
        self.editar.place(relx=0.3, rely=0.9, anchor="center")

        self.excluir = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.excluir["text"] = "Excluir"
        self.excluir["font"] = self.fontepadrao
        self.excluir["width"] = 10
        self.excluir["command"] = lambda: self.confirmar_exclusao(self.gastos_selecionados)
        self.excluir.place(relx=0.7, rely=0.9, anchor="center")

        self.limpar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.limpar["text"] = "Limpar"
        self.limpar["font"] = self.fontepadrao
        self.limpar["width"] = 10
        self.limpar["command"] = self.limpar_entrys
        self.limpar.place(relx=0.9, rely=0.9, anchor="center")

        self.lucro = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.lucro["text"] = "lucros"
        self.lucro["font"] = self.fontepadrao
        self.lucro["width"] = 10
        self.lucro["command"] = self.calcular_lucro
        self.lucro.place(relx=0.5, rely=0.9, anchor="center")

        style = ThemedStyle()
        style.configure("Treeview", font=("arial", 15), background="#081D3C", foreground="white", fieldbackground="#081D3C")

        self.minha_lista = ttk.Treeview(self.segundoContainer, height=5, columns=("col1", "col2", "col3", "col4"))
        self.minha_lista.heading("col1", text="ID",)
        self.minha_lista.heading("col2", text="Nome do Gasto")
        self.minha_lista.heading("col3", text="Valor do Gasto")
        self.minha_lista.heading("col4", text="Data do Gasto")

        self.minha_lista.column("col1", width=50, anchor=tk.CENTER)
        self.minha_lista.column("col2", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col3", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col4", width=100, anchor=tk.CENTER)

        yscrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.minha_lista.yview)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.minha_lista.configure(yscrollcommand=yscrollbar.set)

        self.minha_lista.pack(expand=True, fill=tk.BOTH)

        self.exibir_dados_do_banco()

        self.minha_lista.bind("<Double-1>", self.double_click)

    def limpar_entrys(self):
        self.nomeGastoEntry.delete(0,tk.END)
        self.precoGastoEntry.delete(0, tk.END)

    def confirmar_exclusao(self, gastos_selecionados):
        if gastos_selecionados:
            resposta = messagebox.askquestion("CONFIRMAÇÃO", "DESEJA REALMENTE EXCLUIR O GASTO ?")
            if resposta == "yes":
                id_gasto = gastos_selecionados[0]
                GastosController.excluir_gastos(gastos_selecionados)
                messagebox.showinfo("Sucesso", "gasto excluído com sucesso")
                self.exibir_dados_do_banco()
                self.limpar_entrys()
            else:
                messagebox.showinfo("Cancelado", "Exclusão cancelada")
                self.limpar_entrys()
        else:
            messagebox.showinfo("Erro", "Nenhum item selecionado para excluir.")

    def double_click(self, event=None):
        gastos_selecionado = self.minha_lista.selection()[0]
        self.gastos_selecionados = self.minha_lista.item(gastos_selecionado, "values")
        self.nomeGastoEntry.delete(0, tk.END)
        self.nomeGastoEntry.insert(0, self.gastos_selecionados[1])
        self.precoGastoEntry.delete(0, tk.END)
        self.precoGastoEntry.insert(0, self.gastos_selecionados[2])

    def exibir_dados_do_banco(self):
        dados_do_banco = GastosModel.obter_dados_do_banco()
        if dados_do_banco:
            for item in self.minha_lista.get_children():
                self.minha_lista.delete(item)
            for row in dados_do_banco:
                self.minha_lista.insert("", tk.END, values=row)

    def obter_gastos(self):
        nome_gasto = self.nomeGastoEntry.get()
        valor_gasto = self.precoGastoEntry.get()
        data_gasto = self.dataAtual
        gastos = (nome_gasto, valor_gasto, data_gasto)
        return gastos

    def inserir_gastos(self, view_instance):
        gastos = self.obter_gastos()
        GastosController.inserir_gastos(gastos, view_instance)
        self.limpar_entrys()

    def editar_gastos(self):
        if self.gastos_selecionados:
            gastos_atualizados = self.obter_gastos()
            gastos_atualizados += (self.gastos_selecionados[0],)
            GastosController.editar_gastos(gastos_atualizados, self)
            msg = "Os gastos foram atualizados com sucesso"
            messagebox.showinfo("Gastos Alterados", msg)
            self.limpar_entrys()
        else:
            messagebox.showinfo("Erro", "Nenhum item selecionado para editar.")


    def excluir_gastos(self):
        gastos_selecionado = self.minha_lista.selection()[0]
        gastos_selecionados = self.minha_lista.item(gastos_selecionado, "values")
        GastosModel.excluir_gastos(gastos_selecionados)

    def calcular_lucro(self):
        GastosController.calcular_lucro()

class GastosController:

    @staticmethod
    def inserir_gastos(gastos, view_instance):
        GastosModel.inserir_gastos(gastos, view_instance)

    @staticmethod
    def editar_gastos(gastos, view_instance):
        GastosModel.editar_gastos(gastos, view_instance)

    @staticmethod
    def excluir_gastos(gastos_selecionados):
       GastosModel.excluir_gastos(gastos_selecionados)
    @staticmethod
    def calcular_lucro():
        GastosModel.calcular_lucro()

if __name__ == "__main__":
    root = tk.Tk()
    GastosView(root)
    root.mainloop()



