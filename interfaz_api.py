import tkinter as tk
from tkinter import messagebox
import requests

ip_api="http://127.0.0.1:8000"

def login():
    #variales que extraen la ifnormacion que se puso en el formulario de la interfaz
    username=username_entry.get()
    password=password_entry.get()

    #datos para el endpoint
    data={"username":username,"password":password}

    try:
        #solicitar hacer el post
        response=requests.post(f"{ip_api}/login",data)

        if response.status_code==200:
            result=response.json()
            messagebox.showinfo("Exito",f"Login exitoso token{result['acces_token']}")

        else:
            messagebox.showinfo("Error","Credenciales invalidas")

    except Exception as e:
        messagebox.showinfo("Error",f"No se pudo conecatr con la api {e}")

#creacion de ventana

root=tk.Tk() #clases de la vista y el formato de la vista 
root.title("Login")

#widget interfaz
tk.Label(root,text="Usario").pack(pady=5)
username_entry=tk.Entry(root)
username_entry.pack(pady=5)
tk.Label(root,text="Contraseña").pack(pady=5)
password_entry=tk.Entry(root)
password_entry.pack(pady=5)

#comandos para el login en la interf
login_button=tk.Button(root,text="Iniciar Login!",command=login)
login_button.pack(pady=10)
root.mainloop()
