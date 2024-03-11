import settings

import inputs
from adafruit_servokit import ServoKit


class SteeringControl:
    game_pad_max_signal = 255
    servo_max_angle = 180

    def __init__(self, max_input, max_output, min_input=0, min_output=0, game_pad_control=None):
        self.pca9685 = ServoKit(channels=16)
        self.steer_servo_obj = self.pca9685.servo[0]
        self.min_input = min_input
        self.max_input = max_input

        self.min_output = min_output
        self.max_output = max_output
    
        self.signal_to_servo_ratio = self.max_input / self.max_output

        self.game_pad_control = game_pad_control if game_pad_control else settings.GAME_PAD_STEER_CODE

    def control(self):
        while True:
            events = inputs.get_gamepad()
            if events:
                for event in events:
                    #print(f'{event.code} {self.game_pad_control}')
                    if event.code == self.game_pad_control:
                        steer_angle = max(self.min_input, min(self.max_input, event.state / self.signal_to_servo_ratio))
                        self.steer_servo_obj.angle = steer_angle

STEER = SteeringControl(settings.MAX_INPUT, settings.MAX_OUTPUT)

if __name__ == "__main__":
    STEER.control()
