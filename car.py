from steering_control import STEER
from motor_control import MOTOR

import threading

def power_train():
    steer_thread = threading.Thread(target=STEER.control, args=[])
    #MOTOR.setup()

    steer_thread.start()
    motor_thread = threading.Thread(target=MOTOR.initialize, args=[])
    

power_train()
