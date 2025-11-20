from tkinter import ttk, messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db import fetch_all, count_rows


def create_charts_tab(parent):

    #  FRAME COM SCROLL 
    container = ttk.Frame(parent)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        container, orient="vertical", command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    charts_frame = ttk.Frame(canvas)
    
    frame_window = canvas.create_window((0, 0), window=charts_frame, anchor="nw")

    # sempre que o canvas mudar de tamanho, ajustamos:
    def on_canvas_configure(event):
        
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.itemconfig(frame_window, width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    
    canvas_widgets = []

    #  HEADER 
    charts_header = ttk.Frame(charts_frame)
    charts_header.pack(fill="x")

    info_lbl = ttk.Label(
        charts_header,
        text="Os gráficos são habilitados após 5 respostas."
    )
    info_lbl.pack(side="left")

    charts_body = ttk.Frame(charts_frame)
    charts_body.pack(fill="both", expand=True, pady=10)

    
    charts_body.columnconfigure(0, weight=1)

    # FUNÇÕES 

    def clear_charts():
        for w in canvas_widgets:
            w.get_tk_widget().destroy()
        canvas_widgets.clear()
        canvas.yview_moveto(0)  

    def plot_charts():
        clear_charts()
        rows = fetch_all()
        if len(rows) < 5:
            messagebox.showwarning(
                "Atenção",
                "Colete pelo menos 5 respostas para ver os gráficos."
            )
            return

        turnos = [r[5] for r in rows]
        sats_geral = [r[7] for r in rows]

        
        fig1 = Figure(figsize=(6, 3), dpi=100)
        fig1.subplots_adjust(bottom=0.18)
        ax1 = fig1.add_subplot(111)
        notas = [1, 2, 3, 4, 5]
        cont = [sats_geral.count(n) for n in notas]
        ax1.bar(notas, cont)
        ax1.set_title("Distribuição da Satisfação Geral")
        ax1.set_xlabel("Nota")
        ax1.set_ylabel("Quantidade")

        canvas1 = FigureCanvasTkAgg(fig1, master=charts_body)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, pady=10)
        canvas_widgets.append(canvas1)

        
        fig2 = Figure(figsize=(6, 3), dpi=100)
        fig2.subplots_adjust(bottom=0.18)
        ax2 = fig2.add_subplot(111)
        grupos = ["Manhã", "Tarde", "Noite"]
        partes = [turnos.count(g) for g in grupos]
        ax2.pie(partes, labels=grupos, autopct="%1.0f%%", startangle=90)
        ax2.set_title("Respostas por Turno")

        canvas2 = FigureCanvasTkAgg(fig2, master=charts_body)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=1, column=0, pady=10)
        canvas_widgets.append(canvas2)

        
        fig3 = Figure(figsize=(6, 3), dpi=100)
        fig3.subplots_adjust(bottom=0.18)
        ax3 = fig3.add_subplot(111)
        ax3.plot(range(1, len(sats_geral) + 1), sats_geral, marker="o")
        ax3.set_title("Evolução da Satisfação Geral")
        ax3.set_xlabel("Respostas")
        ax3.set_ylabel("Nota")
        ax3.set_ylim(1, 5)

        canvas3 = FigureCanvasTkAgg(fig3, master=charts_body)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=2, column=0, pady=10)
        canvas_widgets.append(canvas3)

        canvas.configure(scrollregion=canvas.bbox("all"))

    def refresh_button_state():
        n = count_rows()
        if n >= 5:
            btn_refresh.config(state="normal")
            info_lbl.config(
                text=f"{n} respostas registradas. Clique em 'Atualizar gráficos'."
            )
        else:
            btn_refresh.config(state="disabled")
            info_lbl.config(
                text=f"{n} respostas registradas. Os gráficos ativam a partir de 5."
            )

    btn_refresh = ttk.Button(
        charts_header,
        text="Atualizar gráficos",
        command=plot_charts
    )
    btn_refresh.pack(side="right")

    refresh_button_state()

    return {
        "refresh_button_state": refresh_button_state,
        "plot_charts": plot_charts,
    }
