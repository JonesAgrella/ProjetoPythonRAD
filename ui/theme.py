import os
from tkinter import ttk

# Cores principais do tema
PRIMARY = "#338DD6"
BG = "#ECECEC"
FG = "#111827"  # texto


def _get_azure_tcl_path():
    """
    Retorna o caminho absoluto do arquivo azure.tcl.

    Considerando:
    ui/theme.py  (este arquivo)
    theme/azure.tcl (pasta vizinha ao nível de cima)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))       # .../ui
    theme_dir = os.path.join(base_dir, "..", "theme")           # .../theme
    tcl_path = os.path.join(theme_dir, "azure.tcl")             # .../theme/azure.tcl
    return os.path.abspath(tcl_path)


def apply_azure_theme(root, dark: bool = False):
    """
    Aplica o tema Azure se o azure.tcl for encontrado.
    Caso não consiga carregar, cai para o tema 'clam'.
    """
    style = ttk.Style()

    # tenta carregar o tema Azure; se não encontrar, cai para 'clam'
    try:
        tcl_path = _get_azure_tcl_path()
        root.tk.call("source", tcl_path)
        style.theme_use("azure-dark" if dark else "azure")
    except Exception:
        # fallback para um tema padrão do Tkinter
        style.theme_use("clam")

    # fundo da janela
    root.configure(bg=BG)

    # Frames e Labels
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG, padding=2)
    style.configure(".", font=("Segoe UI", 10))

    # Notebook e abas
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(16, 8))
    style.map(
        "TNotebook.Tab",
        background=[("selected", PRIMARY)],
        foreground=[("selected", "white")]
    )

    # Entradas/Combos
    style.configure("TEntry", fieldbackground="white", foreground=FG)
    style.configure("TCombobox", fieldbackground="white", foreground=FG)

    # Check/Radio
    style.configure("TCheckbutton", background=BG, foreground=FG)
    style.configure("TRadiobutton", background=BG, foreground=FG)

    # Botões (primário + padrão)
    style.configure("TButton", padding=(12, 6), borderwidth=0)
    style.configure("Primary.TButton", background=PRIMARY, foreground="white")
    style.map(
        "Primary.TButton",
        background=[("active", "#1d36a2"), ("disabled", "#000000")],
        foreground=[("disabled", "white")]
    )

    # Labels de informação
    style.configure("Info.TLabel", foreground="#4b5563", background=BG)

    return style
