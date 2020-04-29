from time import sleep
from typing import Dict

from pysphero.core import Sphero
from pysphero.driving import Direction
from pysphero.driving import TankDriveDirection
from pysphero.driving import DirectionRawMotor
from pysphero.device_api.user_io import Color
from pysphero.device_api.sensor import Attitude

from pysphero.device_api.sensor import CoreTime, Quaternion, Attitude, Accelerometer, Velocity, Speed


def notify_callback(data: Dict):
    info = ", ".join("{:1.2f}".format(data.get(param)) for param in Accelerometer)
    print(f"[{data.get(CoreTime.core_time):1.2f}] Accelerometer(x, y, z): {info}", end="\r")

def main():
    #mac_address = "aa:bb:cc:dd:ee:ff"
    mac_address = "f7:e2:c2:7d:4c:bb"
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()
        sleep(2)
        sphero.user_io.set_all_leds_8_bit_mask()
        #testing = True
        #while(testing):
            #sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(blue=255,green=255,red=255),back_color=Color(blue=255,green=255,red=255))
        sphero.user_io.set_led_matrix_one_color(color=Color(blue=255))
            #sphero.sensor.set_notify(notify_callback, CoreTime, Accelerometer)

            #sphero.sensor.cancel_notify_sensors()
        #sphero.sensor.cancel_notify_sensors()
        # while(sphero.sensor.get_ambient_light_sensor_value() <= 75):
        #     print("Light Sensor: {}",sphero.sensor.get_ambient_light_sensor_value(), end="\r")
        #     sphero.user_io.set_all_leds_8_bit_mask()
        # sleep(1)
        # sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(blue=55))
        # sphero.user_io.set_led_matrix_text_scrolling(string=":)",color=Color(blue=255,red=0,green=0))
        # sleep(2)
        # sphero.driving.drive_with_heading(1, 270, Direction.forward)
        # sleep(.1)
        # sphero.driving.drive_with_heading(1, 90, Direction.forward)
        # sleep(.1)
        # sphero.driving.drive_with_heading(1, 0, Direction.forward)
        # sleep(1)
        # sphero.user_io.set_led_matrix_one_color(color=Color(green=255))
        # sphero.driving.drive_with_heading(252, 5, Direction.forward)
        # sleep(3.2)
        # sphero.user_io.set_led_matrix_one_color(color=Color(red=255))
        # sphero.driving.drive_with_heading(1, 0, Direction.forward)
        # sleep(2)
        # sphero.driving.drive_with_heading(200, 180, Direction.forward)
        # sleep(2)
        # sphero.driving.drive_with_heading(200, 200, Direction.forward)
        # sleep(.5)
        # sphero.driving.drive_with_heading(200, 180, Direction.forward)
        # sleep(1.5)
        # sphero.driving.drive_with_heading(1, 180, Direction.forward)
        # sphero.driving.reset_yaw()
        # sphero.driving.drive_with_heading(75, 90, Direction.forward)
        #sphero.driving.tank_drive(right_speed=255,left_speed=255)
        #sphero.user_io.set_led_matrix_one_color(color=Color(blue=255))
        #sphero.user_io.set_led_matrix_single_character(symbol="*",color=Color(blue=255,red=255,green=255))
        #sphero.user_io.set_led_matrix_text_scrolling(string="Get pi",color=Color(blue=255,red=255,green=255))
        #sleep(5)
        #sphero.driving.raw_motor(left_speed=200,left_direction=DirectionRawMotor.reverse,right_speed=200,right_direction=DirectionRawMotor.forward)
        #sphero.driving.raw_motor(left_direction=Direction.reverse,left_speed=100,right_direction=Direction.forward,right_speed=200)
        #sphero.driving.drive_with_heading(255, 0, Direction.forward)
        sleep(40)
        sphero.power.enter_soft_sleep()


if __name__ == "__main__":
    main()
