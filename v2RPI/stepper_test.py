"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-stepper-motor
"""

import RPi.GPIO as GPIO
import time

# Configurar los pines para el motor del eje X
X_STEP_PIN = 16  # Ajusta al pin que usarás para STEP
X_DIR_PIN = 20   # Ajusta al pin que usarás para DIR
X_ENABLE_PIN = 21  # Ajusta al pin que usarás para ENABLE

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(X_STEP_PIN, GPIO.OUT)
GPIO.setup(X_DIR_PIN, GPIO.OUT)
GPIO.setup(X_ENABLE_PIN, GPIO.OUT)

# Número de pasos por revolución
STEPS_PER_REV = 1000

# Habilitar el motor del eje X
GPIO.output(X_ENABLE_PIN, GPIO.LOW)

# Función para mover el motor un número de pasos en una dirección
def move_motor(steps, direction, speed):
    """
    Mueve el motor un número de pasos en la dirección indicada.
    :param steps: Número de pasos a realizar
    :param direction: True para adelante, False para atrás
    :param speed: Velocidad en milisegundos entre pasos
    """
    GPIO.output(X_DIR_PIN, GPIO.HIGH if direction else GPIO.LOW)
    
    for _ in range(steps):
        GPIO.output(X_STEP_PIN, GPIO.HIGH)
        time.sleep(speed / 1000.0)  # Convertir velocidad de ms a segundos
        GPIO.output(X_STEP_PIN, GPIO.LOW)
        time.sleep(speed / 1000.0)

try:
    # Configurar la velocidad del motor (en milisegundos por paso)
    speed = 100  # Ajusta según tus necesidades

    while True:
        print("Moviendo motor hacia adelante...")
        move_motor(STEPS_PER_REV, True, speed)  # Una revolución hacia adelante
        
        time.sleep(1)  # Pausa antes del siguiente movimiento
        
        print("Moviendo motor hacia atrás...")
        move_motor(STEPS_PER_REV, False, speed)  # Una revolución hacia atrás
        
        time.sleep(1)  # Pausa antes del siguiente movimiento

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    # Limpiar configuración GPIO
    GPIO.cleanup()


"""

import RPi.GPIO as GPIO
import time

# Define GPIO pins for L298N driver
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21

# Set GPIO mode and configure pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Constants for stepper motor control
DEG_PER_STEP = 1.8
STEP_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# Function to move the stepper motor one step forward
def step_forward(delay, steps):
    for _ in range(steps):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(delay)
        
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(delay)

# Function to move the stepper motor one step backward
def step_backward(delay, steps):
    for _ in range(steps):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.HIGH)
        time.sleep(delay)
        
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        time.sleep(delay)

try:
    # Set the delay between steps
    delay = 0.001
    while True:
        # Move the stepper motor one revolution in a clockwise direction
        step_forward(delay, STEP_PER_REVOLUTION)

        # Pause for 5 seconds
        time.sleep(5)

        # Move the stepper motor one revolution in an anticlockwise direction
        step_backward(delay, STEP_PER_REVOLUTION)

        # Halt for 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("\nExiting the script.")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()

"""