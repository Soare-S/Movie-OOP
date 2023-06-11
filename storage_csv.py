from abc import ABC
from storage_json import IStorage
from colorama import Fore, Style
import csv


class StorageCsv(IStorage, ABC):
    def __init__(self, file_path):
        self._file_path = file_path

    def load_data(self, file_path):
        with open(self._file_path, "r") as handle:
            return handle.read()

    def write_data(self, data):
        with open(self._file_path, "w") as new_file:
            new_file.write(data)

    def list_movies(self):
        movies = {}
        with open(self._file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                movie_name = row["title"]
                movies[movie_name] = {
                    "rating": row["rating"],
                    "year": row["year"],
                    "notes": row["notes"]
                }
        return movies

    def add_movie(self, title="", year="", rating=""):
        """Adds a movie to the movies' database"""
        movies = self.list_movies()
        title = input("Enter movie title to add: ")
        if title.lower().capitalize() in movies:
            print(f"\n{Fore.YELLOW}Movie {Style.RESET_ALL}{title} {Fore.YELLOW}already exists! {Style.RESET_ALL}")
        else:
            year = input("Enter movie year: ")
            rating = input("Enter movie rating: ")
            title = title.lower().capitalize()
            with open(self._file_path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([title, rating, year])
            print(
                f"\n{Fore.YELLOW}Movie{Style.RESET_ALL} {title}{Fore.YELLOW} has been added successfully!{Style.RESET_ALL}")

    def delete_movie(self, title=""):
        movies = self.list_movies()
        title = input("Enter movie title to delete: ")
        if title.lower().capitalize() in movies:
            del movies[title]
            self._rewrite_csv_file(movies)
            print(
                f"{Fore.YELLOW}The movie{Style.RESET_ALL} {title} {Fore.YELLOW}has been successfully deleted!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The movie '{Style.RESET_ALL}{title}{Fore.RED}' is not in the list!{Style.RESET_ALL}")

    def update_movie(self, title="", notes=""):
        movies = self.list_movies()
        title = input("Enter movie title to update: ")
        if title.lower().capitalize() in movies:
            notes = input("Enter movie notes: ")
            movies[title]["notes"] = notes
            self._rewrite_csv_file(movies)
            print(f"Movie {title} updated!")
        else:
            print(f"Movie {title} not found in the list!")

    def _rewrite_csv_file(self, movies):
        """
        Rewrites the CSV file with the updated movies' data.

        Args:
        - movies: dict, the updated movies data
        """
        with open(self._file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "rating", "year", "notes"])
            for title, info in movies.items():
                writer.writerow([title, info["rating"], info["year"], info["notes"]])
