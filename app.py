from flask import Flask
import pymongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.secret_key="123456"

app.config['UPLOAD_FOLDER']='./static/imagenes'

miConexion = pymongo.MongoClient("mongodb+srv://DannyCastro:danny@cluster0.elfxezh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

baseDatos = miConexion['TiendaP']

productos = baseDatos['Productos']

usuarios = baseDatos['usuarios']

if __name__=="__main__":
    from controlador.productoController import * # * importa todo lo que esta en el archivo
    from controlador.usuarioController import * 
    app.run(port=5000,debug=True)
    