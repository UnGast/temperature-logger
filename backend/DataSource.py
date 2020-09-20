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
            sensors.Mock(1, "Somewhere over the rainbow"),
            sensors.Mock(2, "Somewhere over the rainbow"),
            sensors.Mock(3, "Somewhere over the rainbow"),
            sensors.Mock(4, "Somewhere over the rainbow")
        ]

    def get_sensors(self):

        return self.sensors

    def get_latest_values(self):

        return dict([(s.id, s.last_value()) for s in self.sensors])