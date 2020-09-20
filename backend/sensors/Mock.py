import math
from datetime import datetime
import sensors

class Mock(sensors.Sensor):

  def __init__(self, id, position):

      super().__init__(id=id, name="Mock", position=position, accuracy=0.5)

  def last_value(self) -> { 'timestamp': int, 'value': float }:

      time = datetime.now()

      return { 'timestamp': time.timestamp(), 'value': math.sin(time.timestamp()) }