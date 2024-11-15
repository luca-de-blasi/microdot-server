# Aplicacion del servidor
from boot import do_connect
from microdot import Microdot, send_file
from machine import Pin, ADC
import ds18x20
import onewire
import time

# Configuración de pines y sensores
buzzer = Pin(14, Pin.OUT)
sensor_temperatura_pin = Pin(19)
sensor_temperatura = ds18x20.DS18X20(onewire.OneWire(sensor_temperatura_pin))
temperatura_actual = 24

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

@app.route('/sensors/ds18b20/read')
async def leer_temperatura(request):
    global sensor_temperatura
    sensor_temperatura.convert_temp()
    time.sleep_ms(1)
    dispositivos = sensor_temperatura.scan()
    for dispositivo in dispositivos:
        temperatura_actual = sensor_temperatura.read_temp(dispositivo)
    
    respuesta = {'temperatura': temperatura_actual}
    return respuesta

@app.route('/setpoint/set/<int:valor>')
async def configurar_setpoint(request, valor):
    respuesta = {}
    print("Configurando setpoint")
    if valor >= temperatura_actual:
        buzzer.on()
        respuesta = {'buzzer': 'Encendido'}
    else:
        buzzer.off()
        respuesta = {'buzzer': 'Apagado'}
    
    return respuesta

# Ejecutar la aplicación en el puerto 80
app.run(port=80)
