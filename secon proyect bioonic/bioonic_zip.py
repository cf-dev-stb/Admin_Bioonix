import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import zipfile
import os
import json
import time
import threading
from datetime import datetime, timedelta

# --- Rutas de archivos ---
HISTORIAL_PATH = "historial_respaldo.json"
CREDENCIALES_PATH = "credenciales.json"
PROGRAMADOS_PATH = "respaldos_programados.json"

# --- Colores tecnológicos ---
COLOR_BG = "#1a2238"        # Azul marino oscuro
COLOR_PANEL = "#283655"     # Azul marino medio
COLOR_BTN = "#21a1ff"       # Azul claro
COLOR_BTN_TXT = "#ffffff"   # Blanco
COLOR_ENTRY = "#eaeaea"     # Gris claro
COLOR_LIST = "#f5f6fa"      # Fondo Listbox
COLOR_LIST_TXT = "#222831"  # Texto Listbox

# --- Manejo de credenciales y roles ---
def cargar_credenciales():
    # Si no existe, crea el admin por defecto
    if not os.path.exists(CREDENCIALES_PATH):
        cred = {"admin": {"contrasena": "admin123", "rol": "admin"}}
        with open(CREDENCIALES_PATH, "w") as f:
            json.dump(cred, f)
        return cred
    with open(CREDENCIALES_PATH, "r") as f:
        return json.load(f)

def guardar_credenciales(usuario, contrasena, rol="usuario"):
    cred = cargar_credenciales()
    cred[usuario] = {"contrasena": contrasena, "rol": rol}
    with open(CREDENCIALES_PATH, "w") as f:
        json.dump(cred, f)

def eliminar_usuario(usuario):
    cred = cargar_credenciales()
    if usuario in cred and usuario != "admin":
        del cred[usuario]
        with open(CREDENCIALES_PATH, "w") as f:
            json.dump(cred, f)
        return True
    return False

def obtener_rol(usuario):
    cred = cargar_credenciales()
    if usuario in cred:
        return cred[usuario].get("rol", "usuario")
    return "usuario"

