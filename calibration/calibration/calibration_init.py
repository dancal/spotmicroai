#!/home/pi/spotmicroai/venv/bin/python3 -u

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from pick import pick
import time
import os
import sys
import RPi.GPIO as GPIO

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config

log = Logger().setup_logger('CALIBRATE SERVOS')

log.info('Calibrate init position...')

pca = None

gpio_port = Config().get(Config.ABORT_CONTROLLER_GPIO_PORT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_port, GPIO.OUT)
GPIO.output(gpio_port, False)

i2c = busio.I2C(SCL, SDA)

options = {
        0: 'rear_shoulder_left      - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_PCA9685)) + ']'
                                            + ' CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_CHANNEL)) + ']'
                                            + '- ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_REST_ANGLE)) + ']'
                                            + '  MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MAX_ANGLE)) + ']',
        1: 'rear_leg_left           - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MAX_ANGLE)) + ']',
        2: 'rear_feet_left          - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MAX_ANGLE)) + ']',
        3: 'rear_shoulder_right     - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MAX_ANGLE)) + ']',
        4: 'rear_leg_right          - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_REST_ANGLE)) + ']'+ ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MAX_ANGLE)) + ']',
        5: 'rear_feet_right         - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MAX_ANGLE)) + ']',
        6: 'front_shoulder_left     - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MAX_ANGLE)) + ']',
        7: 'front_leg_left          - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MAX_ANGLE)) + ']',
        8: 'front_feet_left         - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MAX_ANGLE)) + ']',
        9: 'front_shoulder_right    - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MAX_ANGLE)) + ']',
        10: 'front_leg_right        - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_CHANNEL)) + '] - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MAX_ANGLE)) + ']',
        11: 'front_feet_right       - PCA[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_CHANNEL)) + '] - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MAX_ANGLE)) + ']',
        12: 'arm_rotation           - PCA[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_MAX_ANGLE)) + ']',
        13: 'arm_lift               - PCA[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_CHANNEL)) + ']  - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_MAX_ANGLE)) + ']',
        14: 'arm_range              - PCA[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_CHANNEL)) + '] - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_MAX_ANGLE)) + ']',
        15: 'arm_cam_tilt           - PCA[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_PCA9685)) + '] CHANNEL[' + str(Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_CHANNEL)) + '] - ANGLE[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_REST_ANGLE)) + ']' + ' MIN[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_MIN_ANGLE)) + '] MAX[' + str(Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_MAX_ANGLE)) + ']'
}

screen_options = list(options.values())

# selected_option, selected_index = pick(screen_options, title)
# PCA9685_ADDRESS, PCA9685_REFERENCE_CLOCK_SPEED, PCA9685_FREQUENCY, CHANNEL, MIN_PULSE, MAX_PULSE, REST_ANGLE = Config().get_by_section_name(selected_option.split()[0])
for i, values in enumerate(screen_options):
    # CA9685_ADDRESS, PCA9685_REFERENCE_CLOCK_SPEED, PCA9685_FREQUENCY, CHANNEL, MIN_PULSE, MAX_PULSE, REST_ANGLE = Config().get_by_section_name(values.split()[0])
    PCA9685_ADDRESS, PCA9685_REFERENCE_CLOCK_SPEED, PCA9685_FREQUENCY, CHANNEL, MIN_PULSE, MAX_PULSE, REST_ANGLE, MIN_ANGLE, MAX_ANGLE = Config().get_by_section_name(values.split()[0])

    print(PCA9685_ADDRESS);
    pca = PCA9685(i2c, address=int(PCA9685_ADDRESS, 0), reference_clock_speed=PCA9685_REFERENCE_CLOCK_SPEED)
    pca.frequency = PCA9685_FREQUENCY
    active_servo = servo.Servo(pca.channels[CHANNEL])
    active_servo.set_pulse_width_range(min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)
    active_servo.angle = int(REST_ANGLE)
    time.sleep(0.1)
    pca.deinit()

