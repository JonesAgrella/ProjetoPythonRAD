import re
from tkinter import ttk, messagebox
import tkinter as tk
from db import insert_resposta

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class FormTab:
    def __init__(self, parent, on_save_callback):
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.create_variables()
        self.create_widgets()
        
    def create_variables(self):
        self.nome_var = tk.StringVar()
        self.idade_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.curso_var = tk.StringVar()
        self.turno_var = tk.StringVar(value="Manhã")
        self.presenca_var = tk.StringVar(value="Presente")
        self.sat_geral_var = tk.IntVar(value=3)
        self.sat_clareza_var = tk.IntVar(value=3)
        self.sat_infra_var = tk.IntVar(value=3)
        self.sat_material_var = tk.IntVar(value=3)
        self.sat_suporte_var = tk.IntVar(value=3)
        self.avisos_var = tk.BooleanVar(value=False)

    def create_widgets(self):
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(20, weight=1)

        # Nome
        ttk.Label(self.parent, text="Nome:").grid(row=1, column=0, sticky="w", padx=(0,8), pady=4)
        ttk.Entry(self.parent, textvariable=self.nome_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=(1, 500))

        # Idade
        ttk.Label(self.parent, text="Idade:").grid(row=2, column=0, sticky="w", padx=(0,8), pady=4)
        ttk.Spinbox(self.parent, from_=10, to=99, textvariable=self.idade_var, width=6, justify="center").grid(
            row=2, column=1, sticky="w", pady=1)

        # Email
        ttk.Label(self.parent, text="E-mail:").grid(row=3, column=0, sticky="w", padx=(0,8), pady=4)
        ttk.Entry(self.parent, textvariable=self.email_var).grid(row=3, column=1, columnspan=2, sticky="ew", padx=(1, 500))

        # Curso
        ttk.Label(self.parent, text="Curso:").grid(row=4, column=0, sticky="w", padx=(0,8), pady=4)
        curso_cb = ttk.Combobox(
            self.parent, textvariable=self.curso_var, state="readonly",
            values=["ADS", "SI", "Engenharia", "Administração"])
        curso_cb.grid(row=4, column=1, sticky="ew", padx=(1, 650))

        # Turno
        ttk.Label(self.parent, text="Turno:").grid(row=5, column=0, sticky="w", padx=(0,8), pady=4)
        turnos = ttk.Frame(self.parent)
        turnos.grid(row=5, column=1, columnspan=2, sticky="w")
        for t in ["Manhã", "Tarde", "Noite"]:
            ttk.Radiobutton(turnos, text=t, value=t, variable=self.turno_var).pack(side="left", padx=(0,8))

        # Presença
        ttk.Label(self.parent, text="Presença:").grid(row=6, column=0, sticky="w", padx=(0,8), pady=4)
        pres = ttk.Frame(self.parent)
        pres.grid(row=6, column=1, columnspan=2, sticky="w")
        for p in ["Presencial", "Remoto"]:
            ttk.Radiobutton(pres, text=p, value=p, variable=self.presenca_var).pack(side="left", padx=(0,8))

        # Likert scales
        self.create_likert_scales()

        # Avisos
        ttk.Checkbutton(self.parent, text="Deseja receber avisos por e-mail?", variable=self.avisos_var).grid(
            row=12, column=1, columnspan=2, sticky="w", pady=4)

        # Buttons
        botoes = ttk.Frame(self.parent)
        botoes.grid(row=13, column=0, columnspan=3, sticky="e", pady=(12,0))
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="right", padx=6)
        ttk.Button(botoes, text="Salvar", command=self.salvar).pack(side="right")

    def create_likert_scales(self):
        questions = [
            (7, "Satisfação Geral (1–5):", self.sat_geral_var),
            (8, "Qualidade do professor(a) (1–5):", self.sat_clareza_var),
            (9, "Infraestrutura (1–5):", self.sat_infra_var),
            (10, "Material didático (1–5):", self.sat_material_var),
            (11, "Suporte/atendimento (1–5):", self.sat_suporte_var),
        ]
        
        for row, label, var in questions:
            self.create_likert_row(row, label, var)

    def create_likert_row(self, row, label, var):
        def snap(value):
            var.set(round(float(value)))

        ttk.Label(self.parent, text=label).grid(
            row=row, column=0, sticky="w", padx=(0,8), pady=4
        )

        ttk.Label(self.parent, textvariable=var, width=2).grid(
            row=row, column=2, sticky="w", padx=(1,8)
        )

        ttk.Scale(
            self.parent,
            from_=1,
            to=5,
            variable=var,
            orient="horizontal",
            command=snap
        ).grid(
            row=row, column=1,
            sticky="ew",
            pady=4,
            padx=(1,100)
        )

    def validar_campos(self):
        nome = self.nome_var.get().strip()
        if len(nome) < 3:
            return False, "Informe um nome com pelo menos 3 caracteres."

        try:
            idade = int(self.idade_var.get())
        except ValueError:
            return False, "Idade inválida."
        if not (10 <= idade <= 99):
            return False, "Idade deve ser entre 10 e 99."

        email = self.email_var.get().strip()
        if not EMAIL_RE.match(email):
            return False, "E-mail inválido."

        if not self.curso_var.get():
            return False, "Selecione o curso."

        return True, ""

    def limpar(self):
        self.nome_var.set("")
        self.idade_var.set("")
        self.email_var.set("")
        self.curso_var.set("")
        self.turno_var.set("Manhã")
        self.presenca_var.set("Presente")
        for v in [self.sat_geral_var, self.sat_clareza_var, self.sat_infra_var, 
                 self.sat_material_var, self.sat_suporte_var]:
            v.set(3)
        self.avisos_var.set(False)

    def salvar(self):
        ok, msg = self.validar_campos()
        if not ok:
            messagebox.showerror("Dados inválidos", msg)
            return

        data = {
            "nome": self.nome_var.get().strip(),
            "idade": int(self.idade_var.get()),
            "email": self.email_var.get().strip(),
            "curso": self.curso_var.get(),
            "turno": self.turno_var.get(),
            "presenca": self.presenca_var.get(),
            "sat_geral": self.sat_geral_var.get(),
            "sat_clareza": self.sat_clareza_var.get(),
            "sat_infra": self.sat_infra_var.get(),
            "sat_material": self.sat_material_var.get(),
            "sat_suporte": self.sat_suporte_var.get(),
            "avisos": self.avisos_var.get(),
        }
        
        try:
            insert_resposta(data)
            messagebox.showinfo("Sucesso", "Resposta salva com sucesso!")
            self.limpar()
            if self.on_save_callback:
                self.on_save_callback()
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Ocorreu um erro: {e}")