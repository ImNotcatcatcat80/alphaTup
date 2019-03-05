from microbit import *
import radio

radio.config(length=251, queue=3, channel=32, power=7, address=0x75202201, group=120)
radio.on()
rec_str = ""
loop_str = ""
cy_ctr = 0
display.scroll("Ready")
sleep(500)
display.clear()

while True:
    rec_str = radio.receive()
    if isinstance(rec_str, str) and rec_str is not None:
        loop_str = rec_str
    display.scroll(loop_str)
    sleep(4000)
    
    if rec_str is None:
        cy_ctr += 1
        if cy_ctr >= 10:
            cy_ctr = 0
            display.show(Image.DIAMOND)
            sleep(500)
            display.show(Image.DIAMOND_SMALL)
            sleep(500)
            display.clear()
            sleep(4000)