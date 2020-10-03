class Sensor:
    
    def __init__(self, id, type, position, accuracy):
        
        self.id = id

        self.type = type

        self.position = position

        self.accuracy = accuracy

    def read(self) -> float:

        print("READ NOT IMPLEMENTED FOR SENSOR: {} with id {} at {}".format(self.type, self.id, self.position))