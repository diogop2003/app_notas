import tkinter as tk
import sqlite3

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

    texto_resultado.delete(1.0, tk.END)

    for item in resultado:
        texto_resultado.insert(tk.END, str(item) + '\n')

    conexao.close()

def button_adicionar_acao():
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO notas (nome, conteudo)
        VALUES (?, ?)
    ''', ('teste', 'teste@teste'))

    conexao.commit()
    conexao.close()

def button_pesquisar_acao():
    print('Pesquisar ação ainda não implementada')

# Criar a janela principal
janela = tk.Tk()
janela.title('HOME')
janela.geometry('400x380')
janela.config(bg='gray')
janela.resizable(False, False)

# Caixa de texto para mostrar os resultados
texto_resultado = tk.Text(janela, wrap=tk.WORD, bg='lightgrey', fg='black', height=15, width=50)
texto_resultado.place(x=100, y=10, width=290, height=300)

# Botão consultar
button_consulta = tk.Button(janela, text='CONSULTAR', command=button_consulta_acao, bg='lightgrey', fg='black', width=15, height=2)
button_consulta.place(x=10, y=10, width=80, height=40)

# Botão adicionar
button_adicionar = tk.Button(janela, text='ADICIONAR', command=button_adicionar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_adicionar.place(x=10, y=60, width=80, height=40)

# Botão pesquisar
button_pesquisar = tk.Button(janela, text='PESQUISAR', command=button_pesquisar_acao, bg='lightgrey', fg='black', width=15, height=2)
button_pesquisar.place(x=10, y=110, width=80, height=40)

# Caixa de texto para pesquisa
texto_pesquisa = tk.Text(janela, bg='lightgrey', fg='black', height=2, width=20)
texto_pesquisa.place(x=10, y=160, width=80, height=50)

janela.mainloop()
