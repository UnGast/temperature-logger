class Sensor:
    
    def __init__(self, id, name, position, accuracy):
        
        self.id = id

        self.name = name

        self.position = position

        self.accuracy = accuracy

    def read(self):

        print("READ NOT IMPLEMENTED FOR SENSOR: {} with id {} at {}".format(self.name, self.id, self.position))