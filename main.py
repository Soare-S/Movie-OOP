from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
from colorama import Fore, Style
import json
import csv


def main():
    """The main function of the program.
    It prints a menu to the console and executes the corresponding function
    based on the user's input."""
    file = input(f"{Fore.LIGHTGREEN_EX}Enter file name to open or if it does not exist it will be created: {Style.RESET_ALL}")
    try:
        if file.endswith(".csv"):
            storage = StorageCsv(file)
            if not file.endswith(".json") and not file.endswith(".csv"):
                storage = StorageCsv(f'{file}.csv')
            movie_app = MovieApp(storage)
            movie_app.run()
        elif file.endswith('.json'):
            storage = StorageJson(file)
            movie_app = MovieApp(storage)
            movie_app.run()
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        if file.endswith(".json"):
            with open(file, "w") as new_file:
                data = {}
                json.dump(data, new_file, indent=4)
                print(f"{Fore.LIGHTBLUE_EX}\nNo such file in directory. File with name: {Style.RESET_ALL}{file},"
                      f" {Fore.LIGHTBLUE_EX}has been created!\n{Style.RESET_ALL}")
            storage = StorageJson(file)
            movie_app = MovieApp(storage)
            movie_app.run()
        else:
            if file.endswith(".csv"):
                file = file
            else:
                file = f"{file}.csv"
            with open(file, "w") as new_file:
                writer = csv.writer(new_file)
                writer.writerow(["title", "rating", "year", "notes"])
                print(f"{Fore.LIGHTBLUE_EX}\nNo such file in directory. File with name: {Style.RESET_ALL}{file},"
                      f" {Fore.LIGHTBLUE_EX}has been created!\n{Style.RESET_ALL}")
            storage = StorageCsv(file)
            movie_app = MovieApp(storage)
            movie_app.run()


if __name__ == "__main__":
    main()
