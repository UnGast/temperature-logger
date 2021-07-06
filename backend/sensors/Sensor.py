class Sensor:
    def __init__(self, id, type, position, accuracy, correction_offset):
        self.id = id
        self.type = type
        self.position = position
        self.accuracy = accuracy
        if isinstance(correction_offset, str):
            self.correction_offset = float(correction_offset)
        elif isinstance(correction_offset, float):
            self.correction_offset = correction_offset
        else:
            raise Exception(f"type of correction_offset value not supported: {correction_offset}")
        
    def get_info(self):
        
        return {
            'id': self.id,
            'type': self.type,
            'position': self.position,
            'accuracy': self.accuracy,
            'correction_offset': self.correction_offset
        }

    def read(self) -> float:
        print("READ NOT IMPLEMENTED FOR SENSOR: {} with id {} at {}".format(self.type, self.id, self.position))