import tkinter as tk
from tkinter import ttk
from ui.theme import apply_azure_theme
from ui.form import FormTab
from ui.charts import ChartsTab
from db import init_db

def main():
    # Create main window
    root = tk.Tk()
    root.title("Pesquisa - Estácio")
    root.geometry("980x620")

    # Apply theme
    apply_azure_theme(root, "azure.tcl", dark=True)

    # Create notebook for tabs
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # Create tabs
    tab_form = ttk.Frame(nb, padding=12)
    tab_charts = ttk.Frame(nb, padding=12)
    
    # Add tabs to notebook
    nb.add(tab_form, text="Cadastro")
    nb.add(tab_charts, text="Gráficos")

    # Initialize charts tab
    charts = ChartsTab(tab_charts)
    
    # Initialize form tab with callback to refresh charts
    form = FormTab(tab_form, charts.refresh_button_state)

    # Initialize database
    init_db()

    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
