import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import csv

# Habilitar ejecución como script (añade ../ al sys.path)
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Ejecución como paquete: python -m ui.main_window
    from .components import ScrollableFrame, ResultTable, StatsFrame, RegexTester, apply_color_theme
    from ..scripts.reg import compilar_regex, validar_lineas, generar_estadisticas
    from ..utils.file_handler import read_file, save_file, file_exists
except Exception:
    # Ejecución directa: python ui/main_window.py (requiere que 'src' esté en sys.path)
    from ui.components import ScrollableFrame, ResultTable, StatsFrame, RegexTester, apply_color_theme
    from scripts.reg import compilar_regex, validar_lineas, generar_estadisticas
    from utils.file_handler import read_file, save_file, file_exists


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Aplicar tema de colores
        try:
            apply_color_theme(self)
        except Exception:
            pass
        
        self.title("Validador de Correos Electrónicos")
        self.geometry("1000x750")
        self.minsize(800, 600)
        self.configure(padx=10, pady=10)
        
        # Expresión regular predeterminada
        self.default_pattern = r"^[a-zA-Z]+[._-][a-zA-Z]+[0-9]{4}@techsolutions\.cl$"
        self.patron_var = tk.StringVar(value=self.default_pattern)
        self.case_sensitive_var = tk.BooleanVar(value=True)

        
        # Variables para el archivo
        self.current_file = None
        self.file_content = []
        
        # Variables para resultados
        self.resultados = []
        
        # Crear pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de configuración
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuración")
        
        # Pestaña de resultados
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Resultados")
        
        # Inicializar interfaz
        self.create_config_widgets()
        self.create_results_widgets()
    
    def create_config_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.config_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para cargar archivo
        file_frame = ttk.LabelFrame(main_frame, text="Archivo de correos")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Crear controles para cargar archivo
        file_controls = ttk.Frame(file_frame)
        file_controls.pack(fill=tk.X, padx=5, pady=5)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_controls, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_button = ttk.Button(file_controls, text="Examinar...", command=self.browse_file)
        browse_button.pack(side=tk.LEFT)
        
        # Mostrar contenido del archivo
        file_content_frame = ttk.Frame(file_frame)
        file_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(file_content_frame, text="Contenido del archivo:").pack(anchor="w")
        
        self.file_content_text = tk.Text(file_content_frame, height=10, wrap=tk.WORD)
        self.file_content_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        file_scrollbar = ttk.Scrollbar(self.file_content_text, command=self.file_content_text.yview)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_content_text.config(yscrollcommand=file_scrollbar.set)
        
        # Frame para configurar regex
        regex_frame = ttk.LabelFrame(main_frame, text="Expresión Regular")
        regex_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Crear controles para regex
        regex_controls = ttk.Frame(regex_frame)
        regex_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(regex_controls, text="Patrón:").pack(side=tk.LEFT, padx=(0, 5))
        
        regex_entry = ttk.Entry(regex_controls, textvariable=self.patron_var, width=50)
        regex_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        reset_button = ttk.Button(regex_controls, text="Restaurar", 
                                  command=lambda: self.patron_var.set(self.default_pattern))
        reset_button.pack(side=tk.LEFT, padx=(0, 5))
        
        case_check = ttk.Checkbutton(regex_controls, text="Sensible a mayúsculas/minúsculas", 
                                     variable=self.case_sensitive_var)
        case_check.pack(side=tk.LEFT)
        
        # Frame para probar regex
        self.regex_tester = RegexTester(regex_frame)
        self.regex_tester.pack(fill=tk.X, padx=5, pady=5)
        self.regex_tester.set_callbacks(
            lambda: self.patron_var.get(),
            lambda: self.case_sensitive_var.get()
        )
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=10)
        
        validate_button = ttk.Button(action_frame, text="Validar correos", command=self.validate_emails)
        validate_button.pack(side=tk.RIGHT)
    
    def create_results_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.results_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame superior para controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Información del archivo y regex
        info_frame = ttk.LabelFrame(control_frame, text="Información")
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.file_info_var = tk.StringVar(value="Archivo: No seleccionado")
        ttk.Label(info_frame, textvariable=self.file_info_var).pack(anchor="w", padx=5, pady=2)
        
        self.regex_info_var = tk.StringVar(value=f"Regex: {self.default_pattern}")
        ttk.Label(info_frame, textvariable=self.regex_info_var).pack(anchor="w", padx=5, pady=2)
        
        self.case_info_var = tk.StringVar(value="Sensibilidad: Case sensitive")
        ttk.Label(info_frame, textvariable=self.case_info_var).pack(anchor="w", padx=5, pady=2)
        
        # Botones de acción
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(side=tk.RIGHT)
        
        export_menu = tk.Menu(self, tearoff=0)
        export_menu.add_command(label="Exportar a TXT", command=lambda: self.export_results("txt"))
        export_menu.add_command(label="Exportar a CSV", command=lambda: self.export_results("csv"))
        
        export_button = ttk.Button(action_frame, text="Exportar")
        export_button.pack(side=tk.LEFT, padx=5)
        export_button.bind("<Button-1>", lambda e: export_menu.post(
            export_button.winfo_rootx(), 
            export_button.winfo_rooty() + export_button.winfo_height()
        ))
        
        config_button = ttk.Button(action_frame, text="Volver a configuración", 
                                  command=lambda: self.notebook.select(0))
        config_button.pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        results_container = ttk.Frame(main_frame)
        results_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabla de resultados
        table_frame = ttk.LabelFrame(results_container, text="Resultados")
        table_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))
        
        self.result_table = ResultTable(table_frame)
        self.result_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Estadísticas
        stats_frame = ttk.Frame(results_container)
        stats_frame.pack(fill=tk.Y, side=tk.RIGHT, padx=(0, 5), pady=5)
        
        self.stats_display = StatsFrame(stats_frame)
        self.stats_display.pack(fill=tk.BOTH, expand=True)
    
    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de correos",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            try:
                # Verificar que el archivo existe y es legible
                if not os.path.exists(filepath):
                    messagebox.showerror("Error", f"El archivo no existe: {filepath}")
                    return
                
                if not os.path.isfile(filepath):
                    messagebox.showerror("Error", f"No es un archivo válido: {filepath}")
                    return
                
                # Leer contenido
                content = read_file(filepath)
                if not content.strip():
                    messagebox.showwarning("Advertencia", "El archivo está vacío")
                
                # Actualizar UI
                self.current_file = filepath
                self.file_path_var.set(filepath)
                self.file_content_text.delete(1.0, tk.END)
                self.file_content_text.insert(tk.END, content)
                self.file_info_var.set(f"Archivo: {os.path.basename(filepath)}")
                
                # Guardar contenido para procesamiento
                self.file_content = content.strip().split('\n')
                
                messagebox.showinfo("Éxito", f"Archivo cargado correctamente: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def validate_emails(self):
        # Verificar que hay contenido para validar
        if not self.file_content:
            messagebox.showwarning("Advertencia", "No hay correos para validar. Cargue un archivo primero.")
            return
        
        # Verificar que la regex es válida
        patron = self.patron_var.get().strip()
        if not patron:
            messagebox.showerror("Error", "La expresión regular no puede estar vacía")
            return
        
        case_sensitive = self.case_sensitive_var.get()
        
        # Compilar regex
        regex, _ = compilar_regex(patron, case_sensitive)
        if not regex:
            messagebox.showerror("Error", "La expresión regular no es válida")
            return
        
        # Validar correos
        resultados = validar_lineas(self.file_content, regex, case_sensitive)
        self.resultados = resultados
        
        # Generar estadísticas
        stats = generar_estadisticas(resultados)
        
        # Actualizar información en la pestaña de resultados
        self.regex_info_var.set(f"Regex: {patron}")
        self.case_info_var.set(f"Sensibilidad: {'Case sensitive' if case_sensitive else 'Case insensitive'}")
        
        # Actualizar tabla de resultados
        self.result_table.clear()
        for result in resultados:
            self.result_table.add_row(result)
        
        # Actualizar estadísticas
        self.stats_display.update_stats(stats)
        
        # Cambiar a la pestaña de resultados
        self.notebook.select(1)
        
        messagebox.showinfo("Validación completada", 
                           f"Se validaron {stats['total']} correos.\n"
                           f"Válidos: {stats['validos']} ({stats['precision']:.2f}%)\n"
                           f"Inválidos: {stats['invalidos']}")
    
    def export_results(self, format_type):
        """Exporta los resultados a un archivo."""
        if not self.resultados:
            messagebox.showinfo("Sin datos", "No hay resultados para exportar.")
            return
        
        # Definir tipo de archivo y extensión
        if format_type == "txt":
            file_types = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            default_ext = ".txt"
        else:  # csv
            file_types = [("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            default_ext = ".csv"
        
        # Solicitar ubicación para guardar
        filepath = filedialog.asksaveasfilename(
            title=f"Guardar resultados como {format_type.upper()}",
            defaultextension=default_ext,
            filetypes=file_types
        )
        
        if not filepath:
            return  # Usuario canceló
        
        # Verificar si el archivo ya existe
        if file_exists(filepath):
            if not messagebox.askyesno("Confirmar sobrescritura", 
                                    f"El archivo {os.path.basename(filepath)} ya existe. ¿Desea sobrescribirlo?"):
                return
        
        try:
            # Obtener estadísticas
            stats = self.stats_display.get_stats()
            
            # Exportar según formato
            if format_type == "txt":
                self._export_txt(filepath, stats)
            else:  # csv
                self._export_csv(filepath)
                
            messagebox.showinfo("Éxito", f"Resultados guardados en: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar resultados: {str(e)}")
    
    def _export_txt(self, filepath, stats):
        """Exporta resultados a formato TXT."""
        # Formatear resultados
        output = "# Resultados de validación\n"
        output += f"{'#':<5} {'Correo':<40} {'Estado':<10} {'Motivo':<40}\n"
        output += "-" * 95 + "\n"
        
        for row in self.resultados:
            output += f"{row[0]:<5} {row[1]:<40} {row[2]:<10} {row[3]:<40}\n"
        
        # Añadir estadísticas
        output += "\n# Estadísticas\n"
        output += f"Total: {stats['total']}\n"
        output += f"Válidos: {stats['validos']} ({stats['precision']:.2f}%)\n"
        output += f"Inválidos: {stats['invalidos']}\n\n"
        
        output += "# Motivos de invalidez\n"
        for motivo, cantidad in sorted(stats['motivos'].items(), key=lambda x: x[1], reverse=True):
            output += f"- {motivo}: {cantidad}\n"
        
        # Guardar en archivo
        save_file(filepath, output)
    
    def _export_csv(self, filepath):
        """Exporta resultados a formato CSV."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Escribir encabezados
            writer.writerow(["#", "Correo", "Estado", "Motivo"])
            # Escribir datos
            for row in self.resultados:
                writer.writerow(row)