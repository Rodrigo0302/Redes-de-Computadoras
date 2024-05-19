import tkinter as tk
import re
from tkinter import messagebox
import calculadoraIPsClass as calc

def validar_numeros(nuevo_valor):
    # Esta función se llama cada vez que el contenido del cuadro de texto cambia
    # new_value es el nuevo valor del cuadro de texto
    if nuevo_valor.isdigit():
        num = int(nuevo_valor)
        if 1 <= num <= 31:
            return True
        else:
            messagebox.showerror("Entrada incorrecta", "Escribe un numero entre 1 y 31")
            return False
    elif nuevo_valor == "":
        # Permitir el campo vacío
        return True
    else:
        messagebox.showerror("Entrada incorrecta", "Escribe un numero valido")
        return False

def validate_ip_format(P):
    # Expresión regular para validar una dirección IP
    ip_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\."
                            r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\."
                            r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\."
                            r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$")
    if ip_pattern.match(P):
        return True
    elif P == "":
        return True  # Permitir campo vacío
    else:
        messagebox.showerror("Entrada incorrecta", "Ingrese una dirección IP válida")
        return False
    
def actualizar_tabla(ventana,textarea, campo_ip, campo_mascara_actual, campo_mascara_nueva):
    #Validar que los campos no esten vacios
    if campo_ip.get() == "" or campo_mascara_actual.get() == "" or campo_mascara_nueva.get() == "":
        messagebox.showerror("Entrada incorrecta", "Llena todos los campos")
        return
    #Validar que la mascara nueva sea mayor a la actual
    if int(campo_mascara_nueva.get()) <= int(campo_mascara_actual.get()):
        messagebox.showerror("Entrada incorrecta", "La mascara nueva debe ser mayor a la actual")
        return
    #Validar que la IP sea valida
    if not validate_ip_format(campo_ip.get()):
        return

    #Obtener los campos de mascara y pasarlos a enteros
    mascara_actual = int(campo_mascara_actual.get())
    mascara_nueva = int(campo_mascara_nueva.get())
    tab1, tab2,texto = calc.CalculadoraIPs.main_sub(campo_ip.get(), mascara_actual, mascara_nueva)    

    #Limpiar el text area
    textarea.config(state='normal')
    textarea.delete('1.0', tk.END)
    textarea.config(state='disabled')

    #Imprimir la tabla
    textarea.config(state='normal')
    textarea.insert(tk.END, tab1.get_string())
    textarea.insert(tk.END, "\n\n")
    textarea.insert(tk.END, texto)
    textarea.insert(tk.END, "\n\n")
    textarea.insert(tk.END, tab2.get_string())
    textarea.config(state='disabled')

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Interfaz de Subneteo")

    ventana.geometry("1200x800")

    #Registro de validación de campos
    validar_numeros_cmd = (ventana.register(validar_numeros), '%P')

    # Etiqueta y campo de entrada para la dirección IP
    etiqueta_ip = tk.Label(ventana, text="Dirección IP:")
    etiqueta_ip.pack()
    campo_ip = tk.Entry(ventana)
    campo_ip.pack()

    # Etiqueta y campo de entrada para la máscara actual
    etiqueta_mascara_actual = tk.Label(ventana, text="Máscara actual:")
    etiqueta_mascara_actual.pack()
    campo_mascara_actual = tk.Entry(ventana, validate='key', validatecommand=validar_numeros_cmd)
    campo_mascara_actual.pack()

    # Etiqueta y campo de entrada para la nueva máscara
    etiqueta_mascara_nueva = tk.Label(ventana, text="Nueva máscara:")
    etiqueta_mascara_nueva.pack()
    campo_mascara_nueva = tk.Entry(ventana, validate='key', validatecommand=validar_numeros_cmd)
    campo_mascara_nueva.pack()

    # Botón para imprimir la tabla
    boton_imprimir = tk.Button(ventana, text="Calcular Subredes", command= lambda: actualizar_tabla(ventana,text_area, campo_ip, campo_mascara_actual, campo_mascara_nueva))
    boton_imprimir.pack()

    # Etiqueta para mostrar la tabla
    etiqueta_tabla = tk.Label(ventana, text="Tabla de subredes")
    etiqueta_tabla.pack()
    text_area = tk.Text(ventana, height=80, width=150)
    text_area.pack(padx=10, pady=10)
    text_area.config(state='disabled')

    

    ventana.mainloop()

crear_interfaz()