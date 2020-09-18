from abc import ABC, abstractmethod

class DataSource(ABC):

    @abstractmethod
    def get_latest_value(self):

        pass

class MockDataSource(DataSource):

    def get_latest_value(self):

        return 1