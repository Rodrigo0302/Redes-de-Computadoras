import tkinter as tk
import customtkinter
from CTkMessagebox import CTkMessagebox
import re
import calculadoraIPsClass as calc

def validar_numeros(nuevo_valor):
    # Esta función se llama cada vez que el contenido del cuadro de texto cambia
    # new_value es el nuevo valor del cuadro de texto
    if nuevo_valor.isdigit():
        num = int(nuevo_valor)
        if 1 <= num <= 31:
            return True
        else:
            #messagebox.showerror("Entrada incorrecta", "Escribe un numero entre 1 y 31")
            CTkMessagebox(title="Entrada incorrecta", message="Escribe un numero entre 1 y 31", icon="cancel")
            return False
    elif nuevo_valor == "":
        # Permitir el campo vacío
        return True
    else:
        #messagebox.showerror("Entrada incorrecta", "Escribe un numero valido")
        CTkMessagebox(title="Entrada incorrecta", message="Escribe un numero valido", icon="cancel")
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
        #messagebox.showerror("Entrada incorrecta", "Ingrese una dirección IP válida")
        CTkMessagebox(title="Entrada incorrecta", message="Ingrese una dirección IP válida", icon="cancel")
        return False
    
def actualizar_tabla(ventana,textArea,campo_ip, campo_mascara_actual, campo_mascara_nueva):

    

    #Validar que los campos no esten vacios
    if campo_ip.get() == "" or campo_mascara_actual.get() == "" or campo_mascara_nueva.get() == "":
        #messagebox.showerror("Entrada incorrecta", "Llena todos los campos")
        CTkMessagebox(title="Entrada incorrecta", message="Llena todos los campos")
        return
    #Validar que la mascara nueva sea mayor a la actual
    if int(campo_mascara_nueva.get()) <= int(campo_mascara_actual.get()):
        #messagebox.showerror("Entrada incorrecta", "La mascara nueva debe ser mayor a la actual")
        CTkMessagebox(title="Entrada incorrecta", message="La mascara nueva debe ser mayor a la actual")
        return
    #Validar que la IP sea valida
    if not validate_ip_format(campo_ip.get()):
        return

    #Obtener los campos de mascara y pasarlos a enteros
    mascara_actual = int(campo_mascara_actual.get())
    mascara_nueva = int(campo_mascara_nueva.get())
    tab1, tab2,texto = calc.CalculadoraIPs.main_sub(campo_ip.get(), mascara_actual, mascara_nueva)

    #Actualizar el campo de texto
    textArea.configure(state='normal')
    textArea.delete('1.0', tk.END)
    textArea.insert(tk.END, tab1.get_string())
    textArea.insert(tk.END, "\n")
    textArea.insert(tk.END, texto)
    textArea.insert(tk.END, "\n")
    textArea.insert(tk.END, tab2.get_string())
    textArea.configure(state='disabled')

            

def crear_interfaz():
    #ventana = tk.Tk()
    ventana = customtkinter.CTk()
    ventana.title("Interfaz de Subneteo")

    ventana.geometry("1200x800")

    #Registro de validación de campos
    validar_numeros_cmd = (ventana.register(validar_numeros), '%P')

    # Etiqueta y campo de entrada para la dirección IP
    #etiqueta_ip = tk.Label(ventana, text="Dirección IP:", font=("Arial",13))
    etiqueta__ip = customtkinter.CTkLabel(master=ventana, text="Dirección IP:")
    etiqueta__ip.pack()
    #campo_ip = tk.Entry(ventana)
    campo_ip = customtkinter.CTkEntry(master=ventana, placeholder_text="XXX.XXX.XXX.XXX")
    campo_ip.pack()

    # Etiqueta y campo de entrada para la máscara actual
    #etiqueta_mascara_actual = tk.Label(ventana, text="Máscara actual:",font=("Arial",13))
    etiqueta_mascara_actual = customtkinter.CTkLabel(master=ventana, text="Máscara actual:")
    etiqueta_mascara_actual.pack()
    #campo_mascara_actual = tk.Entry(ventana, validate='key', validatecommand=validar_numeros_cmd)
    campo_mascara_actual = customtkinter.CTkEntry(master=ventana, validate='key', validatecommand=validar_numeros_cmd, placeholder_text="24")
    campo_mascara_actual.pack()

    # Etiqueta y campo de entrada para la nueva máscara
    #etiqueta_mascara_nueva = tk.Label(ventana, text="Nueva máscara:",font=("Arial",13))
    etiqueta_mascara_nueva = customtkinter.CTkLabel(master=ventana, text="Nueva máscara:")
    etiqueta_mascara_nueva.pack()
    #campo_mascara_nueva = tk.Entry(ventana, validate='key', validatecommand=validar_numeros_cmd,font=("Arial",13))
    campo_mascara_nueva = customtkinter.CTkEntry(master=ventana, validate='key', validatecommand=validar_numeros_cmd, placeholder_text="26")
    campo_mascara_nueva.pack()

    # Botón para imprimir la tabla
    #boton_imprimir = tk.Button(ventana, text="Calcular Subredes", command= lambda: actualizar_tabla(ventana,text_area, campo_ip, campo_mascara_actual, campo_mascara_nueva))
    boton_imprimir = customtkinter.CTkButton(master=ventana, corner_radius=10, command= lambda: actualizar_tabla(ventana,text_area, campo_ip, campo_mascara_actual, campo_mascara_nueva), 
                                             text="Calcular Subredes", font=("Arial",13))
    
    boton_imprimir.place(relx=0.5, rely=0.5, anchor= tk.CENTER)
    boton_imprimir.pack()

    # Etiqueta para mostrar la tabla
    #etiqueta_tabla = tk.Label(ventana, text="Tabla de subredes",font=("Arial",13))
    etiqueta_tabla = customtkinter.CTkLabel(master=ventana, text="Tabla de subredes")
    etiqueta_tabla.pack()

    #text_area = tk.Text(ventana, height=80, width=150)
    text_area = customtkinter.CTkTextbox(master=ventana, height=700, width=1500, text_color="white",font=("Courier",15))
    text_area.configure(state='disabled')
    text_area.pack(padx=10, pady=10)

    #textarea = customtkinter.CTkTextbox(master=ventana, height=700, width=1500, corner_radius=10,text_color="white")
    #textarea.configure(state='disabled')
    #textarea.pack()
    

    

    ventana.mainloop()

crear_interfaz()