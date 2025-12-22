import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk # Importamos Pillow

# Estructura de datos sin cambios
INCIDENCIAS = {
    "📶 Sin Internet / Wi-Fi en tu laptop": {
        "pasos": [
            "Verifica que el Modo Avión esté desactivado.",
            "Apaga/enciende el Wi-Fi (o desconecta y vuelve a conectar el cable de red).",
            "Reinicia el router ( en caso este en su casa).",
            #"Ejecuta el solucionador de red de Windows (Configuración > Red e Internet).",
            "Reinicia la laptop."
        ],
        "imagen": "modo_avion.webp"
    },
    # "🐢 Laptop lenta": {
    #     "pasos": [
    #         "Reinicia para liberar memoria y aplicar actualizaciones pendientes.",
    #         "Revisa el Administrador de tareas: CPU/RAM/Disco al 100% y cierra lo innecesario.",
    #         "Desactiva programas de inicio (Administrador de tareas > Inicio).",
    #         "Libera espacio: borra temporales y deja ~15–20% de disco libre.",
    #         "Pasa un escaneo antivirus/antimalware y actualiza Windows."
    #     ],
    #     "imagen": "lenta_ayuda.png"
    # },
    "⚫ No enciende / Pantalla negra": {
        "tipo": "subopcion",
        "opciones": {
            "💻 Laptop": {
                "pasos": [
                    "Conecta el cargador y verifica si enciende el LED de carga.",
                    "Mantén presionado Power 15s (reseteo eléctrico) sin batería (si es extraíble).",
                    "Prueba encender solo con cargador (sin batería) si es posible.",
                    # "Conecta a un monitor externo por HDMI para descartar fallo de pantalla.",
                    "Si enciende LED pero no da video, puede ser fallo de RAM o pantalla."
                ],
                "imagen": "noenciende_pantalla.jpg"
            },
            "🖥️ PC Escritorio": {
                "pasos": [
                    "Verifica que el cable de poder esté firme en la fuente y el enchufe.",
                    "Revisa el interruptor trasero de la fuente de poder (I/O).",
                    "Asegúrate de que el monitor esté encendido y el cable de HDMI o VGA este bien conectado.",
                    #"Si escuchas ventiladores pero no hay video, limpia/reconecta la RAM.",
                    #"Desconecta periféricos USB innecesarios e intenta arrancar."
                ],
                "imagen": "noenciende_pantalla.jpg"
            }
        }
    },
    "🔊 Audio no funciona": {
        "pasos": [
            "Verifica el volumen y que no esté en silencio.",
            "Desconecta/reconecta el USB del casco.",
            "Cambia de puerto USB del casco",
            "Reinicia la laptop o la PC ."
            #"Ejecuta solucionador de audio de Windows (Configuración > Sistema > Sonido).",
            #"Reinstala/actualiza driver de audio (Administrador de dispositivos)."
        ],
        "imagen": "audio_nofunciona.jpg"
    },
    "🔋 Batería dura poco / no carga": {
        "pasos": [
            "Comprueba si el cargador y el puerto están firmes (sin holgura).",
            "Prueba otro cargador si tuvieras a la mano.",
            "Prueba otro tomacorriente."
            #"Revisa ‘Uso de batería’ y reduce brillo / cierra apps en segundo plano.",
            #"Cambia el plan de energía a equilibrado/ahorro cuando no esté enchufada.",
            #"Actualiza drivers (chipset/energía) y BIOS si el fabricante lo recomienda.",
            #"Si el estado de batería está degradado (salud baja), considerar reemplazo."
        ],
        "imagen": "no_carganbateria.png"
    },
    "🖥️ Falla Escritorio Remoto": {
        "pasos": [
            "Comprueba si esta conectado a internet.",
            "Valide su contraseña o solicite el cambio de contraseña.",
            "Valide que solo sea el ùnico usuario suscrito."
        ],
        "imagen": "falla_remoto.jpg"
    },
}

current_incidencia_data = None
current_titulo = ""

