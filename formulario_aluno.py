import tkinter as tk
import sqlite3


class FormularioAluno:
    def __init__(self, root):
        self.root = root

    def criar_formulario(self):
        self.janela_form = tk.Toplevel()
        self.janela_form.title("ADICIONAR ALUNO")
        self.janela_form.geometry("400x350")
        self.janela_form.config(bg='gray')
        self.janela_form.resizable(False, False)

        texto_titulo = tk.Label(self.janela_form, text="FORMULÁRIO", bg='gray', fg='white', font=('Arial', 16, 'bold'))
        texto_titulo.pack(pady=10)

        texto_nome = tk.Label(self.janela_form, text="NOME:", bg='gray', fg='white', anchor='w')
        texto_nome.place(x=10, y=60, width=100, height=25)

        self.caixa_nome = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
        self.caixa_nome.place(x=120, y=60, width=250, height=25)

        texto_info = tk.Label(self.janela_form, text="INFORMAÇÕES:", bg='gray', fg='white', anchor='w')
        texto_info.place(x=10, y=100, width=100, height=25)

        self.caixa_texto = tk.Text(self.janela_form, bg='lightgrey', fg='black', wrap='word')
        self.caixa_texto.place(x=10, y=130, width=360, height=150)

        button_salvar = tk.Button(self.janela_form, text="Salvar", bg='gray', fg='white', command=self.button_salvar_acao)
        button_salvar.place(x=150, y=300, width=100, height=30)


    def button_salvar_acao(self):
        conexao = sqlite3.connect('meu_banco.db')
        cursor = conexao.cursor()

        termo_nome = self.caixa_nome.get().strip()  # Obtendo o valor da caixa de nome
        termo_texto = self.caixa_texto.get("1.0", tk.END).strip()  # Obtendo o valor da caixa de texto

        cursor.execute('''
            INSERT INTO notas (nome, conteudo)
            VALUES (?, ?)
        ''', (termo_nome, termo_texto))

        conexao.commit()
        conexao.close()

        self.fechar_formulario()

    def fechar_formulario(self):
        if self.janela_form:
            self.janela_form.destroy()
            self.janela_form = None

