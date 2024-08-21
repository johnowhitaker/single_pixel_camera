from machine import Pin, ADC, PWM, UART
from utime import sleep
import uos
import sys, select

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)


# Initialize LED, LDR, and Servos
led_pin = Pin("LED", Pin.OUT)
ldr_pin = ADC(28)
servo1 = PWM(Pin(20), freq=50)  # Base
servo2 = PWM(Pin(18), freq=50)  # Top
led_pin.value(0)  # Turn off LED

def move_servos(servo1, pos1, servo2, pos2):
    servo1.duty_u16(pos1)
    servo2.duty_u16(pos2)
    sleep(0.1)  # Give time for servos to move
    ldr_value = ldr_pin.read_u16()
    return ldr_value

# Main loop to listen for commands
while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll(1) # the '1' is how long it will wait for message before looping again (in microseconds)
    if poll_results:
        led_pin.toggle()
        try:
            command = sys.stdin.readline().strip()
            led_pin.toggle()
            # print(f"Received command: {command}")  # Debug: Print the received command
            if command.startswith("MOVE"):
                pos1 = int(command.split(",")[1])
                pos2 = int(command.split(",")[2])
                # print(f"Moving servos to positions: {pos1}, {pos2}")
                ldr_value = move_servos(servo1, pos1, servo2, pos2)
                sys.stdout.write(f"{ldr_value}\n")
        except Exception as e:
            sys.stdout.write(f"Error: {e}\n")