# --- Historial ---
def agregar_a_historial(usuario, archivos, destino):
    historial = []
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            historial = json.load(f)
    historial.append({
        "usuario": usuario,
        "archivos": archivos,
        "destino": destino,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f, indent=4)

def cargar_historial():
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            return json.load(f)
    return []

# --- Programados ---
def cargar_programados():
    if os.path.exists(PROGRAMADOS_PATH):
        with open(PROGRAMADOS_PATH, "r") as f:
            return json.load(f)
    return []

def guardar_programados(lista):
    with open(PROGRAMADOS_PATH, "w") as f:
        json.dump(lista, f, indent=4)

def agregar_programado(hora, archivos, destino):
    lista = cargar_programados()
    lista.append({"hora": hora, "archivos": archivos, "destino": destino})
    guardar_programados(lista)

def eliminar_programado(idx):
    lista = cargar_programados()
    if 0 <= idx < len(lista):
        lista.pop(idx)
        guardar_programados(lista)

def editar_programado(idx, hora, archivos, destino):
    lista = cargar_programados()
    if 0 <= idx < len(lista):
        lista[idx] = {"hora": hora, "archivos": archivos, "destino": destino}
        guardar_programados(lista)

# --- Respaldo ZIP ---
def crear_respaldo_zip(archivos_a_resguardar, destino):
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for archivo in archivos_a_resguardar:
            if os.path.isfile(archivo):
                zipf.write(archivo, os.path.basename(archivo))
            elif os.path.isdir(archivo):
                for carpeta_raiz, _, archivos in os.walk(archivo):
                    for a in archivos:
                        ruta_completa = os.path.join(carpeta_raiz, a)
                        arcname = os.path.relpath(ruta_completa, os.path.dirname(archivo))
                        zipf.write(ruta_completa, arcname)
    return destino

# --- Hilo para respaldos programados ---
def hilo_programados(usuario):
    def tarea():
        while True:
            lista = cargar_programados()
            ahora = datetime.now()
            for p in lista:
                try:
                    hora, minuto = map(int, p["hora"].split(":"))
                except:
                    continue
                proximo = ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
                if proximo <= ahora:
                    proximo += timedelta(days=1)
                espera = (proximo - ahora).total_seconds()
                if espera < 60:
                    if all([os.path.exists(a) for a in p["archivos"]]):
                        crear_respaldo_zip(p["archivos"], p["destino"])
                        agregar_a_historial(usuario, p["archivos"], p["destino"])
                        time.sleep(60)
            time.sleep(30)
    threading.Thread(target=tarea, daemon=True).start()

# --- Interfaz gráfica ---

class App:
    def __init__(self, root):
        self.root = root
        self.usuario = None
        self.credenciales = cargar_credenciales()
        self.root.title("Bioonic Backup")
        self.root.geometry("900x600")  # Más grande para mejor distribución
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        self.mostrar_login()

    def mostrar_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # Panel más ancho y alto
        panel = tk.Frame(self.root, bg=COLOR_PANEL, bd=2, relief="groove")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=520, height=400)

        tk.Label(panel, text="Iniciar Sesión", bg=COLOR_PANEL, fg=COLOR_BTN, font=("Segoe UI", 26, "bold")).pack(pady=(38, 18))
        tk.Label(panel, text="Usuario:", bg=COLOR_PANEL, fg=COLOR_BTN_TXT, font=("Segoe UI", 13)).pack(pady=(12, 0))
        self.entry_usuario = tk.Entry(panel, font=("Segoe UI", 12), bg=COLOR_ENTRY, relief="flat", width=22)
        self.entry_usuario.pack(pady=7, ipadx=4, ipady=2)
        tk.Label(panel, text="Contraseña:", bg=COLOR_PANEL, fg=COLOR_BTN_TXT, font=("Segoe UI", 13)).pack(pady=(12, 0))
        self.entry_contrasena = tk.Entry(panel, show="*", font=("Segoe UI", 12), bg=COLOR_ENTRY, relief="flat", width=22)
        self.entry_contrasena.pack(pady=7, ipadx=4, ipady=2)

        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=38)
        btn_login = tk.Button(
            btn_frame, text="Entrar", command=self.login,
            bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 16, "bold"),
            width=14, height=2, relief="flat"
        )
        btn_login.pack(side="left", padx=24)
        btn_reg = tk.Button(
            btn_frame, text="Registrarse", command=self.registrarse,
            bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 16, "bold"),
            width=14, height=2, relief="flat"
        )
        btn_reg.pack(side="left", padx=24)

    def login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        cred = cargar_credenciales()
        if usuario in cred and cred[usuario]["contrasena"] == contrasena:
            self.usuario = usuario
            self.rol = cred[usuario].get("rol", "usuario")
            self.mostrar_principal()
            hilo_programados(self.usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrarse(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        cred = cargar_credenciales()
        if not usuario or not contrasena:
            messagebox.showerror("Error", "Debes ingresar usuario y contraseña.")
            return
        if usuario in cred:
            messagebox.showerror("Error", "El usuario ya existe.")
            return
        guardar_credenciales(usuario, contrasena, rol="usuario")
        messagebox.showinfo("Registrado", "Usuario registrado correctamente. Ahora puedes iniciar sesión.")

    def mostrar_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame superior para título y botón admin
        top_frame = tk.Frame(self.root, bg=COLOR_BG)
        top_frame.pack(fill="x", pady=(15, 0), padx=30)

        # Bienvenido a la izquierda
        lbl_bienvenido = tk.Label(
            top_frame, text=f"Bienvenido, {self.usuario}",
            bg=COLOR_BG, fg=COLOR_BTN, font=("Segoe UI", 22, "bold"), anchor="w"
        )
        lbl_bienvenido.pack(side="left", padx=(0, 10))

        # Si es admin, botón a la derecha
        if obtener_rol(self.usuario) == "admin":
            btn_admin = tk.Button(
                top_frame, text="Gestionar Usuarios", command=self.gestionar_usuarios,
                bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 12, "bold"),
                width=18, relief="flat", cursor="hand2"
            )
            btn_admin.pack(side="right", padx=(10, 0))

        # Panel principal
        panel = tk.Frame(self.root, bg=COLOR_PANEL, bd=2, relief="groove")
        panel.pack(padx=40, pady=10, fill="both", expand=True)

        # Botones principales, bien espaciados y centrados
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=(18, 15))
        btn_guardar = tk.Button(btn_frame, text="Guardar ZIP", command=self.descargar_respaldo, bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 13, "bold"), width=16, relief="flat")
        btn_guardar.pack(side="left", padx=18)
        btn_programar = tk.Button(btn_frame, text="Agregar Programado", command=self.agregar_programado_dialogo, bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 13, "bold"), width=19, relief="flat")
        btn_programar.pack(side="left", padx=18)
        btn_logout = tk.Button(btn_frame, text="Cerrar Sesión", command=self.mostrar_login, bg=COLOR_BG, fg=COLOR_BTN, font=("Segoe UI", 13, "bold"), width=16, relief="flat")
        btn_logout.pack(side="left", padx=18)

        # Listbox para historial y programados
        self.listbox = tk.Listbox(panel, font=("Segoe UI", 12), bg=COLOR_LIST, fg=COLOR_LIST_TXT, selectbackground=COLOR_BTN, selectforeground=COLOR_BTN_TXT, activestyle="none")
        self.listbox.pack(fill="both", expand=True, padx=30, pady=(15, 8))
        self.actualizar_listbox()

        # Botones debajo del listbox
        btns_hist = tk.Frame(panel, bg=COLOR_PANEL)
        btns_hist.pack(pady=(8, 18))
        btn_editar = tk.Button(btns_hist, text="Editar Programado", command=self.editar_programado_dialogo, bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 11, "bold"), width=18, relief="flat")
        btn_editar.pack(side="left", padx=14)
        btn_eliminar = tk.Button(btns_hist, text="Eliminar Programado", command=self.eliminar_programado_dialogo, bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 11, "bold"), width=18, relief="flat")
        btn_eliminar.pack(side="left", padx=14)
        btn_volver = tk.Button(btns_hist, text="Actualizar Lista", command=self.actualizar_listbox, bg=COLOR_PANEL, fg=COLOR_BTN, font=("Segoe UI", 11, "bold"), width=18, relief="flat")
        btn_volver.pack(side="left", padx=14)

    def actualizar_listbox(self):
        self.listbox.delete(0, tk.END)
        historial = cargar_historial()
        programados = cargar_programados()
        self.listbox.insert(tk.END, "=== HISTORIAL DE RESPALDOS ===")
        for h in historial[::-1]:
            self.listbox.insert(tk.END, f"{h['fecha']} | {os.path.basename(h['destino'])} | Archivos: {', '.join([os.path.basename(a) for a in h['archivos']])}")
        self.listbox.insert(tk.END, "")
        self.listbox.insert(tk.END, "=== RESPALDOS PROGRAMADOS ===")
        for i, p in enumerate(programados):
            self.listbox.insert(tk.END, f"{p['hora']} | {os.path.basename(p['destino'])} | Archivos: {', '.join([os.path.basename(a) for a in p['archivos']])}")

    def descargar_respaldo(self):
        tipo = simpledialog.askstring("Tipo", "¿Qué deseas respaldar? (Archivos/Carpeta)").strip().lower()
        archivos_a_resguardar = []
        if tipo == "archivos":
            archivos_a_resguardar = filedialog.askopenfilenames(title="Selecciona uno o varios archivos a respaldar")
        elif tipo == "carpeta":
            carpeta = filedialog.askdirectory(title="Selecciona la carpeta a respaldar")
            if carpeta:
                archivos_a_resguardar = [carpeta]
        else:
            messagebox.showerror("Error", "Debes escribir 'Archivos' o 'Carpeta'.")
            return
        if not archivos_a_resguardar:
            messagebox.showerror("Error", "No seleccionaste ningún archivo o carpeta.")
            return
        destino = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")])
        if destino:
            crear_respaldo_zip(archivos_a_resguardar, destino)
            agregar_a_historial(self.usuario, archivos_a_resguardar, destino)
            messagebox.showinfo("Éxito", f"Respaldo guardado en:\n{destino}")
            self.actualizar_listbox()

    def agregar_programado_dialogo(self):
        hora = simpledialog.askstring("Hora de respaldo", "¿A qué hora diaria? (formato 24h, ej: 15:30)")
        if not hora:
            return
        archivos = filedialog.askopenfilenames(title="Selecciona archivos/carpeta para respaldo programado")
        if not archivos:
            return
        destino = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")])
        if not destino:
            return
        agregar_programado(hora, list(archivos), destino)
        messagebox.showinfo("Agregado", "Respaldo programado agregado.")
        self.actualizar_listbox()

    def editar_programado_dialogo(self):
        idx = self.listbox.curselection()
        programados = cargar_programados()
        if not idx or idx[0] < self.listbox.get(0, tk.END).index("=== RESPALDOS PROGRAMADOS ===") + 1:
            messagebox.showerror("Error", "Selecciona un respaldo programado para editar.")
            return
        idx_prog = idx[0] - self.listbox.get(0, tk.END).index("=== RESPALDOS PROGRAMADOS ===") - 1
        if not (0 <= idx_prog < len(programados)):
            messagebox.showerror("Error", "Índice inválido.")
            return
        p = programados[idx_prog]
        hora = simpledialog.askstring("Editar hora", "Hora diaria (HH:MM)", initialvalue=p["hora"])
        if not hora:
            return
        archivos = filedialog.askopenfilenames(title="Selecciona archivos/carpeta para respaldo programado")
        if not archivos:
            archivos = p["archivos"]
        destino = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")], initialfile=os.path.basename(p["destino"]))
        if not destino:
            destino = p["destino"]
        editar_programado(idx_prog, hora, list(archivos), destino)
        messagebox.showinfo("Editado", "Respaldo programado editado.")
        self.actualizar_listbox()

    def eliminar_programado_dialogo(self):
        idx = self.listbox.curselection()
        programados = cargar_programados()
        if not idx or idx[0] < self.listbox.get(0, tk.END).index("=== RESPALDOS PROGRAMADOS ===") + 1:
            messagebox.showerror("Error", "Selecciona un respaldo programado para eliminar.")
            return
        idx_prog = idx[0] - self.listbox.get(0, tk.END).index("=== RESPALDOS PROGRAMADOS ===") - 1
        if not (0 <= idx_prog < len(programados)):
            messagebox.showerror("Error", "Índice inválido.")
            return
        eliminar_programado(idx_prog)
        messagebox.showinfo("Eliminado", "Respaldo programado eliminado.")
        self.actualizar_listbox()

    def gestionar_usuarios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de usuarios")
        ventana.configure(bg=COLOR_PANEL)
        ventana.geometry("400x350")
        lista = cargar_credenciales()
        usuarios = [u for u in lista if u != "admin"]
        lb = tk.Listbox(ventana, font=("Segoe UI", 11), bg=COLOR_LIST, fg=COLOR_LIST_TXT)
        lb.pack(fill="both", expand=True, padx=20, pady=20)
        for u in usuarios:
            lb.insert(tk.END, u)
        def eliminar():
            idx = lb.curselection()
            if not idx:
                messagebox.showerror("Error", "Selecciona un usuario para eliminar.")
                return
            usuario = lb.get(idx[0])
            if eliminar_usuario(usuario):
                messagebox.showinfo("Eliminado", f"Usuario '{usuario}' eliminado.")
                lb.delete(idx[0])
            else:
                messagebox.showerror("Error", "No se puede eliminar este usuario.")
        btn_eliminar = tk.Button(ventana, text="Eliminar usuario", command=eliminar, bg=COLOR_BTN, fg=COLOR_BTN_TXT, font=("Segoe UI", 11, "bold"))
        btn_eliminar.pack(pady=10)

# --- Lanzar la app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()