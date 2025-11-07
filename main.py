import os
import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ---------------------- Personalização Tkinter ----------------------
PRIMARY = "#338DD6"
BG = "#ECECEC"
FG = "#111827"  # texto

def apply_azure_theme(root, tcl_path="azure.tcl", dark=False):
    style = ttk.Style()

    # tenta carregar o tema Azure; se não encontrar, cai para 'clam'
    try:
        root.tk.call("source", tcl_path)
        style.theme_use("azure-dark" if dark else "azure")
    except Exception:
        style.theme_use("clam")

    # fundo da janela e frames
    root.configure(bg=BG)
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG, padding=2)
    style.configure(".", font=("Segoe UI", 10))

    # Notebook e abas
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(16, 8))
    style.map("TNotebook.Tab",
              background=[("selected", PRIMARY)],
              foreground=[("selected", "white")])

    # Entradas/Combos
    style.configure("TEntry", fieldbackground="white", foreground=FG)
    style.configure("TCombobox", fieldbackground="white", foreground=FG)

    # Check/Radio
    style.configure("TCheckbutton", background=BG, foreground=FG)
    style.configure("TRadiobutton", background=BG, foreground=FG)

    # Botões (primário + padrão)
    style.configure("TButton", padding=(12, 6), borderwidth=0)
    style.configure("Primary.TButton", background=PRIMARY, foreground="white")
    style.map("Primary.TButton",
              background=[("active", "#1d36a2"), ("disabled", "#000000")],
              foreground=[("disabled", "white")])

    # mensagem info (para labels de aviso)
    style.configure("Info.TLabel", foreground="#4b5563", background=BG)

    # deixar as colunas dos sliders expansíveis (ajuste se já tiver isso)
    # tab_form.columnconfigure(2, weight=1)  # faça isso depois de criar o tab_form

    return style


# ---------------------- DB ----------------------
DB_PATH = "pesquisa_estacio.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL,
            turno TEXT NOT NULL,
            presenca TEXT NOT NULL,
            sat_geral INTEGER NOT NULL,
            sat_clareza INTEGER NOT NULL,
            sat_infra INTEGER NOT NULL,
            sat_material INTEGER NOT NULL,
            sat_suporte INTEGER NOT NULL,
            avisos INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def insert_resposta(d):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO respostas
        (nome, idade, email, curso, turno, presenca,
         sat_geral, sat_clareza, sat_infra, sat_material, sat_suporte, avisos)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        d["nome"], d["idade"], d["email"], d["curso"], d["turno"], d["presenca"],
        d["sat_geral"], d["sat_clareza"], d["sat_infra"], d["sat_material"], d["sat_suporte"],
        1 if d["avisos"] else 0
    ))
    con.commit()
    con.close()

def fetch_all():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM respostas ORDER BY id ASC")
    rows = cur.fetchall()
    con.close()
    return rows

def count_rows():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM respostas")
    n = cur.fetchone()[0]
    con.close()
    return n


# ---------------------- UI ----------------------
root = tk.Tk()
root.title("Pesquisa - Estácio")
root.geometry("980x620")

apply_azure_theme(root, "azure.tcl", dark=True)


from tkinter import ttk

nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True)

tab_form = ttk.Frame(nb, padding=12)
tab_charts = ttk.Frame(nb, padding=12)
nb.add(tab_form, text="Cadastro")
nb.add(tab_charts, text="Gráficos")

# layout
tab_form.columnconfigure(1, weight=1)
tab_form.rowconfigure(20, weight=1)

# vars
nome_var = tk.StringVar()
idade_var = tk.StringVar()
email_var = tk.StringVar()
curso_var = tk.StringVar()
turno_var = tk.StringVar(value="Manhã")
presenca_var = tk.StringVar(value="Presente")
sat_geral_var = tk.IntVar(value=3)
sat_clareza_var = tk.IntVar(value=3)
sat_infra_var = tk.IntVar(value=3)
sat_material_var = tk.IntVar(value=3)
sat_suporte_var = tk.IntVar(value=3)
avisos_var = tk.BooleanVar(value=False)

