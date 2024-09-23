import tkinter as tk
from tkinter import ttk
import sqlite3



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
