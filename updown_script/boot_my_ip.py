#!/usr/bin/python

from spotmicroai.lcd_screen_controller import LCD_16x2_I2C_driver
import socket
import os
import subprocess

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

i2c_address = "0x27"
host        = 'mungmung'

ipaddr      = get_ip()
lcd_screen  = LCD_16x2_I2C_driver.lcd(address=int(i2c_address, 0))

lcd_screen.lcd_clear()
lcd_screen.lcd_display_string(host, 1)
lcd_screen.lcd_display_string(ipaddr, 2)
