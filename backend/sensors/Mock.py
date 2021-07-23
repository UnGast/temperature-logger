import math
import time
import sensors

class Mock(sensors.Sensor):
  def __init__(self, id, position, amplitude, mean, period, correction_offset):
        super().__init__(id=id, type="Mock", position=position, accuracy=0.5, correction_offset=correction_offset)
        self.amplitude = amplitude
        self.mean = mean
        self.period = period

  def __read__(self) -> float:
        value = self.amplitude * math.sin((time.time() % self.period) / self.period * 2 * 3.1415926535) + self.mean
        return value
