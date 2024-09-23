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
        formulario = FormularioAluno(self.janela)
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
            formulario = FormularioEditar(self.janela, id_selecionado)
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


# Executar a aplicação
janela = tk.Tk()
app = JanelaPrincipal(janela)
janela.mainloop()
