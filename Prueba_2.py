import tkinter as tk  
from tkinter import messagebox
import mysql.connector 
import hashlib



def hash_password(password):  
    if not password:  
        raise ValueError("La contraseña no puede estar vacía")  
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

    

# Función para verificar el inicio de sesión  
def login():  
    username = entry_username.get()  
    password = entry_password.get()
     
    if not username or not password:  
        messagebox.showerror("Error", "Usuario y contraseña no pueden estar vacíos")  
        return   

    try:  
        password = hash_password(password)
        # Conectar a la base de datos  
        conn = mysql.connector.connect(  
            host="localhost",  
            user="root",  # Usuario por defecto de XAMPP  
            password="",  # Contraseña por defecto de XAMPP  
            database="login_db"  
        )  
        cursor = conn.cursor()  

        # Verificar si el usuario y la contraseña coinciden  
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"  
        cursor.execute(query, (username, password))  
        result = cursor.fetchone()  

        if result:  
            messagebox.showinfo("Login", "Inicio de sesión exitoso")  
        else:  
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")  

    except ValueError as e:  
        messagebox.showerror("Error", str(e))
    except mysql.connector.Error as err:  
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")  

    finally:  
        if conn.is_connected():  
            cursor.close()  
            conn.close() 
# Función para registrar un nuevo usuario  
def register():  
    username = entry_username.get()  
    password = entry_password.get()
     
    try:  
       
        # Conectar a la base de datos  
        conn = mysql.connector.connect(  
            host="localhost",  
            user="root",  # Usuario por defecto de XAMPP  
            password="",  # Contraseña por defecto de XAMPP  
            database="login_db"  
        )  
        cursor = conn.cursor() 

        password = hash_password(password)

        # Insertar el nuevo usuario  
        query = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"  
        cursor.execute(query, (username, password))  
        conn.commit()  

        messagebox.showinfo("Registro", "Usuario registrado exitosamente")  

    except ValueError as e:  
        messagebox.showerror("Error", str(e))  
    except mysql.connector.Error as err:  
        messagebox.showerror("Error", f"Error al registrar el usuario: {err}") 

    finally:  
        if conn.is_connected():  
            cursor.close()  
            conn.close() 

# Crear la ventana principal  
root = tk.Tk()  
root.title("Login y Registro")

# Crear y colocar los elementos en la ventana  
label_username = tk.Label(root, text="Usuario:")  
label_username.grid(row=0, column=0, padx=10, pady=10)  

entry_username = tk.Entry(root)  
entry_username.grid(row=0, column=1, padx=10, pady=10)  

label_password = tk.Label(root, text="Contraseña:")  
label_password.grid(row=1, column=0, padx=10, pady=10)  

entry_password = tk.Entry(root, show="*")  
entry_password.grid(row=1, column=1, padx=10, pady=10)  

button_login = tk.Button(root, text="Iniciar Sesión", command=login)  
button_login.grid(row=2, column=0, padx=10, pady=10)  

button_register = tk.Button(root, text="Registrar", command=register)  
button_register.grid(row=2, column=1, padx=10, pady=10)  

# Iniciar la aplicación  
root.mainloop()