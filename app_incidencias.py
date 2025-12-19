import tkinter as tk
from tkinter import ttk, messagebox

INCIDENCIAS = {
    "Sin Internet / Wi-Fi": [
        "Verifica que el Modo Avión esté desactivado.",
        "Apaga/enciende el Wi-Fi (o desconecta y vuelve a conectar la red).",
        "Reinicia el router si aplica (o prueba con hotspot del móvil).",
        "Ejecuta el solucionador de red de Windows (Configuración > Red e Internet).",
        "Reinicia la laptop; si persiste, olvida la red y vuelve a introducir la clave."
    ],
    "Laptop lenta": [
        "Reinicia para liberar memoria y aplicar actualizaciones pendientes.",
        "Revisa el Administrador de tareas: CPU/RAM/Disco al 100% y cierra lo innecesario.",
        "Desactiva programas de inicio (Administrador de tareas > Inicio).",
        "Libera espacio: borra temporales y deja ~15–20% de disco libre.",
        "Pasa un escaneo antivirus/antimalware y actualiza Windows."
    ],
    "No enciende / Pantalla negra": [
        "Conecta el cargador y prueba otro enchufe/cargador si tienes.",
        "Mantén presionado Power 10–15s (apagado forzado) y vuelve a encender.",
        "Desconecta periféricos (USB, docking) e intenta encender de nuevo.",
        "Si tiene batería removible: retírala, mantén Power 15s, vuelve a colocarla.",
        "Prueba salida HDMI a monitor externo para descartar fallo de pantalla."
    ],
    "Audio no funciona": [
        "Verifica el volumen y que no esté en silencio (y la salida correcta).",
        "Desconecta/reconecta auriculares o Bluetooth si estaba activo.",
        "Reinicia el servicio o el PC (muchos casos se arreglan así).",
        "Ejecuta solucionador de audio de Windows (Configuración > Sistema > Sonido).",
        "Reinstala/actualiza driver de audio (Administrador de dispositivos)."
    ],
    "Batería dura poco / no carga": [
        "Comprueba si el cargador y el puerto están firmes (sin holgura).",
        "Revisa ‘Uso de batería’ y reduce brillo / cierra apps en segundo plano.",
        "Cambia el plan de energía a equilibrado/ahorro cuando no esté enchufada.",
        "Actualiza drivers (chipset/energía) y BIOS si el fabricante lo recomienda.",
        "Si el estado de batería está degradado (salud baja), considerar reemplazo."
    ],
}

def mostrar_incidencia(nombre):
    pasos = INCIDENCIAS[nombre]
    texto = f"{nombre}\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(pasos)])
    output.delete("1.0", tk.END)
    output.insert(tk.END, texto)

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
root.geometry("680x420")

frm = ttk.Frame(root, padding=10)
frm.pack(fill="both", expand=True)

ttk.Label(frm, text="Selecciona una incidencia:").pack(anchor="w")

btns = ttk.Frame(frm)
btns.pack(fill="x", pady=8)

for nombre in INCIDENCIAS.keys():
    ttk.Button(btns, text=nombre, command=lambda n=nombre: mostrar_incidencia(n)).pack(side="left", padx=4)

output = tk.Text(frm, wrap="word", height=14)
output.pack(fill="both", expand=True, pady=8)

ttk.Button(frm, text="Copiar recomendaciones", command=copiar).pack(anchor="e")

root.mainloop()
