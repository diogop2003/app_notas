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
            materia TEXT NOT NULL,
            av1 REAL CHECK(av1 <= 10),
            av2 REAL CHECK(av2 <= 10),
            av3 REAL CHECK(av3 <= 10),
            media REAL 
        ) 
    ''')
    conexao.commit()
    conexao.close()



def formatar_media(media):
    return f"{media:.1f}"

def button_atualizar_acao():
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM notas')
    resultado = cursor.fetchall()

    # Limpar a Treeview
    for item in tv.get_children():
        tv.delete(item)

    for item in resultado:
        id_nota, nome, materia, av1, av2, av3, media = item
        media_formatada = formatar_media(media) if media is not None else 'N/A'
        tv.insert('', tk.END, values=(id_nota, nome, materia, av1, av2, av3, media_formatada))

    conexao.close()

def button_criar_acao():
    formulario = FormularioAluno(janela)
    formulario.criar_formulario()

def button_pesquisar_acao():
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()

    termo_pesquisa = texto_pesquisa.get("1.0", tk.END).strip()

    cursor.execute('SELECT * FROM notas WHERE nome LIKE ?', ('%' + termo_pesquisa + '%',))
    resultado = cursor.fetchall()

    # Limpar a Treeview 
    for item in tv.get_children():
        tv.delete(item)

    # Inserir dados Treeview
    for item in resultado:
        id_nota, nome, materia, av1, av2, av3, media = item
        tv.insert('', tk.END, values=(id_nota, nome, materia, av1, av2, av3, media))

    conexao.close()

def button_editar_acao():
    pass

 
def button_remover_acao():
    pass
    


# Criar a janela principal
janela = tk.Tk()
janela.title('APP ALUNOS')
janela.geometry('700x500')  
janela.config(bg='gray')
janela.resizable(False, False)

# Treeview para consulta
tv = ttk.Treeview(janela, columns=('id', 'nome', 'materia', 'av1', 'av2', 'av3', 'media'), show='headings')
tv.column('id', minwidth=0, width=50, anchor='center')
tv.column('nome', minwidth=0, width=150, anchor='center')
tv.column('materia', minwidth=0, width=150, anchor='center')
tv.column('av1', minwidth=0, width=50, anchor='center')
tv.column('av2', minwidth=0, width=50, anchor='center')
tv.column('av3', minwidth=0, width=50, anchor='center')
tv.column('media', minwidth=0, width=50, anchor='center')
tv.heading('id', text='ID', anchor='center')
tv.heading('nome', text='NOME', anchor='center')
tv.heading('materia', text='MATERIA', anchor='center')
tv.heading('av1', text='AV1', anchor='center')
tv.heading('av2', text='AV2', anchor='center')
tv.heading('av3', text='AV3', anchor='center')
tv.heading('media', text='MEDIA', anchor='center')
tv.place(x=100, y=10, width=580, height=470)

# Criar o banco de dados quando iniciar
criar_banco()

# Atualizar a Treeview quando iniciar 
button_atualizar_acao()

# Botão consultar
button_atualizar = tk.Button(janela, text='ATUALIZAR', command=button_atualizar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_atualizar.place(x=10, y=10, width=80, height=30)

# Botão criar
button_criar = tk.Button(janela, text='CRIAR', command=button_criar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_criar.place(x=10, y=45, width=80, height=30)

# Botão pesquisar
button_pesquisar = tk.Button(janela, text='PESQUISAR', command=button_pesquisar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_pesquisar.place(x=10, y=80, width=80, height=30)

# Caixa de texto para pesquisa
texto_pesquisa = tk.Text(janela, bg='lightgrey', fg='black', width=20, height=2)
texto_pesquisa.place(x=10, y=110, width=80, height=20)

# Botão editar
button_editar = tk.Button(janela, text='EDITAR', command=button_editar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_editar.place(x=10, y=135, width=80, height=30)

# Botão remover
button_remover = tk.Button(janela, text='REMOVER', command=button_remover_acao, bg='lightgrey', fg='black', width=15, height=2)
button_remover.place(x=10, y=170, width=80, height=30)

janela.mainloop()
