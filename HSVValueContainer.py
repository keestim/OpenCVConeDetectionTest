from typing import NamedTuple

MIN_VALUE = 0
MAX_VALUE = 255
MAX_HUE_VALUE = 180

class HSVValueContainer:
    def __init__(self, 
                input_low_H =  MIN_VALUE, 
                input_high_H = MAX_HUE_VALUE, 
                input_low_S = MIN_VALUE, 
                input_high_S = MAX_VALUE, 
                input_low_V = MIN_VALUE,
                input_high_V = MAX_VALUE):
        self.low_H = input_low_H
        self.high_H = input_high_H
        self.low_S = input_low_S
        self.high_S = input_high_S
        self.low_V = input_low_V
        self.high_V = input_high_V

    def reset(self):
        self.low_H =  MIN_VALUE
        self.high_H = MAX_HUE_VALUE 
        self.low_S = MIN_VALUE 
        self.high_S = MAX_VALUE 
        self.low_V = MIN_VALUE
        self.high_V = MAX_VALUE

    def printValues(self):
        print("low H: " + str(self.low_H) + '\n' +
            "high H: " + str(self.high_H) + '\n' +
            "low S: " + str(self.low_S) + '\n' +
            "high S: " + str(self.high_S) + '\n' +
            "low V: " + str(self.low_V) + '\n' +
            "high V: " + str(self.high_V) + '\n')   