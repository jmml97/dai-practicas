# ./flask/app.py

from flask import Flask
from flask import render_template
from flask import request

from PIL import Image
import uuid

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# http://127.0.0.1:8080/fractal?x1=-2.0&x2=1.0&y1=-1.5&y2=1.5&ancho=300
@app.route('/fractal')
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

# Función que pinta en una ventana y salva en formato PNG el fractal de Mandelbrot. Nota: iteraciones tiene que ser menor que 1000
def pintaMandelbrot(x1, y1, x2, y2, ancho, iteraciones, nombreFichero):
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

    im.save('./static/' + nombreFichero, 'PNG')  # Grabamos en formato PPM
