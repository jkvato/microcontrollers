import time
import serial
import random

# Use /dev/ttyS0 for Raspberry Pi 4
# Use /dev/ttyAMA0 for Raspberry Pi 1
PORT = '/dev/ttyS0'
#PORT = '/dev/ttyAMA0'

ser = serial.Serial(
    port=PORT,
    baudrate = 115200,
    timeout=0
)

msg = ""
i = 1
next_send_time = None
data_string: str = ""

while True:
    now = time.monotonic()

    if next_send_time is None:
        delay = random.random() * 5
        #print("Delay: ", delay)
        next_send_time = now + delay

    if next_send_time <= now:
        msg = "Hello #{} from Raspberry Pi\n".format(i)
        print("Sending #{}...".format(i))
        ser.write(msg.encode('utf-8'))
        next_send_time = None
        i += 1

    if ser.in_waiting > 0:
        b = ser.read(1)
        c = b.decode("utf-8")
        if c == '\n':
            print(">> " + data_string)
            data_string = ""
        else:
            data_string += c