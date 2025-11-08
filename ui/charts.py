from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db import fetch_all, count_rows

class ChartsTab:
    def __init__(self, parent):
        self.parent = parent
        self.canvas_widgets = []
        self.create_widgets()

    def create_widgets(self):
        self.charts_header = ttk.Frame(self.parent)
        self.charts_header.pack(fill="x")

        self.info_lbl = ttk.Label(
            self.charts_header,
            text="Os gráficos são habilitados após 5 respostas."
        )
        self.info_lbl.pack(side="left")

        self.btn_refresh = ttk.Button(
            self.charts_header, 
            text="Atualizar gráficos",
            command=self.plot_charts
        )
        self.btn_refresh.pack(side="right")

        self.charts_body = ttk.Frame(self.parent)
        self.charts_body.pack(fill="both", expand=True)

        self.refresh_button_state()

    def clear_charts(self):
        for w in self.canvas_widgets:
            w.get_tk_widget().destroy()
        self.canvas_widgets.clear()

    def plot_charts(self):
        self.clear_charts()
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
        canvas1 = FigureCanvasTkAgg(fig1, master=self.charts_body)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="x", pady=6)
        self.canvas_widgets.append(canvas1)

        # 2) Pizza: participação por Turno
        fig2 = Figure(figsize=(5,2.6), dpi=100)
        ax2 = fig2.add_subplot(111)
        grupos = ["Manhã","Tarde","Noite"]
        partes = [turnos.count(g) for g in grupos]
        ax2.pie(partes, labels=grupos, autopct="%1.0f%%", startangle=90)
        ax2.set_title("Respostas por Turno")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.charts_body)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="x", pady=6)
        self.canvas_widgets.append(canvas2)

        # 3) Linha: satisfação geral ao longo das respostas
        fig3 = Figure(figsize=(5,2.6), dpi=100)
        ax3 = fig3.add_subplot(111)
        ax3.plot(range(1, len(sats_geral)+1), sats_geral, marker="o")
        ax3.set_title("Evolução da Satisfação Geral")
        ax3.set_xlabel("Resposta #")
        ax3.set_ylabel("Nota")
        ax3.set_ylim(1,5)
        canvas3 = FigureCanvasTkAgg(fig3, master=self.charts_body)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="x", pady=6)
        self.canvas_widgets.append(canvas3)

    def refresh_button_state(self):
        n = count_rows()
        if n >= 5:
            self.btn_refresh.config(state="normal")
            self.info_lbl.config(text=f"{n} respostas registradas. Clique em 'Atualizar gráficos'.")
        else:
            self.btn_refresh.config(state="disabled")
            self.info_lbl.config(text=f"{n} respostas registradas. Os gráficos ativam a partir de 5.")