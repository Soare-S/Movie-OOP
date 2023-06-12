from istorage import IStorage
from colorama import Fore, Style
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initializes the StorageJson object.
        Args:
            file_path (str): The path of the JSON file.
        """
        self._file_path = file_path

    def load_data(self, file_path):
        """
       Loads data from the JSON file.
       Args:
           file_path (str): The path of the JSON file.
       Returns:
           dict: The data loaded from the JSON file.
       """
        with open(self._file_path, "r") as handle:
            return json.load(handle)

    def write_data(self, data):
        """
        Writes data to a JSON file.
        Args:
            data (dict): The data to be written to the JSON file.
        """
        with open(self._file_path, "w") as new_file:
            json.dump(data, new_file, indent=4)

    def list_movies(self):
        """
        Retrieves the movies' information from the JSON file.
        Returns:
            dict: A dictionary containing the movies' information.
                The keys are the movie titles, and the values are dictionaries
                with keys 'rating', 'year', and 'notes'.
        """
        return self.load_data(self._file_path)

    def add_movie(self, title, year, rating):
        """
        Adds a movie to the movies' database.
        Args:
            title (str): The title of the movie.
            year (str): The year of the movie.
            rating (str): The rating of the movie.
        """
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
        """
        Deletes a movie from the movies' database.
        Args:
            title (str): The title of the movie to delete.
        """
        lst_movies = self.load_data(self._file_path)
        if title in lst_movies.keys():
            del lst_movies[title]
            self.write_data(lst_movies)
            print(
                f"{Fore.YELLOW}The movie{Style.RESET_ALL} {title} {Fore.YELLOW}has been successfully deleted!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The movie '{Style.RESET_ALL}{title}{Fore.RED}' is not in the list!{Style.RESET_ALL}")

    def update_movie(self, title, notes):
        """
        Updates a movie's notes in the movies' database.
        Args:
            title (str): The title of the movie to update.
            notes (str): The updated notes for the movie.
        """
        lst_movies = self.load_data(self._file_path)
        if title in lst_movies.keys():
            lst_movies[title]["notes"] = notes
            self.write_data(lst_movies)
            print(f"{Fore.YELLOW}Movie{Style.RESET_ALL} {title} {Fore.YELLOW}has been updated.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The movie '{Style.RESET_ALL}{title}{Fore.RED}' is not in the list{Style.RESET_ALL}!")
