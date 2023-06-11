from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import json
import csv


def main():
    """The main function of the program.
    It prints a menu to the console and executes the corresponding function
    based on the user's input."""
    file = input("Enter file name to open or if it does not exist it will be created: ")
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
    except FileNotFoundError:
        if file.endswith(".json"):
            with open(file, "w") as new_file:
                data = {}
                json.dump(data, new_file, indent=4)
                print(f"File with name: {file}, has been created!")
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
                print(f"File with name: {file}.csv, has been created!")
            storage = StorageCsv(file)
            movie_app = MovieApp(storage)
            movie_app.run()


if __name__ == "__main__":
    main()