# helpers
def likert_row(row, label, var):
    def snap(value):
        var.set(round(float(value)))

    ttk.Label(tab_form, text=label).grid(
        row=row, column=0, sticky="w", padx=(0,8), pady=4
    )

    ttk.Label(tab_form, textvariable=var, width=2).grid(
        row=row, column=2, sticky="w", padx=(1,8)
    )

    ttk.Scale(
        tab_form,
        from_=1,
        to=5,
        variable=var,
        orient="horizontal",
        command=snap
    ).grid(
        row=row, column=1,
        sticky="ew",  # ⬅ permite expandir
        pady=4,
        padx=(1,100)
    )

# linha 1: Nome
ttk.Label(tab_form, text="Nome:").grid(row=1, column=0, sticky="w", padx=(0,8), pady=4)
ttk.Entry(tab_form, textvariable=nome_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=(1, 500))

# linha 2: Idade
ttk.Label(tab_form, text="Idade:").grid(row=2, column=0, sticky="w", padx=(0,8), pady=4)
ttk.Spinbox(tab_form, from_=10, to=99, textvariable=idade_var, width=6, justify="center").grid(
    row=2, column=1, sticky="w", pady=1
)

# linha 3: Email
ttk.Label(tab_form, text="E-mail:").grid(row=3, column=0, sticky="w", padx=(0,8), pady=4)
ttk.Entry(tab_form, textvariable=email_var).grid(row=3, column=1, columnspan=2, sticky="ew", padx=(1, 500))

# linha 4: Curso
ttk.Label(tab_form, text="Curso:").grid(row=4, column=0, sticky="w", padx=(0,8), pady=4)
curso_cb = ttk.Combobox(
    tab_form, textvariable=curso_var, state="readonly",
    values=["ADS", "SI", "Engenharia", "Administração"])
curso_cb.grid(row=4, column=1, sticky="ew", padx=(1, 650))

# linha 5: Turno
ttk.Label(tab_form, text="Turno:").grid(row=5, column=0, sticky="w", padx=(0,8), pady=4)
turnos = ttk.Frame(tab_form)
turnos.grid(row=5, column=1, columnspan=2, sticky="w")
for t in ["Manhã", "Tarde", "Noite"]:
    ttk.Radiobutton(turnos, text=t, value=t, variable=turno_var).pack(side="left", padx=(0,8))

# linha 6: Presença
ttk.Label(tab_form, text="Presença:").grid(row=6, column=0, sticky="w", padx=(0,8), pady=4)
pres = ttk.Frame(tab_form)
pres.grid(row=6, column=1, columnspan=2, sticky="w")
for p in ["Presente", "Faltou", "Remoto"]:
    ttk.Radiobutton(pres, text=p, value=p, variable=presenca_var).pack(side="left", padx=(0,8))

# linhas 7–11: Perguntas (Likert 1–5)
likert_row(7,  "Satisfação Geral (1–5):", sat_geral_var)
likert_row(8,  "Qualidade do professor(a) (1–5):", sat_clareza_var)
likert_row(9,  "Infraestrutura (1–5):", sat_infra_var)
likert_row(10, "Material didático (1–5):", sat_material_var)
likert_row(11, "Suporte/atendimento (1–5):", sat_suporte_var)

# linha 12: Avisos
ttk.Checkbutton(tab_form, text="Deseja receber avisos por e-mail?", variable=avisos_var).grid(
    row=12, column=1, columnspan=2, sticky="w", pady=4
)

# botões
botoes = ttk.Frame(tab_form)
botoes.grid(row=13, column=0, columnspan=3, sticky="e", pady=(12,0))

