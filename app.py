#HADES0413

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from PIL import Image, ImageTk
import os
import subprocess
import re
import moviepy.editor as mp
#

# Variable global para almacenar el directorio actual
directorio_actual = ""

def descargar(url, formato, directorio):
    global directorio_actual  # Acceder a la variable global

    try:
        if not url:
            raise ValueError("No ha colocado ninguna URL")

        # Crear un objeto YouTube
        yt = YouTube(url)

        # Seleccionar directorio de descarga
        if not directorio:
            directorio = os.path.expanduser("~")  # Directorio de descargas por defecto

        if not os.path.exists(directorio):
            os.makedirs(directorio)

        # Actualizar el directorio actual
        directorio_actual = directorio

        if formato == "mp4":
            # Mostrar una alerta mientras se realiza la conversión
            messagebox.showinfo("Conversión", f"El video se está convirtiendo a {formato.upper()}. Esto puede tomar un momento...")
            # Obtener la mejor resolución disponible para el video
            video_stream = yt.streams.get_highest_resolution()
            # Descargar el video en la ubicación especificada
            video_stream.download(output_path=directorio)
            messagebox.showinfo("Éxito", "Descarga de video exitosa!")
        elif formato == "mp3":
            # Mostrar una alerta mientras se realiza la conversión
            messagebox.showinfo("Conversión", f"El video se está convirtiendo a {formato.upper()}. Esto puede tomar un momento...")

            # Obtener la mejor calidad de audio disponible
            audio_stream = yt.streams.filter(only_audio=True).first()

            # Eliminar caracteres no permitidos en el nombre del archivo
            filename = re.sub(r'[\\/*?:"<>|]', '', yt.title)

            # Descargar el audio en formato mp3 en la ubicación especificada
            filename = os.path.join(directorio, f"{filename}.mp3")
            audio_stream.download(output_path=directorio, filename=filename)
            messagebox.showinfo("Éxito", "Conversión a MP3 exitosa!")

        # Borrar el contenido del campo de entrada
        entry_url.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# MP4 a MP3
def seleccionar_archivo():
    try:
        archivo_video = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4;*.avi;*.mov")])
        if archivo_video:
            # Obtener la ubicación del directorio
            directorio = os.path.dirname(archivo_video)
            # Actualizar el directorio actual
            global directorio_actual
            directorio_actual = directorio

            # Mostrar una alerta mientras se realiza la conversión
            messagebox.showinfo("Conversión", "El video se está convirtiendo a MP3. Esto puede tomar un momento...")

            # Convertir el archivo de video a MP3
            video_clip = mp.VideoFileClip(archivo_video)
            audio_clip = video_clip.audio
            # Eliminar caracteres no permitidos en el nombre del archivo
            filename = re.sub(r'[\\/*?:"<>|]', '', os.path.splitext(os.path.basename(archivo_video))[0])
            mp3_filename = os.path.join(directorio, f"{filename}.mp3")
            audio_clip.write_audiofile(mp3_filename)
            audio_clip.close()
            video_clip.close()
            messagebox.showinfo("Éxito", "Conversión a MP3 exitosa!")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")



def seleccionar_directorio():
    global directorio_actual  # Acceder a la variable global

    # Abrir el cuadro de diálogo para seleccionar el directorio de descarga
    directorio = filedialog.askdirectory()
    if directorio:
        # Actualizar el directorio actual
        directorio_actual = directorio
        label_directorio.config(text=f"Directorio de Descarga: {directorio}")

def abrir_directorio():
    global directorio_actual  # Acceder a la variable global

    # Abrir el explorador de archivos en el directorio de descarga
    subprocess.run(["explorer", directorio_actual])

def on_enter(event):
    boton_descargar.config(bg="#ffffff", fg="#000000")

def on_leave(event):
    boton_descargar.config(bg="#ffca28", fg="white")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("HADES0413//MP4//MP3")
ventana.configure(bg="#1a1a1a")  # Cambiar el color de fondo a negro

try:
    # Establecer el ícono de la ventana
    icono = Image.open("icono.png")  # Cambia "icono.png" con el nombre de tu archivo de ícono
    ventana.iconphoto(True, ImageTk.PhotoImage(icono))

    # Marco principal
    marco_principal = ttk.Frame(ventana, padding=(10, 10), style="Marco.TFrame")
    marco_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Ajustar la geometría de la ventana para centrar los elementos
    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(0, weight=1)

    # Etiqueta y entrada para la URL
    label_url = ttk.Label(marco_principal, text="URL:", style="Etiqueta.TLabel")
    label_url.grid(row=0, column=0, sticky=tk.W, pady=(10, 0))

    entry_url = ttk.Entry(marco_principal, width=40, font=('Nunito', 10))
    entry_url.grid(row=0, column=1, sticky=tk.W, pady=(10, 0))

    # Elección del formato
    label_formato = ttk.Label(marco_principal, text="Formato:", style="Etiqueta.TLabel")
    label_formato.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

    format_choice = tk.StringVar()
    format_choice.set("mp4")

    radio_mp4 = ttk.Radiobutton(marco_principal, text="mp4", variable=format_choice, value="mp4", style="Radiobutton.TRadiobutton")
    radio_mp4.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))

    radio_mp3 = ttk.Radiobutton(marco_principal, text="mp3", variable=format_choice, value="mp3", style="Radiobutton.TRadiobutton")
    radio_mp3.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))

    # Botón de descarga
    boton_descargar = tk.Button(marco_principal, text="Descargar", command=lambda: descargar(entry_url.get(), format_choice.get(), label_directorio.cget("text")[len("Directorio de Descarga: "):]), bg="#ffca28", fg="white", font=('Nunito', 12, 'bold'))
    boton_descargar.grid(row=3, column=0, columnspan=2, pady=(20, 0))

    # Botón para seleccionar el directorio de descarga
    boton_seleccionar = tk.Button(marco_principal, text="Seleccionar Directorio", command=seleccionar_directorio, bg="#ffca28", fg="white", font=('Nunito', 10, 'bold'))
    boton_seleccionar.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    # Botón para abrir el directorio de descarga
    boton_abrir = tk.Button(marco_principal, text="Abrir Directorio", command=abrir_directorio, bg="#ffca28", fg="white", font=('Nunito', 10, 'bold'))
    boton_abrir.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    # Botón para seleccionar un archivo de video y convertirlo a MP3
    boton_seleccionar_archivo = tk.Button(marco_principal, text="Seleccionar Video y Convertir a MP3", command=seleccionar_archivo, bg="#ffca28", fg="white", font=('Nunito', 10, 'bold'))
    boton_seleccionar_archivo.grid(row=7, column=0, columnspan=2, pady=(10, 0))

    # Etiqueta para mostrar el directorio de descarga
    label_directorio = ttk.Label(marco_principal, text="Directorio de Descarga: ", style="Etiqueta.TLabel")
    label_directorio.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

    # Asignar funciones de eventos al botón
    boton_descargar.bind("<Enter>", on_enter)
    boton_descargar.bind("<Leave>", on_leave)

    # Estilo mejorado para widgets
    style = ttk.Style()
    style.configure("TLabel", padding=5, background="#1a1a1a", foreground="#ffca28", font=('Nunito', 10))
    style.configure("TRadiobutton", padding=5, background="#1a1a1a", foreground="#ffca28", font=('Nunito', 10))
    style.configure("TFrame", background="#1a1a1a")

except Exception as e:
    print(f"Error al cargar imágenes: {e}")

# Ejecutar la interfaz
ventana.mainloop()
