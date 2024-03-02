import RPi.GPIO as GPIO
import settings
import time
import inputs

class MotorControl:
    def __init__(self, pwm_pin, in1, in2, pin_mode=None):
        self.gpio = GPIO
        self.pwm_pin = pwm_pin
        self.in1 = in1
        self.in2 = in2
        self.pin_mode = pin_mode if pin_mode else GPIO.BOARD
        self._direction = 0 # 0 stop | 1 forward | -1 Reverse
        self.FORWARD = 1
        self.BACKWARD = -1
        self.STOP = 0
        self.stick_midpoint = settings.MAX_INPUT/2 # state value when controller is in mid point
        

    def setup(self):
        self.gpio.setmode(self.pin_mode)
        self.gpio.setup(self.pwm_pin, GPIO.OUT)
        self.pwm_object = self.gpio.PWM(self.pwm_pin, 100)

        # Initially on forward direction with in1 on high and in2 on low.
        self.gpio.setup(self.in1, GPIO.OUT, initial=GPIO.HIGH)
        self.gpio.setup(self.in2, GPIO.OUT, initial=GPIO.LOW)
        self._direction = self.FORWARD

        self.pwm_object.start(self.STOP)
        

    def _set_forward(self):
        if self._direction == self.FORWARD:
            return True
        
        self.gpio.output(self.in1, GPIO.HIGH)
        self.gpio.output(self.in2, GPIO.LOW)
        self._direction = self.FORWARD
        return True

    def _set_backward(self):
        if self._direction == self.BACKWARD:
            return True

        self.gpio.output(self.in1, GPIO.LOW)
        self.gpio.output(self.in2, GPIO.HIGH)
        self._direction = self.BACKWARD
        return True
    
    def current_direction(self):
        return self._direction

    def _stop_motor(self):
        self.pwm_object.ChangeDutyCycle(self.STOP)

    def _compute_duty_cycle(self, input_value):
        duty_cycle = 0

        if self._direction == self.FORWARD:
            duty_cycle = (1 - (input_value / self.stick_midpoint)) * 100
        
        if self._direction == self.BACKWARD:
            duty_cycle  = self.stick_midpoint/100 * (input_value - self.stick_midpoint)

        return min(max(duty_cycle, 0.0), 100)

    def initialize(self):
        while True:
            events = inputs.get_gamepad()
            if events:
                for event in events:
                    if event.code == settings.GAME_PAD_ACC_CODE:
                        if event.state > self.stick_midpoint:
                            self._set_backward()
                        elif event.state < self.stick_midpoint:
                            self._set_forward()
                        else:
                            self.pwm_object.ChangeDutyCycle(self.STOP)

                        if self._direction != self.STOP:
                            duty_cycle = self._compute_duty_cycle(event.state)
                            self.pwm_object.ChangeDutyCycle(duty_cycle)
            else:
                self.pwm_object.ChangeDutyCycle(self.STOP)

MOTOR = MotorControl(settings.PWM_PIN, settings.IN1_PIN, settings.IN2_PIN)

if __name__ == "__main__":
    motor.setup()
    motor.run_motor()
