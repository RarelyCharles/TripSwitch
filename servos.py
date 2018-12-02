#!/usr/bin/python

# TODO: Need license info for Adafruit PWM driver
# Directly pulled from Adafruit

from utils.pwm import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x41)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
servoMid = 375

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

servos = {"left": {"channel": 0, "on": servoMax, "off": servoMin, "neutral": servoMid},
          "right": {"channel": 7, "on": servoMin, "off": servoMax, "neutral": servoMid}}

# Channel 4 is left
def flip_switch(side, state):
    """Flips the desired side switch to the desired state of on|off"""
    pwm.setPWM(servos[side.lower()]["channel"], 0, servos[side.lower()][state.lower()])
    time.sleep(1)
    pwm.setPWM(servos[side.lower()]["channel"], 0, servos[side.lower()]["neutral"])

