import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from formulario_criar import FormularioAluno
from formulario_editar import FormularioEditar
from info_aluno import InformacoesAluno


class JanelaPrincipal:

    def __init__(self, janela):
        self.janela = janela
        self.tv = None
        self.texto_pesquisa = None
        self.criar_banco()
        self.iniciar_interface()

    def criar_banco(self):
        '''
        Essa função cria o banco de dados caso ele não exista

        '''
        conexao = sqlite3.connect('meu_banco.db')
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                materia TEXT NOT NULL,
                av1 REAL CHECK(av1 <= 10),
                av2 REAL CHECK(av2 <= 10),
                av3 REAL CHECK(av3 <= 10),
                media REAL 
            ) 
        ''')
        conexao.commit()
        conexao.close()

    def formatar_media(self, media):
        '''
        Essa função formata a media dos alunos

        '''
        return f"{media:.1f}"

    def button_atualizar_acao(self):
        '''
        Essa função é a ação do botão "ATUALIZAR", que atualiza as informações dos alunos no Banco de dados

        '''
        conexao = sqlite3.connect('meu_banco.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM notas')
        resultado = cursor.fetchall()

        # Limpar a Treeview
        for item in self.tv.get_children():
            self.tv.delete(item)

        for item in resultado:
            id_nota, nome, materia, av1, av2, av3, media = item
            media_formatada = self.formatar_media(
                media) if media is not None else 'N/A'
            self.tv.insert('', tk.END, values=(
                id_nota, nome, materia, av1, av2, av3, media_formatada))

        conexao.close()

    def button_criar_acao(self):
        '''
        Essa função é a ação do botão "CRIAR", que chama a janela de criação do formulario do aluno 

        '''
        formulario = FormularioAluno(self.janela, self.button_atualizar_acao)
        formulario.criar_formulario()

    def button_pesquisar_acao(self):
        '''
        Essa função é a ação do botão "PESQUISAR", que mostra na TreevView o aluno de acordo 
        com o nome escrito no campo de entrada embaixo do botão

        '''

        conexao = sqlite3.connect('meu_banco.db')
        cursor = conexao.cursor()

        termo_pesquisa = self.texto_pesquisa.get("1.0", tk.END).strip()

        cursor.execute('SELECT * FROM notas WHERE nome LIKE ?',
                       ('%' + termo_pesquisa + '%',))
        resultado = cursor.fetchall()

        # Limpar a Treeview
        for item in self.tv.get_children():
            self.tv.delete(item)

        # Inserir dados Treeview
        for item in resultado:
            id_nota, nome, materia, av1, av2, av3, media = item
            self.tv.insert('', tk.END, values=(
                id_nota, nome, materia, av1, av2, av3, media))

        conexao.close()

    def button_remover_acao(self):
        '''
        Essa função é a ação do botão "REMOVER", que exclui o aluno selecionado

        '''

        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()

            selecionado = self.tv.selection()[0]
            valores = self.tv.item(selecionado)['values']
            id_selecionado = valores[0]
            self.tv.delete(selecionado)
            cursor.execute("DELETE FROM notas WHERE id = ?", (id_selecionado,))

            conexao.commit()

        except IndexError:
            messagebox.showinfo(
                title='ERRO', message='Selecione um elemento a ser deletado')
        except Exception as e:
            messagebox.showinfo(
                title='ERRO', message=f'Ocorreu um erro: {str(e)}')
        finally:
            conexao.close()

    def id_selecionado(self):
        '''
        Essa função retorna o id do aluno selecionado na TreeView

        '''

        try:
            selecionado = self.tv.selection()[0]
            valores = self.tv.item(selecionado)['values']
            return valores[0]  # Retorna o ID do item selecionado
        except IndexError:
            messagebox.showinfo(
                title='ERRO', message='Selecione um elemento a ser editado')
            return None

    def button_editar_acao(self):
        '''
        Essa função é a ação do botão "EDITAR", que chama a janela de edição do aluno selecionado

        '''

        id_selecionado = self.id_selecionado()
        if id_selecionado is not None:
            formulario = FormularioEditar(
                id_selecionado, self.button_atualizar_acao)

        formulario.criar_formulario()

    def button_exportar_acao(self):
        '''
        Essa função gera o aquivo "meu_csv", que contem todos os dados do Banco de dados

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

    def double_click(self, event):
        '''
        Essa função ao dar double-click no aluno na Treeview, chama a função "info_aluno",
        que abre a janela de informações do aluno

        '''

        item = self.tv.selection()
        if item:
            self.info_aluno()

    def info_aluno(self):
        '''
        Essa função chama a janela de informações do aluno selecionado

        '''

        id_selecionado = self.id_selecionado()
        if id_selecionado is not None:
            informacoes = InformacoesAluno(self.janela, id_selecionado)
            informacoes.criar_formulario()

    def iniciar_interface(self):
        '''
        Essa função cria a janela principal

        '''

        # Criar a janela principal
        self.janela.title('APP ALUNOS')
        self.janela.geometry('700x500')
        self.janela.config(bg='gray')
        self.janela.resizable(False, False)

        # Treeview para consulta
        self.tv = ttk.Treeview(self.janela, columns=(
            'id', 'nome', 'materia', 'av1', 'av2', 'av3', 'media'), show='headings')
        self.tv.column('id', minwidth=0, width=50, anchor='center')
        self.tv.column('nome', minwidth=0, width=150, anchor='center')
        self.tv.column('materia', minwidth=0, width=150, anchor='center')
        self.tv.column('av1', minwidth=0, width=50, anchor='center')
        self.tv.column('av2', minwidth=0, width=50, anchor='center')
        self.tv.column('av3', minwidth=0, width=50, anchor='center')
        self.tv.column('media', minwidth=0, width=50, anchor='center')
        self.tv.heading('id', text='ID', anchor='center')
        self.tv.heading('nome', text='NOME', anchor='center')
        self.tv.heading('materia', text='MATERIA', anchor='center')
        self.tv.heading('av1', text='AV1', anchor='center')
        self.tv.heading('av2', text='AV2', anchor='center')
        self.tv.heading('av3', text='AV3', anchor='center')
        self.tv.heading('media', text='MEDIA', anchor='center')
        self.tv.place(x=100, y=10, width=580, height=470)

        # Atualizar a Treeview quando iniciar
        self.button_atualizar_acao()

        # Botões ------------
        button_atualizar = tk.Button(self.janela, text='ATUALIZAR', command=self.button_atualizar_acao,
                                     bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=10, width=80, height=30)

        button_criar = tk.Button(self.janela, text='CRIAR', command=self.button_criar_acao,
                                 bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=45, width=80, height=30)

        button_pesquisar = tk.Button(self.janela, text='PESQUISAR', command=self.button_pesquisar_acao,
                                     bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=80, width=80, height=30)

        self.texto_pesquisa = tk.Text(self.janela, bg='lightgrey', fg='black', width=20, height=2).place(
            x=10, y=110, width=80, height=20)

        button_editar = tk.Button(janela, text='EDITAR', command=self.button_editar_acao,
                                  bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=135, width=80, height=30)

        button_remover = tk.Button(self.janela, text='REMOVER', command=self.button_remover_acao,
                                   bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=170, width=80, height=30)

        button_exportar = tk.Button(self.janela, text='EXPORTAR', command=self.button_exportar_acao,
                                    bg='lightgrey', fg='black', width=15, height=2).place(x=10, y=205, width=80, height=30)

        self.tv.bind('<Double-1>', self.double_click)

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


