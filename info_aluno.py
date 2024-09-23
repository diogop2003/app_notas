import tkinter as tk
from tkinter import messagebox
import sqlite3


class InformacoesAluno:

    def __init__(self, root, id_selecionado):
        self.root = root
        self.id_selecionado = id_selecionado  # Armazena o ID do aluno
            
    def criar_formulario(self):
        '''
        Essa função cria a janela de informações sobre o aluno selecionado

        '''
        
        
        self.janela_form = tk.Toplevel()
        self.janela_form.title("EDITAR ALUNO")
        self.janela_form.geometry("500x400")
        self.janela_form.config(bg='gray')
        self.janela_form.resizable(False, False)
        texto_titulo = tk.Label(self.janela_form, text='Informações do aluno', bg='gray', fg='white', font=('Arial', 16, 'bold'))
        texto_titulo.pack(pady=10)
        self.frame = tk.Frame(self.janela_form, bg='light gray')
        self.frame.place(x=10, y=50, width=250, height=330)
        self.criar_campos()
        

        self.button_exportar = tk.Button(self.janela_form, text='EXPORTAR', command=self.button_exportar_acao,
                                    bg='lightgrey', fg='black', width=15, height=2).place(x=25, y=250, width=80, height=30)


        #button_salvar = tk.Button(self.janela_form, text="Salvar", bg='gray', fg='white', command=self.button_editar_acao)
        #button_salvar.place(x=75, y=250, width=100, height=30)

    def criar_campos(self):
        '''
        Essa função cria os campos da janela
        
        '''
        
        labels = ["NOME:", "MATERIA:", "AV1:", "AV2:", "AV3:"]
        self.campos = []
        for i, label in enumerate(labels):
            tk.Label(self.janela_form, text=label, bg='light gray', fg='black', anchor='w', font=('Arial', 10)).place(x=10, y=50 + i * 40, width=100, height=25)
            campo = tk.Label(self.janela_form, text=None, bg='light gray', fg='black', anchor='w', font=('Arial', 10))
            campo.place(x=120, y=50 + i * 40, width=100, height=25)
            self.campos.append(campo)
        self.dados_anteriores()
        
    def dados_anteriores(self):
        '''
        Essa função traz os dados do aluno selecionado
        
        '''

        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()
            cursor.execute('SELECT nome, materia, av1, av2, av3 FROM notas WHERE id = ?', (self.id_selecionado,))
            resultado_fet = cursor.fetchone()

            if resultado_fet:
                self.campos[0].config(text=resultado_fet[0])             # Nome
                self.campos[1].config(text=resultado_fet[1])             # Matéria 
                self.campos[2].config(text=resultado_fet[2])  # AV1
                self.campos[3].config(text=resultado_fet[3])  # AV2
                self.campos[4].config(text=resultado_fet[4])  # AV3

                self.av1 = resultado_fet[2]  # AV1
                self.av2 = resultado_fet[3]  # AV2
                self.av3 = resultado_fet[4]
                self.plot()

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
        finally:
            if conexao:
                conexao.close()
    
    def plot(self):
        '''
        Essa função cria um grafico de barras para visualizar as notas dos alunos

        '''
        
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fc
    
        media = (self.av1 + self.av2 + self.av3) / 3
        label = ['media','AV1', 'AV2', 'AV3']
        nota = [media, self.av1, self.av2, self.av3]

        # Plotagem
        fig = plt.figure(figsize=(2, 3))
        ax = fig.add_subplot(111)  # Adicionar um subplot
        ax.bar(label, nota, color=['blue', 'green', 'green', 'green'])  
        ax.set_title('Notas')
        ax.set_ylabel('Valores')  # eixo y
        ax.set_ylim(0, 10) # limite
        ax.set_xlabel('Avaliações')  # eixo x
        ax.set_xticklabels(label, rotation=45, ha='right')
        plt.suptitle('Desempenho do Aluno')
        plt.tight_layout()

        # FigureCanvasTkAgg para exibir o gráfico na janela do Tkinter
        self.canvas = fc(fig, master=self.janela_form)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=275, y=60)

    def button_exportar_acao(self):
        '''
        Essa função gera o csv do aluno selecionado
        
        '''
        
        from pandas import DataFrame
        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()
            dados = cursor.execute("SELECT * FROM notas").fetchall()
            if not dados:
                messagebox.showinfo(
                    title='ERRO', message='Nenhum dado disponível para exportação')
                return

            colunas = [descricao[0] for descricao in cursor.description]
            df = DataFrame(dados, columns=colunas)
            df.to_csv('meu_csv', index=False)
            messagebox.showinfo(title='Concluido',
                                message='Exportação feita com sucesso')
            conexao.commit()

        except IndexError:
            messagebox.showinfo(
                title='ERRO', message='Selecione um elemento a ser deletado')
        except Exception as e:
            messagebox.showinfo(
                title='ERRO', message=f'Ocorreu um erro: {str(e)}')
        finally:
            conexao.close()
        
