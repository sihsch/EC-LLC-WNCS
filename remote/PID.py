class PID:

    def __init__(self):

        self.clear()

    def clear(self):
        self.SetPoint = 80
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.output = 0.0
        self.error = 0.0

    def update(self, feedback_value):
        #Calculates PID value for given reference feedback
        self.error = feedback_value - self.SetPoint
        delta_error = self.error - self.last_error
        self.ITerm += self.error
        # Remember last time and last error for next calculation
        self.last_error = self.error

        self.PTerm = self.error/10
        self.DTerm = delta_error
        self.output = self.PTerm + (self.ITerm/100000) + (self.DTerm * 0.65)
