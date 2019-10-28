# archivo:    flask/app.py
# asignatura: Desarrollo de Aplicaciones para Internet
# práctica:   Prácticas 2, 3
# autor:      José María Martín Luque

from flask import Flask
from flask import render_template
from flask import request

from pickleshare import *

# Para hacer hasing de las contraseñas
import hashlib
import os

from PIL import Image
import uuid

app = Flask(__name__)
db = PickleShareDB('./p3db')

@app.route('/p3/')
def p3(login=None):
    return render_template('p3.html')

@app.route('/p3/signup/', methods=['GET', 'POST'])
def p3_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        salt = os.urandom(32)

        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        salted_password = salt + key

        db[email] = {'password': salted_password}

        return render_template('welcome.html', email=email)
    else:
        return render_template('signup.html')

@app.route('/p3/login/', methods=['POST'])
def p3_login():
    
    email = request.form['email']
    password = request.form['password']

    try:
        stored_password = db[email]['password']


        stored_salt = stored_password[:32]
        stored_key = stored_password[32:]

        input_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            stored_salt,
            100000
        )

        if input_key == stored_key:
            return render_template('p3.html', login="Sesión inciada")
        else:
            return render_template('p3.html', login="Contraseña incorrecta")

        
    except KeyError: 
        return render_template('p3.html', login="Usuario incorrecto")

@app.route('/p2/')
@app.route('/p2/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# http://127.0.0.1:8080/p2/fractal?x1=-2.0&x2=1.0&y1=-1.5&y2=1.5&ancho=300
@app.route('/p2/fractal')
def fractal():
    x1 = request.args.get('x1')
    x2 = request.args.get('x2')
    y1 = request.args.get('y1')
    y2 = request.args.get('y2')
    ancho = request.args.get('ancho')
    nombre_fichero = str(uuid.uuid1())  + '.png'

    pintaMandelbrot(float(x1), float(y1), float(x2), float(y2), int(ancho), 255, nombre_fichero)

    return render_template('fractal.html', imagen=nombre_fichero)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def pintaMandelbrot(x1, y1, x2, y2, ancho, iteraciones, nombre_fichero):
    """Función que pinta en una ventana y guarda en formato PNG el fractal de 
    Mandelbrot.

    Parámetros:
    x1 -- Coordenada x de la posición inicial
    y1 -- Coordenada y de la posición inicial
    x2 -- Coordenada x de la posición final
    y2 -- Coordenada y de la posición final
    ancho -- Anchura de la imagen
    iteraciones -- Número de iteraciones
    nombre_ficher -- Nombre del fichero en el que se va a guardar la imagen
    
    Nota: iteraciones tiene que ser un valor menor que 1000.
    """
    xa = x1
    xb = x2
    ya = y1
    yb = y2
    maxIt = iteraciones
    # image size
    imgx = ancho
    imgy = int(abs(y2 - y1) * ancho / abs(x2 - x1))

    im = Image.new('RGB', (imgx, imgy), color='black')

    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya

        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = zx + zy * 1j
            c = z

            for i in range(maxIt):
                if abs(z) > 2.0:
                    break
                z = z * z + c

            i = maxIt - i

            col = (i % 10*25, i % 16*16, i % 8*32)

            im.putpixel((x, y), col)

    im.save('./static/' + nombre_fichero, 'PNG')  # Grabamos en formato PPM
