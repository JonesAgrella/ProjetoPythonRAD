from tkinter import ttk

# Theme colors
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

    return style