class FormularioAluno:
    def __init__(self, janela, button_atualizar_acao):
        self.janela = janela
        self.button_atualizar_acao = button_atualizar_acao
        

    def criar_formulario(self):
        self.janela_form = tk.Toplevel()
        self.janela_form.title("CRIAR ALUNO")
        self.janela_form.geometry("250x310")
        self.janela_form.config(bg='gray')
        self.janela_form.resizable(False, False)
        texto_titulo = tk.Label(self.janela_form, text="FORMULARIO ALUNO", bg='gray', fg='white', font=('Arial', 16, 'bold'))
        texto_titulo.pack(pady=10)
        self.criar_campos()

        button_salvar = tk.Button(self.janela_form, text="Salvar", bg='gray', fg='white', command=self.button_salvar_acao)
        button_salvar.place(x=75, y=250, width=100, height=30)


    def criar_campos(self):
        labels = ["NOME:", "MATERIA:", "AV1:", "AV2:", "AV3:"]
        self.campos = []
        for i, label in enumerate(labels):
            tk.Label(self.janela_form, text=label, bg='gray', fg='white', anchor='w').place(x=10, y=50 + i * 40, width=100, height=25)
            campo = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
            campo.place(x=120, y=50 + i * 40, width=100, height=25)
            self.campos.append(campo) 

    def button_salvar_acao(self):
        '''
        Extrair os valores digitados

        '''
        nome = self.campos[0].get()
        materia = self.campos[1].get()
        av1 = self.campos[2].get()
        av2 = self.campos[3].get()
        av3 = self.campos[4].get()

        if not nome or not materia or not av1 or not av2 or not av3:  # Verifica se os campos estão vazios
            tk.messagebox.showwarning("Aviso", "Todos os campos devem estar preenchidos!")
            return

        conexao = sqlite3.connect('meu_banco.db')
        cursor = conexao.cursor()

        cursor.execute('''
            INSERT INTO notas (nome, materia, av1, av2, av3)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, materia, float(av1), float(av2), float(av3)))

        # Recupera o ID da linha inserida
        id_nota = cursor.lastrowid

        # Calcula a media e atualiza a tabela
        media = self.calc_media(float(av1), float(av2), float(av3))
        cursor.execute('''
            UPDATE notas
            SET media = ?
            WHERE id = ?
        ''', (media, id_nota))

        conexao.commit()
        conexao.close()

        self.fechar_formulario()

    def fechar_formulario(self):
        if self.janela_form:
            self.janela_form.destroy()
            self.janela_form = None
            self.button_atualizar_acao()

    def calc_media(self, av1, av2, av3):
        return (av1 + av2 + av3) / 3


class FormularioEditar:
    
    def __init__(self, id_selecionado, button_atualizar_acao):
        self.button_atualizar_acao = button_atualizar_acao
        self.id_selecionado = id_selecionado  # Armazena o ID do aluno

    def criar_formulario(self):
        self.janela_form = tk.Toplevel()
        self.janela_form.title("EDITAR ALUNO")
        self.janela_form.geometry("250x310")
        self.janela_form.config(bg='gray')
        self.janela_form.resizable(False, False)
        texto_titulo = tk.Label(self.janela_form, text="FORMULARIO ALUNO", bg='gray', fg='white', font=('Arial', 16, 'bold'))
        texto_titulo.pack(pady=10)
        self.criar_campos()

        self.button_salvar = tk.Button(self.janela_form, text="Salvar", bg='gray', fg='white', command=self.button_editar_acao)
        self.button_salvar.place(x=75, y=250, width=100, height=30)

    def criar_campos(self):
        labels = ["NOME:", "MATERIA:", "AV1:", "AV2:", "AV3:"]
        self.campos = []
        for i, label in enumerate(labels):
            tk.Label(self.janela_form, text=label, bg='gray', fg='white', anchor='w').place(x=10, y=50 + i * 40, width=100, height=25)
            campo = tk.Entry(self.janela_form, bg='lightgrey', fg='black')  # Criação do campo Entry
            campo.place(x=120, y=50 + i * 40, width=100, height=25)  # Posiciona o campo Entry
            self.campos.append(campo)  # Armazena o campo Entry na lista
        self.dados_anteriores() 
    
    def dados_anteriores(self):
        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()
            cursor.execute('SELECT nome, materia, av1, av2, av3 FROM notas WHERE id = ?', (self.id_selecionado,))
            resultado_fet = cursor.fetchone()

            if resultado_fet:
                # Preenche os campos com os valores recuperados do banco de dados
                self.campos[0].insert(0, resultado_fet[0])  # Nome
                self.campos[1].insert(0, resultado_fet[1])  # Matéria
                self.campos[2].insert(0, resultado_fet[2])  # AV1
                self.campos[3].insert(0, resultado_fet[3])  # AV2
                self.campos[4].insert(0, resultado_fet[4])  # AV3

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
        finally:
            if conexao:
                conexao.close()

    def button_editar_acao(self):
        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()

            termo_nome = self.campos[0].get().strip()
            termo_materia = self.campos[1].get().strip()
            termo_av1 = self.campos[2].get().strip()
            termo_av2 = self.campos[3].get().strip()
            termo_av3 = self.campos[4].get().strip()

            if not termo_nome or not termo_materia or not termo_av1 or not termo_av2 or not termo_av3:
                messagebox.showwarning("Aviso", "Preencha todos os campos corretamente!")
                return

            cursor.execute('''
                UPDATE notas
                SET nome = ?, materia = ?, av1 = ?, av2 = ?, av3 = ?
                WHERE id = ?
            ''', (termo_nome, termo_materia, termo_av1, termo_av2, termo_av3, self.id_selecionado))

            # Calcula a média e atualiza a tabela
            media = self.calc_media(float(termo_av1), float(termo_av2), float(termo_av3))
            cursor.execute('UPDATE notas SET media = ? WHERE id = ?', (media, self.id_selecionado))

            conexao.commit()
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            conexao.close()
            self.fechar_formulario()

         

    def fechar_formulario(self):
        if self.janela_form:
            self.janela_form.destroy()
            self.janela_form = None
            self.button_atualizar_acao()

    def calc_media(self, av1, av2, av3):
        return (av1 + av2 + av3) / 3


# Executar a aplicação
janela = tk.Tk()
app = JanelaPrincipal(janela)
janela.mainloop()
