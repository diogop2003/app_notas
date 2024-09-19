import tkinter as tk
from tkinter import ttk
import sqlite3



class FormularioEditar:
    def __init__(self, root):
        self.root = root

    def criar_formulario(self):
        self.janela_form = tk.Toplevel()
        self.janela_form.title("EDITAR ALUNO")
        self.janela_form.geometry("400x400")
        self.janela_form.config(bg='gray')
        self.janela_form.resizable(False, False)

        texto_titulo = tk.Label(self.janela_form, text="EDITAR ALUNO", bg='gray', fg='white', font=('Arial', 16, 'bold'))
        texto_titulo.pack(pady=10)

        texto_nome = tk.Label(self.janela_form, text="NOME:", bg='gray', fg='white', anchor='w')
        texto_nome.place(x=10, y=50, width=100, height=25)

        self.caixa_nome = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
        self.caixa_nome.place(x=120, y=50, width=260, height=25)

        texto_materia = tk.Label(self.janela_form, text="MATERIA:", bg='gray', fg='white', anchor='w')
        texto_materia.place(x=10, y=90, width=100, height=25)

        self.caixa_materia = tk.Text(self.janela_form, bg='lightgrey', fg='black', wrap='word')
        self.caixa_materia.place(x=120, y=90, width=260, height=25)

        texto_av1 = tk.Label(self.janela_form, text="AV1:", bg='gray', fg='white', anchor='w')
        texto_av1.place(x=10, y=180, width=100, height=25)

        self.caixa_av1 = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
        self.caixa_av1.place(x=120, y=180, width=100, height=25)

        texto_av2 = tk.Label(self.janela_form, text="AV2:", bg='gray', fg='white', anchor='w')
        texto_av2.place(x=10, y=220, width=100, height=25)

        self.caixa_av2 = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
        self.caixa_av2.place(x=120, y=220, width=100, height=25)

        texto_av3 = tk.Label(self.janela_form, text="AV3:", bg='gray', fg='white', anchor='w')
        texto_av3.place(x=10, y=260, width=100, height=25)

        self.caixa_av3 = tk.Entry(self.janela_form, bg='lightgrey', fg='black')
        self.caixa_av3.place(x=120, y=260, width=100, height=25)

        # Botão editar
        button_salvar = tk.Button(self.janela_form, text="Editar", bg='gray', fg='white', command=self.button_editar_acao)
        button_salvar.place(x=150, y=310, width=100, height=30)

    def button_editar_acao(self):
        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()
            from index import button_editar_acao
            id_aluno = button_editar_acao  # Obtém o ID do aluno a ser editado

            termo_nome = self.caixa_nome.get().strip()
            termo_materia = self.caixa_materia.get("1.0", tk.END).strip()
            termo_av1 = self.caixa_av1.get().strip()
            termo_av2 = self.caixa_av2.get().strip()
            termo_av3 = self.caixa_av3.get().strip()

            # Validações
            if not termo_nome or not termo_materia or not termo_av1 or not termo_av2 or not termo_av3:
                raise ValueError("Preencha todos os campos corretamente!")

            # Atualiza o registro no banco de dados
            cursor.execute('''
                UPDATE notas
                SET nome = ?, materia = ?, av1 = ?, av2 = ?, av3 = ?
                WHERE id = ?
            ''', (termo_nome, termo_materia, termo_av1, termo_av2, termo_av3, id_aluno))

            # Calcula a média e atualiza a tabela
            media = self.calc_media(float(termo_av1), float(termo_av2), float(termo_av3))
            cursor.execute('''
                UPDATE notas
                SET media = ?
                WHERE id = ?
            ''', (media, id_aluno))

            conexao.commit()
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            conexao.close()
            self.fechar_formulario()

    def fechar_formulario(self):
        if self.janela_form:
            self.janela_form.destroy()
            self.janela_form = None

    def calc_media(self, av1, av2, av3):
        return (av1 + av2 + av3) / 3
