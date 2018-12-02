#!/usr/bin/python

__all__ = ["move_switch_row"]

from utils.hat_motors import Adafruit_MotorHAT

import atexit

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def move_switch_row(number_of_switches, direction):

    if direction.lower() == "down":
        stepper_motor.step(150 * number_of_switches * 4, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)

    if direction.lower() == "up":
        stepper_motor.step(150 * number_of_switches * 4, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)


# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

atexit.register(turnOffMotors)

stepper_motor = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
stepper_motor.setSpeed(45)