# validação
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

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
    presenca_var.set("Presente")
    for v in [sat_geral_var, sat_clareza_var, sat_infra_var, sat_material_var, sat_suporte_var]:
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
        refresh_charts_button_state()
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Ocorreu um erro: {e}")

ttk.Button(botoes, text="Limpar", command=limpar).pack(side="right", padx=6)
ttk.Button(botoes, text="Salvar", command=salvar).pack(side="right")

# ---------------------- Gráficos ----------------------
charts_header = ttk.Frame(tab_charts)
charts_header.pack(fill="x")

info_lbl = ttk.Label(
    charts_header,
    text="Os gráficos são habilitados após 5 respostas."
)
info_lbl.pack(side="left")

btn_refresh = ttk.Button(charts_header, text="Atualizar gráficos")
btn_refresh.pack(side="right")

charts_body = ttk.Frame(tab_charts)
charts_body.pack(fill="both", expand=True)

canvas_widgets = []

def clear_charts():
    for w in canvas_widgets:
        w.get_tk_widget().destroy()
    canvas_widgets.clear()

def plot_charts():
    clear_charts()
    rows = fetch_all()
    if len(rows) < 5:
        messagebox.showwarning("Atenção", "Colete pelo menos 5 respostas para ver os gráficos.")
        return

    # unpack columns (ver CREATE TABLE para índices)
    turnos = [r[5] for r in rows]
    sats_geral = [r[7] for r in rows]
    idade = [r[2] for r in rows]

    # 1) Barras: contagem por nota de satisfação geral
    fig1 = Figure(figsize=(5,2.6), dpi=100)
    ax1 = fig1.add_subplot(111)
    notas = [1,2,3,4,5]
    cont = [sats_geral.count(n) for n in notas]
    ax1.bar(notas, cont)
    ax1.set_title("Distribuição da Satisfação Geral")
    ax1.set_xlabel("Nota")
    ax1.set_ylabel("Quantidade")
    canvas1 = FigureCanvasTkAgg(fig1, master=charts_body)
    canvas1.draw(); canvas1.get_tk_widget().pack(fill="x", pady=6)
    canvas_widgets.append(canvas1)

    # 2) Pizza: participação por Turno
    fig2 = Figure(figsize=(5,2.6), dpi=100)
    ax2 = fig2.add_subplot(111)
    grupos = ["Manhã","Tarde","Noite"]
    partes = [turnos.count(g) for g in grupos]
    ax2.pie(partes, labels=grupos, autopct="%1.0f%%", startangle=90)
    ax2.set_title("Respostas por Turno")
    canvas2 = FigureCanvasTkAgg(fig2, master=charts_body)
    canvas2.draw(); canvas2.get_tk_widget().pack(fill="x", pady=6)
    canvas_widgets.append(canvas2)

    # 3) Linha: satisfação geral ao longo das respostas (ou por idade média rolante)
    fig3 = Figure(figsize=(5,2.6), dpi=100)
    ax3 = fig3.add_subplot(111)
    ax3.plot(range(1, len(sats_geral)+1), sats_geral, marker="o")
    ax3.set_title("Evolução da Satisfação Geral")
    ax3.set_xlabel("Resposta #")
    ax3.set_ylabel("Nota")
    ax3.set_ylim(1,5)
    canvas3 = FigureCanvasTkAgg(fig3, master=charts_body)
    canvas3.draw(); canvas3.get_tk_widget().pack(fill="x", pady=6)
    canvas_widgets.append(canvas3)

def refresh_charts_button_state():
    n = count_rows()
    if n >= 5:
        btn_refresh.config(state="normal")
        info_lbl.config(text=f"{n} respostas registradas. Clique em 'Atualizar gráficos'.")
    else:
        btn_refresh.config(state="disabled")
        info_lbl.config(text=f"{n} respostas registradas. Os gráficos ativam a partir de 5.")

btn_refresh.config(command=plot_charts)

# boot
init_db()
refresh_charts_button_state()

root.mainloop()
