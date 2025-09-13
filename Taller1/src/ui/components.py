import tkinter as tk
from tkinter import ttk, messagebox

# --- Color theme (ttk) --------------------------------------------------------
def apply_color_theme(root):
    """
    Aplica una paleta de colores moderna a los widgets ttk.
    Llama a esta función una vez después de crear `Tk()`.
    """
    import colorsys
    from tkinter import ttk
    
    PALETTE = {
        "bg": "#F8FAFC",          # slate-50
        "card": "#FFFFFF",
        "text": "#0F172A",        # slate-900
        "muted": "#475569",       # slate-600
        "primary": "#2563EB",     # blue-600
        "primary_dk": "#1E40AF",  # blue-800
        "success": "#16A34A",     # green-600
        "danger": "#DC2626",      # red-600
        "warn": "#F59E0B",        # amber-500
        "border": "#E2E8F0",      # slate-200
        "stripe": "#F1F5F9"       # slate-100
    }
    
    style = ttk.Style(root)
    # Usamos 'clam' como base para que los colores se respeten en todas las plataformas
    try:
        style.theme_create('RegexTheme', parent='clam', settings={
            'TFrame': {
                'configure': {'background': PALETTE['bg']}
            },
            'TLabelframe': {
                'configure': {'background': PALETTE['bg'], 'borderwidth': 1, 'relief': 'solid'},
            },
            'TLabelframe.Label': {
                'configure': {'background': PALETTE['bg'], 'foreground': PALETTE['text'], 'font': ('Segoe UI', 10, 'bold')}
            },
            'TLabel': {
                'configure': {'background': PALETTE['bg'], 'foreground': PALETTE['text']}
            },
            'TEntry': {
                'configure': {'fieldbackground': '#FFFFFF'}
            },
            'TCombobox': {
                'configure': {'fieldbackground': '#FFFFFF'}
            },
            'TButton': {
                'configure': {
                    'padding': 8,
                    'background': PALETTE['primary'],
                    'foreground': '#FFFFFF',
                    'borderwidth': 0
                },
                'map': {
                    'background': [('active', PALETTE['primary_dk']), ('disabled', PALETTE['border'])],
                    'foreground': [('disabled', '#94A3B8')]
                }
            },
            'Secondary.TButton': {
                'configure': {
                    'padding': 8,
                    'background': PALETTE['stripe'],
                    'foreground': PALETTE['text'],
                    'borderwidth': 0
                },
                'map': {
                    'background': [('active', PALETTE['border'])]
                }
            },
            'Danger.TButton': {
                'configure': {
                    'padding': 8,
                    'background': PALETTE['danger'],
                    'foreground': '#FFFFFF',
                    'borderwidth': 0
                },
                'map': {'background': [('active', '#991B1B')]}
            },
            'Success.TLabel': {
                'configure': {'foreground': PALETTE['success'], 'background': PALETTE['bg'], 'font': ('Segoe UI', 10, 'bold')}
            },
            'Danger.TLabel': {
                'configure': {'foreground': PALETTE['danger'], 'background': PALETTE['bg'], 'font': ('Segoe UI', 10, 'bold')}
            },
            'Muted.TLabel': {
                'configure': {'foreground': PALETTE['muted'], 'background': PALETTE['bg']}
            },
            'Treeview': {
                'configure': {
                    'background': '#FFFFFF',
                    'fieldbackground': '#FFFFFF',
                    'foreground': PALETTE['text'],
                    'rowheight': 24,
                    'bordercolor': PALETTE['border'],
                    'lightcolor': PALETTE['border'],
                    'darkcolor': PALETTE['border']
                }
            },
            'Treeview.Heading': {
                'configure': {
                    'background': PALETTE['stripe'],
                    'foreground': PALETTE['text'],
                    'font': ('Segoe UI', 10, 'bold'),
                    'borderwidth': 1
                }
            },
            'TNotebook': {
                'configure': {'background': PALETTE['bg'], 'tabmargins': [4, 4, 4, 0]}
            },
            'TNotebook.Tab': {
                'configure': {'padding': [10, 6], 'background': PALETTE['stripe']},
                'map': {'background': [('selected', '#FFFFFF')]}
            }
        })
    except tk.TclError:
        # Si ya existe (por hot-reload), ignorar
        pass
    
    style.theme_use('RegexTheme')
    # Fijar color de fondo del root (afecta a widgets tk.*)
    root.configure(bg=PALETTE['bg'])
    
    # Exponer la paleta para quien la quiera usar puntualmente
    root.__dict__['PALETTE'] = PALETTE
