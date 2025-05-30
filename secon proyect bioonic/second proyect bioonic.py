import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import zipfile
import os
import json
import time
import threading
from datetime import datetime, timedelta

HISTORIAL_PATH = "historial_respaldo.json"
CREDENCIALES_PATH = "credenciales.json"
PROGRAMADOS_PATH = "respaldos_programados.json"

# --- Manejo de credenciales ---
def cargar_credenciales():
    if os.path.exists(CREDENCIALES_PATH):
        with open(CREDENCIALES_PATH, "r") as f:
            return json.load(f)
    else:
        return {"usuario": "admin", "contrasena": "1234"}

def guardar_credenciales(usuario, contrasena):
    with open(CREDENCIALES_PATH, "w") as f:
        json.dump({"usuario": usuario, "contrasena": contrasena}, f)

credenciales = cargar_credenciales()

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

def mostrar_historial():
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            historial = json.load(f)
        texto = ""
        for h in historial[-10:][::-1]:
            texto += f"{h['fecha']} - {h['usuario']} - {os.path.basename(h['destino'])}\n"
            for a in h['archivos']:
                texto += f"   {os.path.basename(a)}\n"
        messagebox.showinfo("Historial de respaldos", texto)
    else:
        messagebox.showinfo("Historial de respaldos", "No hay respaldos registrados.")

# --- Respaldo ---
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

def descargar_respaldo():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario == credenciales["usuario"] and contrasena == credenciales["contrasena"]:
        tipo = combo_tipo.get()
        archivos_a_resguardar = []
        if tipo == "Archivos":
            archivos_a_resguardar = filedialog.askopenfilenames(title="Selecciona uno o varios archivos a respaldar")
        elif tipo == "Carpeta":
            carpeta = filedialog.askdirectory(title="Selecciona la carpeta a respaldar")
            if carpeta:
                archivos_a_resguardar = [carpeta]
        if not archivos_a_resguardar:
            messagebox.showerror("Error", "No seleccionaste ningún archivo o carpeta.")
            return
        destino = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")])
        if destino:
            crear_respaldo_zip(archivos_a_resguardar, destino)
            agregar_a_historial(usuario, archivos_a_resguardar, destino)
            messagebox.showinfo("Éxito", f"Respaldo guardado en:\n{destino}")
    else:
        messagebox.showerror("Acceso denegado", "Credenciales incorrectas.")

def cambiar_credenciales():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario == credenciales["usuario"] and contrasena == credenciales["contrasena"]:
        nuevo_usuario = simpledialog.askstring("Nuevo usuario", "Introduce el nuevo usuario:")
        if not nuevo_usuario:
            return
        nueva_contrasena = simpledialog.askstring("Nueva contraseña", "Introduce la nueva contraseña:", show="*")
        if not nueva_contrasena:
            return
        guardar_credenciales(nuevo_usuario, nueva_contrasena)
        messagebox.showinfo("Listo", "Usuario y contraseña cambiados.\nReinicia la aplicación para aplicar cambios.")
    else:
        messagebox.showerror("Acceso denegado", "Credenciales incorrectas.")

# --- Respaldo programado ---
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

def mostrar_programados():
    lista = cargar_programados()
    if not lista:
        messagebox.showinfo("Respaldos programados", "No hay respaldos programados.")
        return
    ventana_prog = tk.Toplevel(ventana)
    ventana_prog.title("Respaldos programados")
    ventana_prog.configure(bg="#232946")
    ventana_prog.geometry("500x350")
    tree = ttk.Treeview(ventana_prog, columns=("Hora", "Destino", "Archivos"), show="headings")
    tree.heading("Hora", text="Hora")
    tree.heading("Destino", text="Destino ZIP")
    tree.heading("Archivos", text="Archivos/Carpeta")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    for i, p in enumerate(lista):
        tree.insert("", "end", iid=i, values=(p["hora"], os.path.basename(p["destino"]), "; ".join([os.path.basename(a) for a in p["archivos"]])))
    def editar():
        sel = tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        editar_programado_dialogo(idx)
        ventana_prog.destroy()
    def eliminar():
        sel = tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        eliminar_programado(idx)
        ventana_prog.destroy()
        messagebox.showinfo("Eliminado", "Respaldo programado eliminado.")
    btn_editar = tk.Button(ventana_prog, text="Editar", command=editar, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10, "bold"))
    btn_editar.pack(side="left", padx=20, pady=10)
    btn_eliminar = tk.Button(ventana_prog, text="Eliminar", command=eliminar, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10, "bold"))
    btn_eliminar.pack(side="right", padx=20, pady=10)

