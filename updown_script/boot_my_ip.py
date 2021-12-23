#!/home/pi/spotmicroai/venv/bin/python3 -u

from spotmicroai.lcd_screen_controller import LCD_16x2_I2C_driver
import socket

#i2c_address = Config().get('lcd_screen_controller[0].lcd_screen[0].address')

i2c_address = "0x27"

lcd_screen = LCD_16x2_I2C_driver.lcd(address=int(i2c_address, 0))

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def startup():

    myIp    = extract_ip()

    lcd_screen.lcd_clear()
    lcd_screen.lcd_display_string("System Ip", 1)
    lcd_screen.lcd_display_string(myIp, 2)

startup()