def mostrar_pasos(titulo, datos):
    global current_incidencia_data, current_titulo
    current_incidencia_data = datos
    current_titulo = titulo
    
    pasos = datos["pasos"]
    texto = f"{titulo}\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(pasos)])
    
    output.delete("1.0", tk.END)
    output.insert(tk.END, texto)
    
    # Limpiar frame de subopciones y añadir botón "Atrás" si es una subopción
    for widget in subopciones_frm.winfo_children():
        widget.destroy()
        
    if " - " in titulo: # Detecta si es una subopción por el título
        parent_titulo = titulo.split(" - ")[0]
        btn_atras = ttk.Button(subopciones_frm, text="⬅️ Atrás", command=lambda: mostrar_incidencia(parent_titulo))
        btn_atras.pack(side="left", padx=10, pady=5)

    btn_imagen.config(state="normal")

def mostrar_incidencia(nombre):
    global current_incidencia_data
    
    output.delete("1.0", tk.END)
    btn_imagen.config(state="disabled")
    
    for widget in subopciones_frm.winfo_children():
        widget.destroy()

    data = INCIDENCIAS[nombre]
    
    if data.get("tipo") == "subopcion":
        ttk.Label(subopciones_frm, text=f"¿Qué tipo de equipo es? ({nombre})", font=("Segoe UI", 9, "bold")).pack(pady=5)
        
        for sub_nombre, sub_data in data["opciones"].items():
            ttk.Button(subopciones_frm, text=sub_nombre, 
                       command=lambda t=sub_nombre, d=sub_data: mostrar_pasos(f"{nombre} - {t}", d)).pack(side="left", padx=10, pady=5)
            
        output.insert(tk.END, "Selecciona una opción arriba para ver los pasos...")
    else:
        mostrar_pasos(nombre, data)

def ver_imagen():
    if not current_incidencia_data:
        return

    nombre_archivo = current_incidencia_data.get("imagen", "")
    if not nombre_archivo:
        messagebox.showinfo("Información", "Esta incidencia no tiene imagen asociada.")
        return

    ruta_imagen = os.path.join("imagenes", nombre_archivo)
    
    if not os.path.exists(ruta_imagen):
        messagebox.showwarning("Imagen no encontrada", f"No se encontró el archivo: {nombre_archivo}")
        return

    try:
        ventana_img = tk.Toplevel(root)
        ventana_img.title(f"Ayuda visual: {current_titulo}")
        
        # Usamos Pillow para abrir y redimensionar
        image_file = Image.open(ruta_imagen)
        
        # Redimensionar si es muy grande (Max 800x600)
        max_size = (800, 600)
        image_file.thumbnail(max_size, Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(image_file)
        
        lbl_img = tk.Label(ventana_img, image=img)
        lbl_img.image = img 
        lbl_img.pack(padx=10, pady=10)
        
        ttk.Button(ventana_img, text="Cerrar", command=ventana_img.destroy).pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Error al abrir imagen", f"No se pudo abrir la imagen '{nombre_archivo}'.\n\nAsegúrate de tener la librería 'Pillow' instalada (pip install Pillow).\n\nDetalle: {e}")

def copiar():
    contenido = output.get("1.0", tk.END).strip()
    if not contenido:
        messagebox.showinfo("Copiar", "No hay texto para copiar.")
        return
    root.clipboard_clear()
    root.clipboard_append(contenido)
    messagebox.showinfo("Copiar", "Texto copiado al portapapeles.")

root = tk.Tk()
root.title("Incidencias comunes - Soporte")
root.geometry("850x550")

frm = ttk.Frame(root, padding=10)
frm.pack(fill="both", expand=True)

ttk.Label(frm, text="Selecciona una incidencia:").pack(anchor="w")

btns = ttk.Frame(frm)
btns.pack(fill="x", pady=8)

for nombre in INCIDENCIAS.keys():
    ttk.Button(btns, text=nombre, command=lambda n=nombre: mostrar_incidencia(n)).pack(side="left", padx=2, fill="x", expand=True)

subopciones_frm = ttk.Frame(frm)
subopciones_frm.pack(fill="x", pady=5)

output = tk.Text(frm, wrap="word", height=14, font=("Segoe UI", 10))
output.pack(fill="both", expand=True, pady=8)

bottom_frm = ttk.Frame(frm)
bottom_frm.pack(fill="x", pady=5)

btn_imagen = ttk.Button(bottom_frm, text="📷 Ver imagen de ayuda", command=ver_imagen, state="disabled")
btn_imagen.pack(side="left")

ttk.Button(bottom_frm, text="Copiar recomendaciones", command=copiar).pack(side="right")

root.mainloop()