def editar_programado_dialogo(idx):
    lista = cargar_programados()
    if not (0 <= idx < len(lista)):
        return
    p = lista[idx]
    hora = simpledialog.askstring("Editar hora", "Hora diaria (HH:MM)", initialvalue=p["hora"])
    if not hora:
        return
    archivos = filedialog.askopenfilenames(title="Selecciona archivos/carpeta para respaldo programado")
    if not archivos:
        archivos = p["archivos"]
    destino = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")], initialfile=os.path.basename(p["destino"]))
    if not destino:
        destino = p["destino"]
    editar_programado(idx, hora, list(archivos), destino)
    messagebox.showinfo("Editado", "Respaldo programado editado.")

def agregar_programado_dialogo():
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

def hilo_programados():
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
                if espera < 60:  # Si falta menos de 1 minuto, ejecuta respaldo
                    if all([os.path.exists(a) for a in p["archivos"]]):
                        crear_respaldo_zip(p["archivos"], p["destino"])
                        agregar_a_historial(credenciales["usuario"], p["archivos"], p["destino"])
                        time.sleep(60)  # Espera un minuto para evitar dobles respaldos
            time.sleep(30)
    threading.Thread(target=tarea, daemon=True).start()

# --- Interfaz gráfica elegante ---
ventana = tk.Tk()
ventana.title("Respaldo seguro de archivos y carpetas")
ventana.configure(bg="#232946")
ventana.geometry("470x480")
ventana.resizable(False, False)

titulo = tk.Label(
    ventana, text="Respaldo Corporativo", 
    bg="#232946", fg="#eebbc3", font=("Segoe UI", 18, "bold")
)
titulo.pack(pady=(25, 10))

frame = tk.Frame(ventana, bg="#393d5c", bd=2, relief="groove")
frame.pack(padx=30, pady=10, fill="both", expand=True)

tk.Label(frame, text="Usuario:", bg="#393d5c", fg="#eebbc3", font=("Segoe UI", 11)).grid(row=0, column=0, padx=10, pady=12, sticky="e")
entry_usuario = tk.Entry(frame, font=("Segoe UI", 11), bg="#f4f4f6", relief="flat")
entry_usuario.grid(row=0, column=1, padx=10, pady=12)

tk.Label(frame, text="Contraseña:", bg="#393d5c", fg="#eebbc3", font=("Segoe UI", 11)).grid(row=1, column=0, padx=10, pady=12, sticky="e")
entry_contrasena = tk.Entry(frame, show="*", font=("Segoe UI", 11), bg="#f4f4f6", relief="flat")
entry_contrasena.grid(row=1, column=1, padx=10, pady=12)

tk.Label(frame, text="Tipo de respaldo:", bg="#393d5c", fg="#eebbc3", font=("Segoe UI", 11)).grid(row=2, column=0, padx=10, pady=12, sticky="e")
combo_tipo = ttk.Combobox(frame, values=["Archivos", "Carpeta"], state="readonly", font=("Segoe UI", 11))
combo_tipo.set("Archivos")
combo_tipo.grid(row=2, column=1, padx=10, pady=12)

estilo_btn = {"font": ("Segoe UI", 11, "bold"), "bd": 0, "relief": "flat", "activebackground": "#eebbc3", "activeforeground": "#232946"}

btn_descargar = tk.Button(frame, text="Descargar respaldo ZIP", command=descargar_respaldo, bg="#eebbc3", fg="#232946", **estilo_btn)
btn_descargar.grid(row=3, column=0, columnspan=2, pady=(18, 8), sticky="we")

btn_historial = tk.Button(frame, text="Ver historial", command=mostrar_historial, bg="#393d5c", fg="#eebbc3", highlightbackground="#eebbc3", **estilo_btn)
btn_historial.grid(row=4, column=0, columnspan=2, pady=5, sticky="we")

btn_cambiar = tk.Button(frame, text="Cambiar usuario/contraseña", command=cambiar_credenciales, bg="#232946", fg="#eebbc3", highlightbackground="#eebbc3", **estilo_btn)
btn_cambiar.grid(row=5, column=0, columnspan=2, pady=(5, 5), sticky="we")

btn_ver_programados = tk.Button(frame, text="Ver/Editar respaldos programados", command=mostrar_programados, bg="#eebbc3", fg="#232946", **estilo_btn)
btn_ver_programados.grid(row=6, column=0, columnspan=2, pady=(5, 5), sticky="we")

btn_agregar_programado = tk.Button(frame, text="Agregar respaldo programado", command=agregar_programado_dialogo, bg="#393d5c", fg="#eebbc3", **estilo_btn)
btn_agregar_programado.grid(row=7, column=0, columnspan=2, pady=(5, 18), sticky="we")

frame.grid_columnconfigure(1, weight=1)

# Inicia el hilo de respaldos programados
hilo_programados()

ventana.mainloop()