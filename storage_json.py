from istorage import IStorage
from colorama import Fore, Style
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path

    def load_data(self, file_path):
        with open(self._file_path, "r") as handle:
            return json.load(handle)

    def write_data(self, data):
        """Writes data to a JSON file"""
        with open(self._file_path, "w") as new_file:
            json.dump(data, new_file, indent=4)

    def list_movies(self):
        return self.load_data(self._file_path)

    def add_movie(self, title, year, rating):
        """Adds a movie to the movies' database"""
        lst_movies = self.load_data(self._file_path)
        movie_info = {
            "rating": rating,
            "year": year,
            "notes": ""
        }
        if title in lst_movies.keys():
            print(f"\n{Fore.YELLOW}Movie {Style.RESET_ALL}{title} {Fore.YELLOW}already exists! {Style.RESET_ALL}")
        else:
            lst_movies[title] = movie_info
            self.write_data(lst_movies)
            print(
                f"\n{Fore.YELLOW}Movie{Style.RESET_ALL} {title}{Fore.YELLOW} has been added successfully!{Style.RESET_ALL}")

    def delete_movie(self, title):
        """Deletes a movie from the movies' database"""
        lst_movies = self.load_data(self._file_path)
        if title in lst_movies.keys():
            del lst_movies[title]
            self.write_data(lst_movies)
            print(
                f"{Fore.YELLOW}The movie{Style.RESET_ALL} {title} {Fore.YELLOW}has been successfully deleted!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The movie '{Style.RESET_ALL}{title}{Fore.RED}' is not in the list!{Style.RESET_ALL}")

    def update_movie(self, title, notes):
        """Updates a movie's notes in the movies' database"""
        lst_movies = self.load_data(self._file_path)
        if title in lst_movies.keys():
            lst_movies[title]["notes"] = notes
            self.write_data(lst_movies)
            print(f"{Fore.YELLOW}Movie{Style.RESET_ALL} {title} {Fore.YELLOW}has been updated.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The movie '{Style.RESET_ALL}{title}{Fore.RED}' is not in the list{Style.RESET_ALL}!")
