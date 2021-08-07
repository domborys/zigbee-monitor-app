import xbee, time, machine

LED_PIN_ID = "D4"
TEMP_SEND_PERIOD = 20000

def handle_packet(packet):
    payload = packet["payload"]
    if payload.startswith(b"ledon"):
        led_on()
    elif payload.startswith(b"ledoff"):
        led_off()
    elif payload.startswith(b"add"):
        add_and_send_result(packet)
    print("Received {} from {}".format(packet["payload"], packet["sender_eui64"]))

def led_on():
    led_pin.value(0)

def led_off():
    led_pin.value(1)

def add_and_send_result(packet):
    try:
        result = add_numbers_in_payload(packet["payload"])
        xbee.transmit(packet["sender_eui64"], "addresult {}".format(result))
    except Exception as err:
        print(err)

def add_numbers_in_payload(payload):
    payload_split = payload.split()
    return int(payload_split[1]) + int(payload_split[2])

def send_temperature():
    temp = xbee.atcmd("TP")
    msg = "temp {}".format(temp)
    try:
        xbee.transmit(xbee.ADDR_COORDINATOR, msg)
    except Exception as err:
        print(err)

led_pin = machine.Pin(LED_PIN_ID, machine.Pin.OUT, value=1)
last_temp_time = time.ticks_ms()

while True:
    p = xbee.receive()
    if p is not None:
        handle_packet(p)
    
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_temp_time) > TEMP_SEND_PERIOD:
        last_temp_time = current_time
        send_temperature()

    

