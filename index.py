import tkinter as tk
from tkinter import ttk
import sqlite3
from formulario_aluno import FormularioAluno



def criar_banco():
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            conteudo TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def button_consulta_acao():
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM notas')
    resultado = cursor.fetchall()

    # Limpar a Treeview antes de adicionar novos dados
    for item in tv.get_children():
        tv.delete(item)

    # Inserir novos dados na Treeview
    for item in resultado:
        tv.insert('', tk.END, values=item)


def button_criar_acao():
    formulario = FormularioAluno(janela)
    formulario.criar_formulario()

def button_pesquisar_acao():

    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()

    termo_pesquisa = texto_pesquisa.get("1.0", tk.END).strip() 

    cursor.execute('SELECT * FROM notas WHERE nome LIKE ?', ('%' + termo_pesquisa + '%',))
    resultado = cursor.fetchall()

    # Limpar a Treeview antes de adicionar
    for item in tv.get_children():
        tv.delete(item)

    # Inserir dados na Treeview
    for item in resultado:
        tv.insert('', tk.END, values=item)

    conexao.commit()
    conexao.close()

def button_editar_acao():
    pass


# Criar a janela principal
janela = tk.Tk()
janela.title('APP ALUNOS')
janela.geometry('500x380')
janela.config(bg='gray')
janela.resizable(False, False)

#Treeview para consulta
tv = ttk.Treeview(janela, columns=('id', 'nome', 'conteudo'), show='headings')
tv.column('id', minwidth=0, width=10)
tv.column('nome', minwidth=0, width=150)
tv.column('conteudo', minwidth=0, width=150)
tv.heading('id', text='ID')
tv.heading('nome', text='NOME')
tv.heading('conteudo', text='CONTEÚDO')
tv.place(x=100, y=10, width=390, height=360)

# Botão consultar
button_consulta = tk.Button(janela, text='CONSULTAR', command=button_consulta_acao, bg='lightgrey', fg='black', width=15, height=2)
button_consulta.place(x=10, y=10, width=80, height=30)

# Botão criar
button_criar = tk.Button(janela, text='ADICIONAR', command=button_criar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_criar.place(x=10, y=45, width=80, height=30)

# Botão pesquisar
button_pesquisar = tk.Button(janela, text='PESQUISAR', command=button_pesquisar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_pesquisar.place(x=10, y=80, width=80, height=30)

# Caixa de texto para pesquisa
texto_pesquisa = tk.Text(janela, bg='lightgrey', fg='black', width=20, height=2)
texto_pesquisa.place(x=10, y=110, width=80, height=20)

janela.mainloop()
