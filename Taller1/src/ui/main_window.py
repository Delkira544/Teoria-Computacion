import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from src.ui.components import ResultsTable
from src.utils.file_handler import cargar_archivo_txt, exportar_resultados
from src.scripts.reg import compilar_regex, probar_regex, validar_lineas

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validador de Correos - Taller")
        self.geometry("700x400")
        self.lineas = []
        self.regex_str = r"^[a-zA-Z]+[._-][a-zA-Z]+[0-9]{4}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.case_sensitive = True
        self.regex = None
        self.resultados = []
        self.show_open_file()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_open_file(self):
        self.clear()
        tk.Label(self, text="Selecciona un archivo .txt con correos (uno por línea):").pack(pady=10)
        self.file_label = tk.Label(self, text="", fg="blue")
        self.file_label.pack(pady=5)
        tk.Button(self, text="Abrir .txt", command=self.cargar_archivo).pack()
        self.btn_next = tk.Button(self, text="Siguiente", state="disabled", command=self.show_regex_config)
        self.btn_next.pack(side="right", padx=10, pady=10)
        tk.Button(self, text="Salir", command=self.quit).pack(side="right", padx=10, pady=10)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not ruta:
            return
        lineas, error = cargar_archivo_txt(ruta)
        if error:
            messagebox.showerror("Error", error)
            return
        self.file_label.config(text=ruta)
        self.lineas = lineas
        self.btn_next.config(state="normal")

    def show_regex_config(self):
        self.clear()
        tk.Label(self, text="Expresión regular para validar correos:").pack(pady=5)
        self.regex_var = tk.StringVar(value=self.regex_str)
        tk.Entry(self, textvariable=self.regex_var, width=60).pack(pady=5)
        self.case_var = tk.BooleanVar(value=self.case_sensitive)
        tk.Checkbutton(self, text="Sensible a mayúsculas/minúsculas", variable=self.case_var).pack()
        tk.Button(self, text="Probar regex", command=self.probar_regex).pack(pady=5)
        tk.Label(self, text="Ejemplo válido: daniel.soto2025@dominio.com").pack()
        tk.Label(self, text="Ejemplo inválido: daniel..soto2025@dominio.com").pack()
        tk.Button(self, text="Atrás", command=self.show_open_file).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Siguiente", command=self.compilar_regex).pack(side="right", padx=10, pady=10)
        tk.Button(self, text="Salir", command=self.quit).pack(side="right", padx=10, pady=10)

    def probar_regex(self):
        cadena = simpledialog.askstring("Probar regex", "Ingresa una cadena para probar:")
        if cadena is None:
            return
        patron = self.regex_var.get()
        case_sensitive = self.case_var.get()
        try:
            resultado = probar_regex(patron, case_sensitive, cadena)
            if resultado:
                messagebox.showinfo("Prueba", "¡Coincide!")
            else:
                messagebox.showinfo("Prueba", "No coincide.")
        except Exception as e:
            messagebox.showerror("Regex inválida", str(e))

    def compilar_regex(self):
        patron = self.regex_var.get()
        case_sensitive = self.case_var.get()
        try:
            self.regex, self.flags = compilar_regex(patron, case_sensitive)
            self.regex_str = patron
            self.case_sensitive = case_sensitive
            self.show_results()
        except Exception as e:
            messagebox.showerror("Regex inválida", str(e))

    def show_results(self):
        self.clear()
        tk.Button(self, text="Validar", command=self.validar).pack(pady=5)
        self.filtro = tk.StringVar(value="Todos")
        filtro_frame = tk.Frame(self)
        filtro_frame.pack()
        for estado in ["Todos", "Válidos", "Inválidos"]:
            tk.Radiobutton(filtro_frame, text=estado, variable=self.filtro, value=estado, command=self.aplicar_filtro).pack(side="left")
        self.tree = ResultsTable(self)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.mostrar_detalle)
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Exportar", command=self.exportar_resultados).pack(side="right", padx=10)
        tk.Button(btn_frame, text="Atrás", command=self.show_regex_config).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Salir", command=self.quit).pack(side="left", padx=10)
        self.status = tk.Label(self, text="Total: 0 | Válidos: 0 | Inválidos: 0 | Tiempo: 0s", anchor="w")
        self.status.pack(fill="x")
        self.resultados = []

    def validar(self):
        import time
        start = time.time()
        resultados_raw = validar_lineas(self.lineas, self.regex, self.regex_str)
        self.resultados = resultados_raw
        self.aplicar_filtro()
        total = len(self.resultados)
        validos = sum(1 for r in self.resultados if r[2] == "Válido")
        invalidos = total - validos
        elapsed = round(time.time() - start, 2)
        self.status.config(text=f"Total: {total} | Válidos: {validos} | Inválidos: {invalidos} | Tiempo: {elapsed}s")

    def aplicar_filtro(self):
        self.tree.delete(*self.tree.get_children())
        estado = self.filtro.get()
        for r in self.resultados:
            if estado == "Todos":
                self.tree.insert("", "end", values=r)
            elif estado == "Válidos" and r[2] == "Válido":
                self.tree.insert("", "end", values=r)
            elif estado == "Inválidos" and r[2] == "Inválido":
                self.tree.insert("", "end", values=r)

    def exportar_resultados(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Text", "*.txt")])
        if not ruta:
            return
        error = exportar_resultados(ruta, self.resultados)
        if error:
            messagebox.showerror("Error", f"No se pudo exportar: {error}")
        else:
            messagebox.showinfo("Exportar", "Reporte exportado correctamente.")

    def mostrar_detalle(self, event):
        item = self.tree.focus()
        if not item:
            return
        vals = self.tree.item(item, "values")
        detalle = f"Línea: {vals[0]}\nCorreo: {vals[1]}\nEstado: {vals[2]}\nMotivo: {vals[3]}"
        dlg = tk.Toplevel(self)
        dlg.title("Detalle")
        tk.Label(dlg, text=detalle, justify="left").pack(padx=10, pady=10)
        tk.Button(dlg, text="Copiar", command=lambda: self.copiar_detalle(detalle)).pack(pady=5)
        tk.Button(dlg, text="Cerrar", command=dlg.destroy).pack(pady=5)

    def copiar_detalle(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Detalle copiado al portapapeles.")
    def cerrar(self):
        self.master.quit()
        self.master.destroy()

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from src.ui.components import LabeledEntry, LabeledCheck, LabeledButton, ResultsTable
from src.utils.file_handler import cargar_archivo_txt, exportar_resultados
from src.scripts.reg import compilar_regex, probar_regex, validar_lineas, analizar_motivo

# --- Datos resultado ---
class Resultado:
    def __init__(self, linea, correo, estado, motivo):
        self.linea = linea
        self.correo = correo
        self.estado = estado
        self.motivo = motivo
        


# --- Ventana 1: Abrir archivo ---
class WinAbrir(tk.Toplevel):
    def __init__(self, master, on_next):
        super().__init__(master)
        self.title("Abrir archivo")
        self.geometry("400x200")
        self.on_next = on_next
        self.file_path = tk.StringVar()
        self.lineas = []
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Selecciona un archivo .txt con correos (uno por línea):").pack(pady=10)
        tk.Button(self, text="Abrir .txt", command=self.cargar_archivo).pack()
        tk.Label(self, textvariable=self.file_path, fg="blue").pack(pady=5)
        self.btn_next = tk.Button(self, text="Siguiente", state="disabled", command=self.siguiente)
        self.btn_next.pack(side="right", padx=10, pady=10)
        tk.Button(self, text="Cancelar", command=self.cancelar).pack(side="right", padx=10, pady=10)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not ruta:
            return
        try:
            with open(ruta, encoding="utf-8") as f:
                lineas = [line.strip() for line in f.readlines()]
            if not any(lineas):
                messagebox.showwarning("Archivo vacío", "El archivo no contiene líneas útiles.")
                return
            self.file_path.set(ruta)
            self.lineas = lineas
            self.btn_next.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def siguiente(self):
        self.on_next(self.lineas)
        self.destroy()

    def cancelar(self):
        self.master.destroy()

# --- Ventana 2: Configurar Regex ---
class WinRegex(tk.Toplevel):
    def __init__(self, master, lineas, on_next, on_back):
        super().__init__(master)
        self.title("Configurar Regex")
        self.geometry("500x300")
        self.lineas = lineas
        self.on_next = on_next
        self.on_back = on_back
        self.regex_str = tk.StringVar(value=r"^[a-zA-Z]+[._-][a-zA-Z]+[0-9]{4}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        self.case_sensitive = tk.BooleanVar(value=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Expresión regular para validar correos:").pack(pady=5)
        tk.Entry(self, textvariable=self.regex_str, width=60).pack(pady=5)
        tk.Checkbutton(self, text="Sensible a mayúsculas/minúsculas", variable=self.case_sensitive).pack()
        tk.Button(self, text="Probar regex", command=self.probar_regex).pack(pady=5)
        tk.Label(self, text="Ejemplo válido: daniel.soto2025@dominio.com").pack()
        tk.Label(self, text="Ejemplo inválido: daniel..soto2025@dominio.com").pack()
        frame = tk.Frame(self)
        frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(frame, text="Atrás", command=self.atras).pack(side="left", padx=10)
        tk.Button(frame, text="Siguiente", command=self.siguiente).pack(side="right", padx=10)
        tk.Button(frame, text="Cancelar", command=self.cerrar).pack(side="right", padx=10)

    def cerrar(self):
        self.master.quit()
        self.master.destroy()

    def probar_regex(self):
        import re
        cadena = simpledialog.askstring("Probar regex", "Ingresa una cadena para probar:")
        if cadena is None:
            return
        try:
            flags = 0 if self.case_sensitive.get() else re.IGNORECASE
            patron = self.regex_str.get()
            regex = re.compile(patron, flags)
            if regex.fullmatch(cadena):
                messagebox.showinfo("Prueba", "¡Coincide!")
            else:
                messagebox.showinfo("Prueba", "No coincide.")
        except Exception as e:
            messagebox.showerror("Regex inválida", str(e))

    def siguiente(self):
        import re
        try:
            flags = 0 if self.case_sensitive.get() else re.IGNORECASE
            patron = self.regex_str.get()
            regex = re.compile(patron, flags)
            self.on_next(self.lineas, regex, patron, flags)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Regex inválida", str(e))

    def atras(self):
        geom = self.geometry()
        self.on_back(geom)
        self.destroy()

    def cancelar(self):
        self.master.destroy()

# --- Ventana 3: Resultados ---
class WinResultados(tk.Toplevel):
    def __init__(self, master, lineas, regex, patron, flags, on_back):
        super().__init__(master)
        self.title("Resultados")
        self.geometry("700x400")
        self.lineas = lineas
        self.regex = regex
        self.patron = patron
        self.flags = flags
        self.on_back = on_back
        self.resultados = []
        self.filtro = tk.StringVar(value="Todos")
        self.validado = False
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Validar", command=self.validar).pack(pady=5)
        filtro_frame = tk.Frame(self)
        filtro_frame.pack()
        for estado in ["Todos", "Válidos", "Inválidos"]:
            tk.Radiobutton(filtro_frame, text=estado, variable=self.filtro, value=estado, command=self.aplicar_filtro).pack(side="left")
        self.tree = ResultsTable(self)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.mostrar_detalle)
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Exportar", command=self.exportar_resultados).pack(side="right", padx=10)
        tk.Button(btn_frame, text="Atrás", command=self.atras).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cerrar", command=self.cerrar).pack(side="left", padx=10)
        self.status = tk.Label(self, text="Total: 0 | Válidos: 0 | Inválidos: 0 | Tiempo: 0s", anchor="w")
        self.status.pack(fill="x")

    def validar(self):
        import time
        from src.scripts.reg import compilar_regex, validar_lineas
        start = time.time()
        # Recompilar regex con el flag actual
        case_sensitive = self.flags == 0
        regex, _ = compilar_regex(self.patron, case_sensitive)
        resultados_raw = validar_lineas(self.lineas, regex, self.patron)
        self.resultados = [Resultado(*r) for r in resultados_raw]
        self.validado = True
        self.aplicar_filtro()
        total = len(self.resultados)
        validos = sum(1 for r in self.resultados if r.estado == "Válido")
        invalidos = total - validos
        elapsed = round(time.time() - start, 2)
        self.status.config(text=f"Total: {total} | Válidos: {validos} | Inválidos: {invalidos} | Tiempo: {elapsed}s")

    # validación y motivo ahora están en reg.py

    def aplicar_filtro(self):
        self.tree.delete(*self.tree.get_children())
        estado = self.filtro.get()
        for r in self.resultados:
            if estado == "Todos":
                self.tree.insert("", "end", values=(r.linea, r.correo, r.estado, r.motivo))
            elif estado == "Válidos" and r.estado == "Válido":
                self.tree.insert("", "end", values=(r.linea, r.correo, r.estado, r.motivo))
            elif estado == "Inválidos" and r.estado == "Inválido":
                self.tree.insert("", "end", values=(r.linea, r.correo, r.estado, r.motivo))

    def exportar_resultados(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Text", "*.txt")])
        if not ruta:
            return
        resultados_raw = [(r.linea, r.correo, r.estado, r.motivo) for r in self.resultados]
        error = exportar_resultados(ruta, resultados_raw)
        if error:
            messagebox.showerror("Error", f"No se pudo exportar: {error}")
        else:
            messagebox.showinfo("Exportar", "Reporte exportado correctamente.")

    def mostrar_detalle(self, event):
        item = self.tree.focus()
        if not item:
            return
        vals = self.tree.item(item, "values")
        detalle = f"Línea: {vals[0]}\nCorreo: {vals[1]}\nEstado: {vals[2]}\nMotivo: {vals[3]}"
        dlg = tk.Toplevel(self)
        dlg.title("Detalle")
        tk.Label(dlg, text=detalle, justify="left").pack(padx=10, pady=10)
        tk.Button(dlg, text="Copiar", command=lambda: self.copiar_detalle(detalle)).pack(pady=5)
        tk.Button(dlg, text="Cerrar", command=dlg.destroy).pack(pady=5)

    def copiar_detalle(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Detalle copiado al portapapeles.")

    def atras(self):
        geom = self.geometry()
        self.on_back(geom)
        self.destroy()
