# archivo:    flask/app.py
# asignatura: Desarrollo de Aplicaciones para Internet
# práctica:   Prácticas 2, 3, 4
# autor:      José María Martín Luque

from flask import Flask, render_template, request, redirect, session, url_for

from pickleshare import *

# Para hacer hasing de las contraseñas
import hashlib
import os

from PIL import Image

from pymongo import MongoClient

import uuid

app = Flask(__name__)

app.secret_key = "59d112cd063f89a074903d667117316774255a59f582e724"

db_users = PickleShareDB('./p3db')

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
db_data = client.SampleCollections        # Elegimos la base de datos de ejemplo

@app.route('/p4/pokemon/', methods=['GET', 'POST'])
def search_pokemon():
    if request.method == 'POST':
        query = request.form['query']
        query_regex = '.*' + query + '.*'

        results = db_data.samples_pokemon.find({'name' : {'$regex' : query_regex, '$options' : 'i'}})

        return render_template('pokemon.html', busqueda='Pokémon', results=results)

    else:
        return render_template('pokemon.html', busqueda='Pokémon', results=[])

@app.route('/p4/friends/', methods=['GET', 'POST'])
def search_friends():
    if request.method == 'POST':
        query = request.form['query']
        query_regex = '.*' + query + '.*'

        results = db_data.samples_friends.find({'name' : {'$regex' : query_regex, '$options' : 'i'}})

        return render_template('friends.html', busqueda='Episodios de Friends',results=results)

    else:
        return render_template('friends.html', busqueda='Episodios de Friends', results=[])

@app.route('/p3/')
def p3():
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

        db_users[email] = {'password': salted_password}

        return render_template('welcome.html', email=email)
    else:
        return render_template('signup.html')

@app.route('/p3/login/', methods=['POST', 'GET'])
def p3_login():
    
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        try:
            stored_password = db_users[email]['password']

            stored_salt = stored_password[:32]
            stored_key = stored_password[32:]

            input_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),  # Convert the password to bytes
                stored_salt,
                100000
            )

            if input_key == stored_key:
                session['email'] = email
                return redirect(url_for('p3'))
            else:
                return render_template('login.html', error="Contraseña incorrecta")
            
        except KeyError: 
            return render_template('login.html', error="Usuario incorrecto")
    else:
        return render_template('login.html')

@app.route('/p3/logout/', methods=['GET'])
def p3_logout():
    session['email'] = ''
    return redirect(url_for('p3'))

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
