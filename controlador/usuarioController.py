from app import app, usuarios
from flask import render_template, request, redirect, session
import yagmail
import threading

# Ruta para el login
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("frmLogin.html")
    else:
        username = request.form.get('txtUsername')
        password = request.form.get('txtPassword')

        if not username or not password:
            mensaje = "Por favor, completa todos los campos."
            return render_template("frmLogin.html", mensaje=mensaje)

        usuario = {
            "username": username,
            "password": password
        }

        try:
            userExiste = usuarios.find_one(usuario)
        except Exception as e:
            mensaje = "Error al verificar usuario. Intente más tarde."
            return render_template("frmLogin.html", mensaje=mensaje)

        if userExiste:
            session['user'] = usuario
            email = yagmail.SMTP("danicastro.nz@gmail.com", open(".password", "r", encoding="UTF-8").read())
            
            asunto = "Notificación de ingreso a la tienda"
            mensaje = f"Se informa que el usuario {username} ha ingresado al sistema"
            destinatario = "danicastro.nz@gmail.com"

            thread = threading.Thread(target=enviarCorreo, args=(email, destinatario, asunto, mensaje))
            thread.start()
            return redirect('/api/listarProductos') 
        else:
            mensaje = "Credenciales de ingreso inválidas"
            return render_template("frmLogin.html", mensaje=mensaje)


# Ruta para cerrar la sesión
@app.route("/salir")
def salir():
    session.pop('user', None)
    session.clear()  
    return render_template("frmLogin.html", mensaje="Se ha cerrado sesión")

def enviarCorreo(email, destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=mensaje)