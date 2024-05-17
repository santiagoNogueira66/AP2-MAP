import psycopg2
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.styles import ParagraphStyle


class RelatorioModel:

    @staticmethod
    def conectar_com_banco():
        try:
            conexao = psycopg2.connect(database='DBvendas', host='localhost', user='postgres', password='123456', port='5432')
            cursor = conexao.cursor()
            return conexao, cursor
        except psycopg2.Error as err:
            print("Erro ao conectar ao banco de dados:", err)

    @staticmethod
    def recuperar_dados_vendas():
        conexao, cursor = RelatorioModel.conectar_com_banco()
        if conexao and cursor:
            try:
                cursor.execute("SELECT * FROM produtos")
                dados_vendas = cursor.fetchall()
                return dados_vendas
            except psycopg2.Error as err:
                print("Erro ao recuperar os dados de vendas:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

    @staticmethod
    def recuperar_dados_gastos():
        conexao, cursor = RelatorioModel.conectar_com_banco()
        if conexao and cursor:
            try:
                cursor.execute("SELECT * FROM gastos")
                dados_gastos = cursor.fetchall()
                return dados_gastos
            except psycopg2.Error as err:
                print("Erro ao recuperar os dados de gastos:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

    @staticmethod
    def somar_lucros():
        conexao, cursor = RelatorioModel.conectar_com_banco()
        if conexao and cursor:
            try:
                cursor.execute("SELECT SUM(preco_produto) FROM produtos")
                total_de_vendas = cursor.fetchone()[0] or 0

                return  total_de_vendas
            except psycopg2.Error as err:
                print("erro ao somar as venda totais", err)

            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

    @staticmethod
    def somar_gastos():
        conexao, cursor = RelatorioModel.conectar_com_banco()
        if conexao and cursor:
            try:
                cursor.execute("SELECT SUM(valor_gasto) FROM gastos")
                total_de_gastos = cursor.fetchone()[0] or 0

                return total_de_gastos

            except psycopg2.Error as err:
                print("erro ao somar os gastos totais", err)

            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

    @staticmethod
    def calcular_lucros_totais():

        total_de_vendas = RelatorioModel.somar_lucros()
        total_de_gastos = RelatorioModel.somar_gastos()
        lucro_total = total_de_vendas - total_de_gastos

        return lucro_total

    @staticmethod
    def gerar_relatorio_pdf():
        dados_vendas = RelatorioModel.recuperar_dados_vendas()
        dados_gastos = RelatorioModel.recuperar_dados_gastos()
        total_de_vendas = RelatorioModel.somar_lucros()
        total_de_gastos = RelatorioModel.somar_gastos()
        lucro_total = RelatorioModel.calcular_lucros_totais()

        if dados_vendas is not None and dados_gastos is not None and lucro_total is not None:

            # Cria um novo arquivo pdf
            doc = SimpleDocTemplate("relatorio.pdf", pagesize=letter)

            # Cria listas vazias para a tabela
            table_vendas = []
            table_gastos = []

            # Adiciona da tabela de vendas à tabela
            for venda in dados_vendas:
                table_vendas.append([venda[1], venda[2], venda[3]])

            # Adiciona da tabela de gastos à tabela
            for gasto in dados_gastos:
                table_gastos.append([gasto[1], gasto[2], gasto[3]])

            # Adiciona o cabeçalho das tabelas
            table_vendas.insert(0, ["Nome do Produto", "Preço", "Data da Venda"])
            table_gastos.insert(0, ["Nome do Gasto", "Valor", "Data do Gasto"])

            # Adiciona uma linha para o total de vendas e o total de gastos como o último item das tabelas
            table_vendas.append(["Total de Vendas:", f"R$ {total_de_vendas:.2f}", ""])
            table_gastos.append(["Total de Gastos:", f"R$ {total_de_gastos:.2f}", ""])

            # Estilo das tabelas
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            style2 = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                 ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            # Cria as tabelas
            table_vendas = Table(table_vendas)
            table_gastos = Table(table_gastos)

            # Aplica o estilo nas tabelas
            table_vendas.setStyle(style)
            table_gastos.setStyle(style2)

            # Adiciona um espaço vertical entre as tabelas
            espaco_vertical = Spacer(1, 15)

            # Adiciona um espaço vazio entre o lucro total
            espaco_vazio = Spacer(1, 20)

            # Define um estilo de parágrafo para o lucro total
            style_lucro_total = ParagraphStyle(
                name="LucroTotalStyle",
                alignment=1,  # 0=esquerda, 1=centro, 2=direita
                fontSize=14
            )

            # Adiciona o lucro total como um objeto de texto formatado
            lucro_total_text = Paragraph(f"<b>Lucro Total:</b> R$ {lucro_total:.2f}", style_lucro_total)

            # Adiciona as tabelas, o lucro total e os espaçamentos ao pdf
            elements = [table_vendas, espaco_vertical, table_gastos, espaco_vazio, lucro_total_text]

            # Gera o pdf
            doc.build(elements)
            print("Relatório PDF gerado com sucesso.")

        else:
            print("Não foi possível gerar o relatório PDF.")

