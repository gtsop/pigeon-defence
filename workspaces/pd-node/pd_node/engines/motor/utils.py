import time

try:
    import RPi.GPIO as GPIO

    PIN = 37

    MIN_DUTY = 1.8
    MAX_DUTY = 13.05

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)

    pwm = GPIO.PWM(PIN, 50)
    pwm.start(0)

    def set_angle(angle: float):
        angle = max(0, min(100, angle))
        duty = MIN_DUTY + (angle / 100.0) * (MAX_DUTY - MIN_DUTY)

        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)

except Exception as e:
    def set_angle(angle: float):
        print(f"[motor_thread]: Setting angle {angle}")



