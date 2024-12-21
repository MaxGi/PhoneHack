import RPi.GPIO as GPIO
import time
import socket

s = socket.socket()
host = socket.gethostname()
port = 3000

s.connect((host, port))

def send_pd(mess):
    send_mess = str(mess) + " ;"
    s.send(send_mess.encode('utf-8'))
    print("Sent mess: ", mess)

row = [17, 27, 22, 10]
collumn = [14, 15, 4]

r_pin = 9
hang_up_pin = 11

debounce_h = 0
debounce_r = 0

button_combinations = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]

old_state = []
old_r = 0
old_hang = 0

GPIO.setmode(GPIO.BCM)

for pin in collumn:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in row:
    GPIO.setup(pin, GPIO.OUT)
    

GPIO.setup(hang_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(r_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


send_pd(50)

while True:
    states = []
    for row_pin in row:
        GPIO.output(row_pin, GPIO.HIGH)
        for collumn_pin in collumn:
            states.append(GPIO.input(collumn_pin))
        GPIO.output(row_pin, GPIO.LOW)

    if states != old_state:
#        print(states)
        if sum(states) < 2:
            for index, combo in enumerate(button_combinations):
                if states == combo:
#                    print(index)
                    send_pd(index)
                    
    old_state = states
    r_state = GPIO.input(r_pin)
    h_state = GPIO.input(hang_up_pin)
    
    #Debounce test
    if h_state == 0:
        debounce_h -= 1
        if debounce_h < 0:
            debounce_h = 0
    else:
        debounce_h += 1
        if debounce_h > 10:
            debounce_h = 10
    
    if r_state != old_r:
#        print("R",r_state)
        if r_state == 0:
            send_pd(40)
            
    if h_state != old_hang:
        if h_state == 0:
            send_pd(55)
        else:
            send_pd(50)
#        print("H",h_state)

    print("R: ", r_state, " H: ", h_state, " D: ", debounce_h)
    old_hang = h_state
    old_r = r_state
    time.sleep(0.1)


GPIO.cleanup()

print("Goodbye!")
