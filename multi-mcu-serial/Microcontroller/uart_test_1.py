import board
import busio
import time
import random
import adafruit_dotstar

uart = busio.UART(
    board.TX,
    board.RX,
    baudrate=115200,
    parity=None,
    stop=1,
    bits=8,
    timeout=0
)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BRIGHTNESS = 0.5

END_OF_MSG = '\n'

dotstar = adafruit_dotstar.DotStar(
    board.APA102_SCK,
    board.APA102_MOSI,
    n=1,
    brightness=0.1,
    auto_write=False
)

dotstar.fill(BLACK)
dotstar.show()

print(uart)
b = None
msg = ""
i = 1
next_send_time = None
data_string: str = ""

def dotstar_show(dotstar: adafruit_dotstar.DotStar, color, brightness):
    dotstar.fill(color)
    dotstar.brightness = brightness
    dotstar.show()

while True:
    now = time.monotonic()

    if next_send_time is None:
        delay = random.random() * 5
        #print("Delay: ", delay)
        next_send_time = now + delay

    if next_send_time <= now:
        message = "Hello #{} from nRF52840{}".format(i, END_OF_MSG)
        dotstar_show(dotstar, GREEN, BRIGHTNESS)
        print("Sending #{}...".format(i))
        write_buffer = message.encode("utf-8")
        uart.write(write_buffer)
        next_send_time = None
        dotstar_show(dotstar, BLACK, 0)
        i += 1

    if uart.in_waiting > 0:
        dotstar_show(dotstar, BLUE, BRIGHTNESS)

        b = uart.read(1)
        c = b.decode("utf-8")
        if c == END_OF_MSG:
            print(">> " + data_string)
            data_string = ""
        else:
            data_string += c

        dotstar_show(dotstar, BLACK, 0)
