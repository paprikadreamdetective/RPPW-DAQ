import RPi.GPIO as GPIO
import time

MANUAL = 0
TIMER = 1
PID = 2
ONOFF = 3

class Output:
    def __init__(self, channel, pin, output_type, control_mode, value):
        self.channel = channel
        self.pin = pin
        self.output_type = output_type
        self.control_mode = control_mode
        self.manual_value = value
        self.value = 0
        
        # private:
        self._adc_input = 0
        self._time_on = 1
        self._time_off = 2
        self._delta_time = 0
        self._current_timer = 2
        self._is_on = False
        
        self._input_value = 0
        self._input_value_lb = 0
        self._input_value_ub = 1

        # PID
        self._setpoint = 0
        self._alpha = 0.01
        self._filtered_input = 0.0
        self._sample_time_us = 2500000 
        self._sample_time_s = 0.25
        self._kp = 0.0
        self._ki = 0.0
        self._kd = 0.0
        self._integral_sum = 0.0
        self._last_error = 0.0
        self._last_time = 0.0
        self._output_min = 0
        self._output_max = 255
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setwarnings(False)
        self.pwm = GPIO.PWM(self.pin, 100)  # PWM at 1kHz
        self.pwm.start(0)
        
    #def write_output(self):
    def write_output(self, input_analog):
        if self.control_mode == MANUAL:
            self.value = self.manual_value
            #print("Value: " + str(self.value))
        elif self.control_mode == TIMER:
            self._delta_time += 1
            if self._delta_time > self._current_timer:
                #self._is_on = not self._is_on
                #self._delta_time = 0
                if self._is_on:
                    self._is_on = False
                else:
                    self._is_on = True
                self._delta_time = 0

            if self._is_on:
                self._current_timer = self._time_on
                self.value = self.manual_value
            else:
                self._current_timer = self._time_off
                self.value = 0
        
        elif self.control_mode == PID:
            #self._filtered_input = self._alpha * self._input_value + (1 - self._alpha) * self._filtered_input
            self._filtered_input = self._alpha * input_analog + (1 - self._alpha) * self._filtered_input
            self.value = self.compute_pid(self._filtered_input)

        elif self.control_mode == ONOFF:
                #if self._input_value < self._input_value_lb:
                analog_value = input_analog

                if int(input_analog) > self._input_value_ub:
                #if int(analog_value) > self._input_value_ub:
                        self.value = self.manual_value
                elif self._input_value > self._input_value_ub:
                #elif int(analog_value) < self._input_value_ub:
                        self.value = 0
        #for i in range(100, -1, -1):
        self.pwm.ChangeDutyCycle(self.map_value(self.value, 0, 255, 0, 100))
            #time.sleep(0.01)
        #for i in range(100, -1, -1):
        #self.pwm.ChangeDutyCycle(self.value)
            #time.sleep(0.01)
            
            
    def map_value(self, input_value, in_min, in_max, out_min, out_max):
        return (int(input_value) - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def set_adc_input_channel(self, input_channel):
        self._adc_input = input_channel

    def set_manual_output(self, value):
        # self.control_mode = self.MANUAL
        self.control_mode = 0
        self.manual_value = value
    
    def set_timer(self, time_on, time_off, value):
        #self.control_mode = self.TIMER
        self.control_mode = 1   
        self._time_on = time_on
        self._time_off = time_off
        self.manual_value = value
        self._delta_time = 0
        self._current_timer = self._time_on
        self._is_on = True

    def set_pid(self, input_value, setpoint):
        #self.control_mode = self.PID
        self.control_mode = 2
        self._input_value = input_value
        self._setpoint = setpoint

    def set_onoff(self, input_value, lb, ub, value):
        self.control_mode = 3
        self._input_value = input_value
        self._input_value_lb = lb
        self._input_value_ub = ub
        self.manual_value = value
    
    def compute_pid(self, input_value):
        now = time.time()
        time_change = now - self._last_time

        error = self._setpoint - input_value
        d_error = error - self._last_error
        # d_error = (error - self._last_error) / time_change

        p_term = self._kp * error
        #i_term = self._ki * error * time_change
        i_term = self._ki * error 
        d_term = self._kd * d_error

        self._integral_sum += i_term
        self._integral_sum = max(min(self._integral_sum, self._output_max), self._output_min)
        output = max(min(self._integral_sum + p_term + d_term, self._output_max), self._output_min)

        self._last_error = error
        self._last_time = now

        return output
    
    def set_sample_time_us(self, sample_time_us):
        self._sample_time_us = sample_time_us
        self._sample_time_s = float(sample_time_us / 1000000.0)

    def set_gh_filter(self, alpha):
        self._alpha = alpha

    def set_pid_tunings(self, Kp, Ki, Kd):
        self._kp = Kp
        self._ki = Ki * self._sample_time_s
        self._kd = Kd / self._sample_time_s

    def set_output_limits(self, min_val, max_val):
        self._output_min = min_val
        self._output_max = max_val

    def initialize_pid(self):
        self._last_time = time.time() - self._sample_time_us / 1000000.0
        self._last_error = 0
        self._integral_sum = 0
        self._filtered_input = self._input_value
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
    
