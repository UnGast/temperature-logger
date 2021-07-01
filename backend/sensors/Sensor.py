class Sensor:
    def __init__(self, id, type, position, accuracy):
        self.id = id
        self.type = type
        self.position = position
        self.accuracy = accuracy
        
    def get_info(self):
        
        return {
            'id': self.id,
            'type': self.type,
            'position': self.position,
            'accuracy': self.accuracy
        }

    def read(self) -> float:
        print("READ NOT IMPLEMENTED FOR SENSOR: {} with id {} at {}".format(self.type, self.id, self.position))