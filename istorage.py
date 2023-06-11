from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def load_data(self, file_path):
        pass

    @abstractmethod
    def write_data(self, data):
        pass

    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title, year, rating):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        pass
