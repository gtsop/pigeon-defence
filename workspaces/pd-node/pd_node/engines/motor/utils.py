import time

try:
    import RPi.GPIO as GPIO

    GPIO.set(GPIO.BOARD)

    # Setup horizontal servo
    h_pin = 33
    GPIO.setup(h_pin, GPIO.OUT)
    h_servo = GPIO.PWM(h_pin, 50)
    h_servo.start(0)

    # Setup horizontal servo
    v_pin = 33
    GPIO.setup(v_pin, GPIO.OUT)
    v_servo = GPIO.PWM(v_pin, 50)
    v_servo.start(0)

    def _servo_move(servo, duty):
        servo.ChangeDutyCycle(duty)
        time.sleep(0.02)
        servo.ChangeDutyCycle(0)

    def move(direction):
        if direction == "left":
            _servo_move(h_servo, 7)
        elif direction == "right":
            _servo_move(h_servo, 7.9)
        if direction == "up":
            _servo_move(v_servo, 7)
        if direction == "down":
            _servo_move(v_servo, 7.9)

    def set_angle(angle: float):
        angle = max(0, min(100, angle))
        duty = MIN_DUTY + (angle / 100.0) * (MAX_DUTY - MIN_DUTY)

        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)

except Exception as e:
    print("[motor_thread]: Failed to init RPi.GPIO", e)

    def set_angle(angle: float):
        print(f"[motor_thread]: Setting angle {angle}")

    def move(direction):
        print(f"[motor_thread]: moving {direction}")

