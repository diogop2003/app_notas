import tkinter as tk
from tkinter import messagebox
import sqlite3

class FormularioEditar:
    
    def __init__(self, root, id_selecionado):
        self.root = root
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

        self.button_salvar = tk.Button(self.janela_form, text="Salvar", bg='gray', fg='white', command=self.button_editar_acao).place(x=75, y=250, width=100, height=30)

    def criar_campos(self):
        labels = ["NOME:", "MATERIA:", "AV1:", "AV2:", "AV3:"]
        self.campos = []
        for i, label in enumerate(labels):
            tk.Label(self.janela_form, text=label, bg='gray', fg='white', anchor='w').place(x=10, y=50 + i * 40, width=100, height=25)
            campo = tk.Entry(self.janela_form, bg='lightgrey', fg='black').place(x=120, y=50 + i * 40, width=100, height=25)
            self.campos.append(campo)
        self.dados_anteriores() 
    
    def dados_anteriores(self):
        try:
            conexao = sqlite3.connect('meu_banco.db')
            cursor = conexao.cursor()
            cursor.execute('SELECT nome, materia, av1, av2, av3 FROM notas WHERE id = ?', (self.id_selecionado,))
            resultado_fet = cursor.fetchone()

            if resultado_fet:
                if resultado_fet:
                    self.campos[0].config(text=resultado_fet[0])  # Nome
                    self.campos[1].config(text=resultado_fet[1])  # Matéria 
                    self.campos[2].config(text=resultado_fet[2])  # AV1
                    self.campos[3].config(text=resultado_fet[3])  # AV2
                    self.campos[4].config(text=resultado_fet[4])  # AV3

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
            termo_materia = self.campos[1].get("1.0", tk.END).strip()
            termo_av1 = self.campos[2].get().strip()
            termo_av2 = self.campos[3].get().strip()
            termo_av3 = self.campos[4].get().strip()

            if not termo_nome or not termo_materia or not termo_av1 or not termo_av2 or not termo_av3:
                raise ValueError("Preencha todos os campos corretamente!")
            cursor.execute('''
                UPDATE notas
                SET nome = ?, materia = ?, av1 = ?, av2 = ?, av3 = ?
                WHERE id = ?
            ''', (termo_nome, termo_materia, termo_av1, termo_av2, termo_av3, self.id_selecionado))

            # Calcula a média e atualiza a tabela
            media = self.calc_media(float(termo_av1), float(termo_av2), float(termo_av3))
            cursor.execute('UPDATE notas SET media = ? WHERE id = ?', (media, self.id_selecionado))

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
            from index import button_atualizar_acao
            button_atualizar_acao()

    def calc_media(self, av1, av2, av3):
        return (av1 + av2 + av3) / 3
