import random
import matplotlib.pyplot as plt


class Sensor:
    def __init__(self, minValue=30, maxValue=80, startingValue=0.4, delta=0.05):
        self.minValue = minValue
        self.maxValue = maxValue
        self.values = {"value": startingValue, "delta": delta}

    def generateValue(self):
        decider = random.random()

        if self.values["value"] <= (self.minValue/100):
            self.values['value'] += self.values['delta']
        elif self.values["value"] >= (self.maxValue/100):
            self.values['value'] -= self.values['delta']
        else:
            if decider < 0.5:
                self.values['value'] += random.uniform(self.values['delta'] / 2.5, self.values['delta'] * 2.5)
            elif decider >= 0.5:
                self.values['value'] -= random.uniform(self.values['delta'] / 2.5, self.values['delta'] * 2.5)

        return self.values["value"]

    @property
    def normalizeValue(self):
        return (self.maxValue - self.minValue) * self.generateValue() + self.minValue
