from abc import ABC, abstractmethod
import sensors

class DataSource(ABC):

    @abstractmethod
    def get_sensors(self):

        pass

    @abstractmethod
    def get_latest_values(self):

        pass

class MockDataSource(DataSource):

    def __init__(self):

        super().__init__()

        self.sensors = [
            sensors.Mock("Somewhere over the rainbow", 1),
            sensors.Mock("Somewhere over the rainbow", 1),
            sensors.Mock("Somewhere over the rainbow", 1),
            sensors.Mock("Somewhere over the rainbow", 1)
        ]

    def get_sensors(self):

        return self.sensors

    def get_latest_values(self):

        return 1