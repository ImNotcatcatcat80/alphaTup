from microbit import *
import radio

status_dict = {
    "init": 0, 
    "compose": 1, 
    "req_send": 2, 
    "send_y": 3, 
    "send_n": 4, 
    "sending": 5, 
    "req_delete": 6, 
    "delete_y": 7, 
    "delete_n": 8, 
    "deleting": 9 
    }
status = 0
alpha = "-+0123456789_abcdefghijklmnopqrstuvwxyz/"
alpha_tup = tuple(alpha)
out_str = ""

while(True):
    
    if(status == status_dict["init"]):
        radio.config(length=251, queue=3, channel=32, power=7, address=0x75202201, group=120)
        radio.on()
        display.scroll("Ready")
        sleep(300)
        disp_chr_index = 12
        status = status_dict["compose"]

    if(status == status_dict["compose"]):
        if(accelerometer.get_x() > 300 and disp_chr_index < 39):
            disp_chr_index += 1
        elif(accelerometer.get_x() < -300 and disp_chr_index > 0):
            disp_chr_index -= 1
        scroll_speed = 600 - abs(abs(accelerometer.get_x()) - 300)
        if(scroll_speed < 100):
            scroll_speed = 100
        display.show(alpha_tup[disp_chr_index])
        sleep(scroll_speed)
        display.clear()
        if(button_a.is_pressed()):
            if(disp_chr_index == 12):
                out_str += " "
            else:
                out_str += alpha_tup[disp_chr_index]
            sleep(300)
        if(button_b.is_pressed()):
            display.scroll(out_str)
            sleep(500)
            display.scroll("|  send?")
            status = status_dict["req_send"]
    
    if(status == status_dict["req_send"]):
        display.show("*")
        if(accelerometer.get_x() > 350):
            status = status_dict["send_y"]
        if(accelerometer.get_x() < -350):
            status = status_dict["send_y"]
    
    if(status == status_dict["send_n"]):
        display.show("N")
        if(accelerometer.get_x() > 350):
            status = status_dict["send_y"]
        if(button_a.is_pressed()):
            display.scroll("delete?")
            status = status_dict["req_delete"]
    
    if(status == status_dict["send_y"]):
        display.show("Y")
        if(accelerometer.get_x() < -350):
            status = status_dict["send_n"]
        if(button_a.is_pressed()):
            status = status_dict["sending"]
    
    if(status == status_dict["sending"]):
        radio.send(out_str)
        display.show(Image.DIAMOND)
        sleep(300)
        display.show(Image.DIAMOND_SMALL)
        sleep(300)
        display.clear()
        out_str = ""
        disp_chr_index = 12
        status = status_dict["compose"]
        sleep(600)
    
    if(status == status_dict["req_delete"]):
        display.show("*")
        if(accelerometer.get_x() > 350):
            status = status_dict["delete_y"]
        if(accelerometer.get_x() < -350):
            status = status_dict["delete_n"]
    
    if(status == status_dict["delete_n"]):
        display.show("N")
        if(accelerometer.get_x() > 350):
            status = status_dict["delete_y"]
        if(button_a.is_pressed()):
            status = status_dict["compose"]
    
    if(status == status_dict["delete_y"]):
        display.show("Y")
        if(accelerometer.get_x() < -350):
            status = status_dict["delete_n"]
        if(button_a.is_pressed()):
            status = status_dict["deleting"]
    
    if(status == status_dict["deleting"]):
        display.show(Image.SQUARE_SMALL)
        sleep(300)
        display.show(Image.SQUARE)
        sleep(300)
        display.clear()
        out_str = ""
        disp_chr_index = 12
        status = status_dict["compose"]
        sleep(600)
    