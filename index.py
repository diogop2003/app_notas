import tkinter as tk
import sqlite3


def criar_banco():
    conexao = sqlite3.connect('notas.db')
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
    # Conectar ao banco de dados
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()
    
    # Selecionar dados da tabela
    cursor.execute('SELECT * FROM usuarios')
    resultado = cursor.fetchall()

    texto_resultado.delete(1.0, tk.END)

    # Exibir os dados no console
    for resultado in resultado:
        texto_resultado.insert(tk.END, str(resultado) + '\n')
    


    # Fechar a conexão
    conexao.close()

def button_adicionar_acao():
    # Conectar ao banco de dados
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
                   INSERT INTO usuarios (nome, email)
                   VALUES (?, ?)
                   ''', ('teste', 'teste@teste')
                   )
    
    conexao.commit()
    cursor.close()
    

# Criar a janela principal
janela = tk.Tk()
janela.title('HOME')
janela.geometry('400x380')
janela.config(bg= 'gray')


#caixa de texto
texto_resultado = tk.Text(janela, wrap=tk.WORD, bg='lightgrey', fg='black', height=15, width=60)
texto_resultado.place(x=100, y=10, width=290, height=360)

# Criar o botao consulta *
button_consulta = tk.Button(janela, text='CONSULTAR', command=button_consulta_acao, bg='blue', fg='black', width=15, height=2)
button_consulta.place(x= 10, y=10, width=80, height=30)


# Criar o botão adicionar
button_adicionar = tk.Button(janela, text='ADICIONAR', command=button_adicionar_acao, bg='blue', fg='black', width=15, height=2)
button_adicionar.place(x= 10, y=40, width=80, height=30)

# Criar o botão 
button_adicionar = tk.Button(janela, text='ADICIONAR', command=button_adicionar_acao, bg='blue', fg='black', width=15, height=2)
button_adicionar.place(x= 10, y=40, width=80, height=30)


# Iniciar o loop principal da interface gráfica
janela.mainloop()
