# Aplicación del servidor
from boot import do_connect
from microdot import Microdot, send_file
from machine import Pin
import neopixel

# Pines de los LEDs individuales
led_rojo = Pin(32, Pin.OUT, value=0)
led_verde = Pin(33, Pin.OUT, value=0)
led_azul = Pin(25, Pin.OUT, value=0)

# Configuración del LED RGB
led_rgb = neopixel.NeoPixel(Pin(27), 4)
for pixel in range(4):
    led_rgb[pixel] = (0, 0, 0)
led_rgb.write()

# Conexión a la red WiFi
do_connect()

# Configuración de la aplicación
app = Microdot()

@app.route('/')
async def pagina_principal(request):
    return send_file('index.html')

@app.route('/<carpeta>/<archivo>')
async def servir_archivo_estatico(request, carpeta, archivo):
    return send_file("/{}/{}".format(carpeta, archivo))

@app.route('/led/toggle/<led>')
async def alternar_led(request, led):
    global led_rojo, led_verde, led_azul

    if led == 'LED1':
        led_rojo.value(not led_rojo.value())
    elif led == 'LED2':
        led_verde.value(not led_verde.value())
    elif led == 'LED3':
        led_azul.value(not led_azul.value())

    return {"estado": "OK"}

@app.route('/rgbled/change/red/<int:rojo>')
async def cambiar_led_rgb_rojo(request, rojo):
    global led_rgb
    verde = led_rgb[0][1]
    azul = led_rgb[0][2]

    for pixel in range(4):
        led_rgb[pixel] = (rojo, verde, azul)

    led_rgb.write()

@app.route('/rgbled/change/blue/<int:azul>')
async def cambiar_led_rgb_azul(request, azul):
    global led_rgb

    rojo = led_rgb[0][0]
    verde = led_rgb[0][1]

    for pixel in range(4):
        led_rgb[pixel] = (rojo, verde, azul)

    led_rgb.write()

@app.route('/rgbled/change/green/<int:verde>')
async def cambiar_led_rgb_verde(request, verde):
    global led_rgb

    rojo = led_rgb[0][0]
    azul = led_rgb[0][2]

    for pixel in range(4):
        led_rgb[pixel] = (rojo, verde, azul)

    led_rgb.write()

# Ejecutar la aplicación en el puerto 80
app.run(port=80)
