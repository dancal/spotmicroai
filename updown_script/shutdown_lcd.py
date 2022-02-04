#!/usr/bin/python

from spotmicroai.lcd_screen_controller import LCD_16x2_I2C_driver
import socket

#i2c_address = Config().get('lcd_screen_controller[0].lcd_screen[0].address')

i2c_address = "0x27"

lcd_screen = LCD_16x2_I2C_driver.lcd(address=int(i2c_address, 0))

def shutdown():

    lcd_screen.lcd_clear()
    lcd_screen.lcd_display_string("Bye Bye!.", 1)
    lcd_screen.lcd_display_string("Shutdown..", 2)

shutdown()
