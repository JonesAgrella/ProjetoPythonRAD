import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Pesquisa RAP")
root.geometry("900x560")

nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True)

tab_form = ttk.Frame(nb, padding=12)
tab_charts = ttk.Frame(nb, padding=12)
nb.add(tab_form, text="Cadastro")
nb.add(tab_charts, text="Gráficos")

# --- configurar grade do tab_form ---
# col0 = labels, col1 = inputs (expansível), col2 = inputs auxiliares
tab_form.columnconfigure(1, weight=1)  # a coluna 1 cresce
tab_form.rowconfigure(10, weight=1)  # linha da tabela/rodapé cresce (se usar)

# --- variáveis ---
nome_var = tk.StringVar()
idade_var = tk.StringVar()
email_var = tk.StringVar()
curso_var = tk.StringVar()
turno_var = tk.StringVar(value="Manhã")
presenca_var = tk.StringVar(value="Presente")
satisfacao_var = tk.IntVar(value=3)
avisos_var = tk.BooleanVar(value=False)

# --- linha 0: Título/descrição (opcional) ---
ttk.Label(tab_form, text="Formulário de Cadastro", font=("Segoe UI", 14, "bold")).grid(
    row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
)

# --- linha 1: Nome ---
ttk.Label(tab_form, text="Nome:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
ttk.Entry(tab_form, textvariable=nome_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 500))

# --- linha 2: Idade ---
ttk.Label(tab_form, text="Idade:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
ttk.Spinbox(tab_form, from_=10, to=99, textvariable=idade_var, width=6, justify="center").grid(
    row=2, column=1, sticky="w", pady=4
)

# --- linha 3: E-mail ---
ttk.Label(tab_form, text="E-mail:").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
ttk.Entry(tab_form, textvariable=email_var).grid(row=3, column=1, columnspan=2, sticky="ew", padx=(0, 500))

# --- linha 4: Curso (Combobox) ---
ttk.Label(tab_form, text="Curso:").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
curso_cb = ttk.Combobox(tab_form, textvariable=curso_var, state="readonly",
                        values=["ADS", "SI", "Engenharia", "Administração"])
curso_cb.grid(row=4, column=1, sticky="ew", padx=(0, 500))

# --- linha 5: Turno (Radio) ---
ttk.Label(tab_form, text="Turno:").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
turnos = ttk.Frame(tab_form)
turnos.grid(row=5, column=1, columnspan=2, sticky="w")
for t in ["Manhã", "Tarde", "Noite"]:
    ttk.Radiobutton(turnos, text=t, value=t, variable=turno_var).pack(side="left", padx=(0, 8))

# --- linha 6: Presença (Radio) ---
ttk.Label(tab_form, text="Presença:").grid(row=6, column=0, sticky="w", padx=(0, 8), pady=4)
pres = ttk.Frame(tab_form)
pres.grid(row=6, column=1, columnspan=2, sticky="w")
for p in ["Presente", "Faltou", "Remoto"]:
    ttk.Radiobutton(pres, text=p, value=p, variable=presenca_var).pack(side="left", padx=(0, 8))

# --- linha 7: Satisfação (1–5) ---
ttk.Label(tab_form, text="Satisfação (1–5):").grid(row=7, column=0, sticky="w", padx=(0, 8), pady=4)
ttk.Scale(tab_form, from_=1, to=5, variable=satisfacao_var, orient="horizontal").grid(
    row=7, column=1, sticky="ew", pady=4
)

# --- linha 8: Avisos (Check) ---
ttk.Checkbutton(tab_form, text="Deseja receber avisos por e-mail?", variable=avisos_var).grid(
    row=8, column=1, columnspan=2, sticky="w", pady=4
)

# --- linha 9: Botões de ação ---
botoes = ttk.Frame(tab_form)
botoes.grid(row=9, column=0, columnspan=3, sticky="e", pady=(12, 0))


def salvar():
    print("salvar() chamado")  # aqui depois entra validação + insert SQLite


def limpar():
    nome_var.set("")
    idade_var.set("")
    email_var.set("")
    curso_var.set("")
    turno_var.set("Manhã")
    presenca_var.set("Presente")
    satisfacao_var.set(3)
    avisos_var.set(False)


ttk.Button(botoes, text="Limpar", command=limpar).pack(side="right", padx=6)
ttk.Button(botoes, text="Salvar", command=salvar).pack(side="right")

root.mainloop()