# ------------------------------------------------------------------------------


class LabeledEntry(tk.Frame):
    def __init__(self, master, label, textvariable=None, **kwargs):
        super().__init__(master)
        tk.Label(self, text=label).pack(side="left", padx=5)
        self.entry = tk.Entry(self, textvariable=textvariable, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

class LabeledCheck(tk.Frame):
    def __init__(self, master, label, variable, **kwargs):
        super().__init__(master)
        self.check = tk.Checkbutton(self, text=label, variable=variable, **kwargs)
        self.check.pack(side="left")

class LabeledButton(tk.Frame):
    def __init__(self, master, label, command, **kwargs):
        super().__init__(master)
        self.button = tk.Button(self, text=label, command=command, **kwargs)
        self.button.pack(side="left")

class ResultsTable(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, columns=("linea", "correo", "estado", "motivo"), show="headings", **kwargs)
        for col in ["linea", "correo", "estado", "motivo"]:
            self.heading(col, text=col.capitalize())
            self.column(col, width=120)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create a frame inside the canvas for widgets
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ResultTable(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create filter frame
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Filter label
        ttk.Label(filter_frame, text="Filtrar:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Filter combobox
        self.filter_var = tk.StringVar(value="Todos")
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                          values=["Todos", "Válidos", "Inválidos"], 
                                          width=10, state="readonly")
        self.filter_combo.pack(side=tk.LEFT)
        self.filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)
        
        # Create treeview for results
        columns = ("#", "Correo", "Estado", "Motivo")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Configure columns
        self.tree.heading("#", text="#")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Motivo", text="Motivo")
        
        self.tree.column("#", width=50, anchor="center")
        self.tree.column("Correo", width=250)
        self.tree.column("Estado", width=100, anchor="center")
        self.tree.column("Motivo", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Estilos de filas (zebra) y estados
        try:
            pal = getattr(self.winfo_toplevel(), 'PALETTE', None) or {}
        except Exception:
            pal = {}
        stripe = pal.get('stripe', '#F1F5F9')
        base = pal.get('card', '#FFFFFF')
        success = pal.get('success', '#16A34A')
        danger = pal.get('danger', '#DC2626')
        
        self.tree.tag_configure('oddrow', background=base)
        self.tree.tag_configure('evenrow', background=stripe)
        self.tree.tag_configure('valido', foreground=success)
        self.tree.tag_configure('invalido', foreground=danger)
    
        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store all results for filtering
        self.all_results = []
    
    def add_row(self, row_data):
        """Add a row to the table with the given data."""
        self.all_results.append(row_data)
        idx = len(self.all_results)-1
        tag = "evenrow" if (idx % 2 == 0) else "oddrow"
        estado = str(row_data[2]).lower()
        estado_tag = "valido" if "válido" in estado or "valido" in estado else "invalido"
        self.tree.insert("", "end", values=row_data, tags=(tag, estado_tag))
    
    def clear(self):
        """Clear all rows from the table."""
        self.all_results = []
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_all_data(self):
        """Get all data from the table."""
        return self.all_results
    
    def apply_filter(self, event=None):
        """Apply filter to the table."""
        filter_value = self.filter_var.get()
        
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Apply filter
        for row in self.all_results:
            if filter_value == "Todos" or \
               (filter_value == "Válidos" and row[2] == "Válido") or \
               (filter_value == "Inválidos" and row[2] == "Inválido"):
                self.tree.insert("", "end", values=row)

class StatsFrame(ttk.LabelFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, text="Estadísticas", *args, **kwargs)
        
        # Initialize stats dictionary
        self.stats = {
            "total": 0,
            "validos": 0,
            "invalidos": 0,
            "precision": 0,
            "motivos": {}
        }
        
        # Create labels for stats
        self.total_label = ttk.Label(self, text=f"Total: {self.stats['total']}")
        self.total_label.pack(anchor="w", padx=5, pady=2)
        
        self.validos_label = ttk.Label(self, text=f"Válidos: {self.stats['validos']}", style='Success.TLabel')
        self.validos_label.pack(anchor="w", padx=5, pady=2)
        
        self.invalidos_label = ttk.Label(self, text=f"Inválidos: {self.stats['invalidos']}", style='Danger.TLabel')
        self.invalidos_label.pack(anchor="w", padx=5, pady=2)
        
        self.precision_label = ttk.Label(self, text=f"Precisión: {self.stats['precision']:.2f}%")
        self.precision_label.pack(anchor="w", padx=5, pady=2)
        
        # Frame for motivos
        self.motivos_frame = ttk.LabelFrame(self, text="Motivos de invalidez")
        self.motivos_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Will be filled dynamically
        self.motivo_labels = []
    
    def update_stats(self, stats):
        """Update stats display with new data."""
        self.stats = stats
        
        # Update basic stats
        self.total_label.config(text=f"Total: {stats['total']}")
        self.validos_label.config(text=f"Válidos: {stats['validos']}")
        self.invalidos_label.config(text=f"Inválidos: {stats['invalidos']}")
        self.precision_label.config(text=f"Precisión: {stats['precision']:.2f}%")
        
        # Clear previous motivo labels
        for label in self.motivo_labels:
            label.destroy()
        self.motivo_labels = []
        
        # Add new motivo labels
        for motivo, cantidad in sorted(stats['motivos'].items(), key=lambda x: x[1], reverse=True):
            label = ttk.Label(self.motivos_frame, text=f"{motivo}: {cantidad}")
            label.pack(anchor="w", padx=5, pady=1)
            self.motivo_labels.append(label)
    
    def get_stats(self):
        """Return the current stats."""
        return self.stats

class RegexTester(ttk.LabelFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, text="Probar Expresión Regular", *args, **kwargs)
        
        # Sample input frame
        sample_frame = ttk.Frame(self)
        sample_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sample_frame, text="Correo de prueba:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.sample_var = tk.StringVar()
        self.sample_entry = ttk.Entry(sample_frame, textvariable=self.sample_var, width=40)
        self.sample_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.test_button = ttk.Button(sample_frame, text="Probar", command=self.test_regex)
        self.test_button.pack(side=tk.LEFT)
        
        # Result frame
        result_frame = ttk.Frame(self)
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(result_frame, text="Resultado:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.result_var = tk.StringVar(value="")
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var)
        self.result_label.pack(side=tk.LEFT)
        
        # Set callbacks
        self.regex_callback = None
        self.case_sensitive_callback = None
    
    def set_callbacks(self, regex_callback, case_sensitive_callback):
        """Set callback functions to get regex and case sensitivity."""
        self.regex_callback = regex_callback
        self.case_sensitive_callback = case_sensitive_callback
    
    def test_regex(self):
        """Testea la regex contra el input de muestra."""
        if not self.regex_callback or not self.case_sensitive_callback:
            messagebox.showerror("Error", "Callbacks no configurados")
            return

        sample = self.sample_var.get().strip()
        if not sample:
            self.result_var.set("Ingrese un correo de prueba")
            return

        # Obtener regex y sensibilidad
        regex = self.regex_callback()
        case_sensitive = self.case_sensitive_callback()

        # Importar funciones de validación
        from src.scripts.reg import probar_regex, analizar_motivo, extraer_año, validar_año_rango, compilar_regex

        # Compilar regex
        compiled_regex, _ = compilar_regex(regex, case_sensitive)
        if not compiled_regex:
            self.result_var.set("Error en la expresión regular")
            self.result_label.configure(style="Danger.TLabel")
            return

        # Validar patrón básico
        if probar_regex(regex, case_sensitive, sample):
            año = extraer_año(sample)
            if validar_año_rango(año):
                self.result_var.set("✅ Válido")
                self.result_label.configure(style="Success.TLabel")
            else:
                self.result_var.set(f"❌ Inválido: año {año} fuera del rango (2010-2025)")
                self.result_label.configure(style="Danger.TLabel")
        else:
            motivo = analizar_motivo(sample)
            self.result_var.set(f"❌ Inválido: {motivo}")
            self.result_label.configure(style="Danger.TLabel")
