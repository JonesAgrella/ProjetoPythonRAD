import re
import tkinter as tk
from tkinter import ttk, messagebox
from db import insert_resposta

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_form(parent, on_save_callback):
    nome_var = tk.StringVar()
    idade_var = tk.StringVar()
    email_var = tk.StringVar()
    curso_var = tk.StringVar()
    turno_var = tk.StringVar(value="Manhã")
    presenca_var = tk.StringVar(value="Presencial")
    sat_geral_var = tk.IntVar(value=3)
    sat_clareza_var = tk.IntVar(value=3)
    sat_infra_var = tk.IntVar(value=3)
    sat_material_var = tk.IntVar(value=3)
    sat_suporte_var = tk.IntVar(value=3)
    avisos_var = tk.BooleanVar(value=False)

    def validar_campos():
        nome = nome_var.get().strip()
        if len(nome) < 3:
            return False, "Informe um nome com pelo menos 3 caracteres."

        try:
            idade = int(idade_var.get())
        except ValueError:
            return False, "Idade inválida."
        if not (10 <= idade <= 99):
            return False, "Idade deve ser entre 10 e 99."

        email = email_var.get().strip()
        if not EMAIL_RE.match(email):
            return False, "E-mail inválido."

        if not curso_var.get():
            return False, "Selecione o curso."

        return True, ""

    def limpar():
        nome_var.set("")
        idade_var.set("")
        email_var.set("")
        curso_var.set("")
        turno_var.set("Manhã")
        presenca_var.set("Presencial")
        for v in [sat_geral_var, sat_clareza_var, sat_infra_var,
                  sat_material_var, sat_suporte_var]:
            v.set(3)
        avisos_var.set(False)

    def salvar():
        ok, msg = validar_campos()
        if not ok:
            messagebox.showerror("Dados inválidos", msg)
            return

        data = {
            "nome": nome_var.get().strip(),
            "idade": int(idade_var.get()),
            "email": email_var.get().strip(),
            "curso": curso_var.get(),
            "turno": turno_var.get(),
            "presenca": presenca_var.get(),
            "sat_geral": sat_geral_var.get(),
            "sat_clareza": sat_clareza_var.get(),
            "sat_infra": sat_infra_var.get(),
            "sat_material": sat_material_var.get(),
            "sat_suporte": sat_suporte_var.get(),
            "avisos": avisos_var.get(),
        }

        try:
            insert_resposta(data)
            messagebox.showinfo("Sucesso", "Resposta salva com sucesso!")
            limpar()
            if on_save_callback:
                on_save_callback()
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Ocorreu um erro: {e}")

    def create_likert_row(row, label, var):
        def snap(value):
            var.set(round(float(value)))

        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=(0, 8), pady=4
        )

        ttk.Label(parent, textvariable=var, width=2).grid(
            row=row, column=2, sticky="w", padx=(1, 8)
        )

        ttk.Scale(
            parent,
            from_=1,
            to=5,
            variable=var,
            orient="horizontal",
            command=snap
        ).grid(
            row=row, column=1,
            sticky="ew",
            pady=4,
            padx=(1, 100)
        )

    def create_likert_scales():
        questions = [
            (7, "Satisfação Geral (1–5):", sat_geral_var),
            (8, "Qualidade do professor(a) (1–5):", sat_clareza_var),
            (9, "Infraestrutura (1–5):", sat_infra_var),
            (10, "Material didático (1–5):", sat_material_var),
            (11, "Suporte/atendimento (1–5):", sat_suporte_var),
        ]
        for row, label, var in questions:
            create_likert_row(row, label, var)

    # ---------- LAYOUT ----------
    parent.columnconfigure(1, weight=1)
    parent.rowconfigure(20, weight=1)

    ttk.Label(parent, text="Nome:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
    ttk.Entry(parent, textvariable=nome_var).grid(
        row=1, column=1, columnspan=2, sticky="ew", padx=(1, 500)
    )

    ttk.Label(parent, text="Idade:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
    ttk.Spinbox(
        parent, from_=10, to=99, textvariable=idade_var,
        width=6, justify="center"
    ).grid(row=2, column=1, sticky="w", pady=1)

    ttk.Label(parent, text="E-mail:").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
    ttk.Entry(parent, textvariable=email_var).grid(
        row=3, column=1, columnspan=2, sticky="ew", padx=(1, 500)
    )

    ttk.Label(parent, text="Curso:").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
    curso_cb = ttk.Combobox(
        parent,
        textvariable=curso_var,
        state="readonly",
        values=["ADS", "SI", "Engenharia", "Administração"]
    )
    curso_cb.grid(row=4, column=1, sticky="ew", padx=(1, 650))

    ttk.Label(parent, text="Turno:").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
    turnos = ttk.Frame(parent)
    turnos.grid(row=5, column=1, columnspan=2, sticky="w")
    for t in ["Manhã", "Tarde", "Noite"]:
        ttk.Radiobutton(turnos, text=t, value=t, variable=turno_var).pack(
            side="left", padx=(0, 8)
        )

    ttk.Label(parent, text="Presença:").grid(row=6, column=0, sticky="w", padx=(0, 8), pady=4)
    pres = ttk.Frame(parent)
    pres.grid(row=6, column=1, columnspan=2, sticky="w")
    for p in ["Presencial", "Remoto"]:
        ttk.Radiobutton(pres, text=p, value=p, variable=presenca_var).pack(
            side="left", padx=(0, 8)
        )

    # Likert
    create_likert_scales()

    ttk.Checkbutton(
        parent,
        text="Deseja receber avisos por e-mail?",
        variable=avisos_var
    ).grid(row=12, column=1, columnspan=2, sticky="w", pady=4)

    botoes = ttk.Frame(parent)
    botoes.grid(row=13, column=0, columnspan=3, sticky="e", pady=(12, 0))
    ttk.Button(botoes, text="Limpar", command=limpar).pack(side="right", padx=6)
    ttk.Button(botoes, text="Salvar", command=salvar).pack(side="right")

    return {
        "limpar": limpar,
        "salvar": salvar,
    }
