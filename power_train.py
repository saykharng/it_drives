from adafruit_servokit import ServoKit

SERVO_CHANNELS = 16

STEER_SERVO_CHANNEL = 0
THROTTLE_SERVO_CHANNEL = 1

print("Initializing power train.")

POWER_TRAIN = ServoKit(channels=SERVO_CHANNELS)

POWER_TRAIN_STEER = POWER_TRAIN.servo[STEER_SERVO_CHANNEL]

POWER_TRAIN_THROTTLE = POWER_TRAIN.continuous_servo[THROTTLE_SERVO_CHANNEL]

print("Power train ready")
