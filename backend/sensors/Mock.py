import math
from datetime import datetime
import sensors

class Mock(sensors.Sensor):

  def __init__(self, id, position):

      super().__init__(id=id, type="Mock", position=position, accuracy=0.5)

  def last_value(self) -> float:

      time = datetime.now()

      value = round(math.sin(time.timestamp() * 0.001 + self.id) * (20 + self.id * 2), 1)

      return value