import tkinter as tk
from tkinter import ttk, Frame

class Listagem():
    def __init__(self, root):
      self.root = root
      self.fontePadrao = ("Arial, 10")

      self.primeiroContainer = Frame(root)
      self.primeiroContainer["pady"] = 100
      self.primeiroContainer["padx"] = 100
      self.primeiroContainer.pack()

      self.listagem = ttk.Treeview(self.primeiroContainer, height=3, columns=("col1", "col2", "col3", "col4"))
      self.listagem.heading("col1", text="ID")
      self.listagem.heading("col2", text="Nome do Produto")
      self.listagem.heading("col3", text="Preço do produto")
      self.listagem.heading("col4", text="Data da Venda")

      self.listagem.column("col1", width="200")
      self.listagem.column("col2", width="100")
      self.listagem.column("col3", width="100")
      self.listagem.column("col4", width="100")

      self.listagem.insert("", tk.END, values=("1", "Produto A", "$10.00", "2024-04-21"))
      self.listagem.insert("", tk.END, values=("2", "Produto B", "$20.00", "2024-04-22"))
      self.listagem.pack(expand=True, fill=tk.BOTH)


root = tk.Tk()
Listagem(root)
root.mainloop()