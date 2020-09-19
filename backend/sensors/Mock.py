import sensors

class Mock(sensors.Sensor):

  def __init__(self, id, position):

      super().__init__(id=id, name="Mock", position=position, accuracy=0.5)

  def read(self):

      return 20