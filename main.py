import tkinter as tk
from tkinter import ttk
from ui.theme import apply_azure_theme
from ui.charts import create_charts_tab
from ui.form import create_form
from db import init_db

def main():

    root = tk.Tk()
    root.title("Pesquisa - Estácio")
    root.geometry("980x620")

    apply_azure_theme(root, dark=True)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    tab_form = ttk.Frame(nb, padding=12)
    tab_charts = ttk.Frame(nb, padding=12)
    
    nb.add(tab_form, text="Cadastro")
    nb.add(tab_charts, text="Gráficos")

    charts_actions = create_charts_tab(tab_charts)
    form_actions = create_form(tab_form, charts_actions["refresh_button_state"])

    init_db()

    root.mainloop()

if __name__ == "__main__":
    main()
