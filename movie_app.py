import random
import matplotlib.pyplot as plt
from thefuzz import fuzz
from colorama import Fore, Style


class MovieApp:
    def __init__(self, storage):
        self.storage = storage

    def run(self):
        """Displays a menu of options to the user and calls the corresponding function based on their input.
        Args:
        - lst_movies: dict, a dictionary containing movies and their ratings, year, and so on."""
        print(10 * '*' + "My Movies Database" + 10 * '*')
        while True:
            print(
                f"""{Fore.LIGHTBLUE_EX}
                  Menu:
                  0. Exit
                  1. List movies
                  2. Add movie
                  3. Delete movie
                  4. Update movie
                  5. Stats
                  6. Random movie
                  7. Search movie
                  8. Movies sorted by rating
                  9. Create Rating Histogram{Style.RESET_ALL}
                  """
            )
            choice = input(f"{Fore.YELLOW}Enter choice (0-9): {Style.RESET_ALL}")
            if choice == "0":
                print("Bye")
                break
            else:
                try:
                    cmd_func = self.get_command_function(choice)
                    cmd_func()
                    input(f"\n{Fore.YELLOW}Press Enter to continue!{Style.RESET_ALL}")
                except KeyError:
                    print("\n")
                    print(f"{Fore.LIGHTRED_EX}Enter a valid value{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue!{Style.RESET_ALL}")

    def movies_list(self):
        """Prints the list of movies with their rating and year."""
        movies = self.storage.list_movies()
        if len(movies) == 0:
            print("Files is empty, add new movies!")
        for name, movie in movies.items():
            rating = movie["rating"]
            year = movie["year"]
            print(f"{name}, {rating}, {year}")

    def statistics(self):
        """Runs all statistical analysis functions on the list of movies."""
        self.average_rating()
        self.median_range()
        self.the_best_movie()
        self.the_worst_movies()

    def get_ratings(self):
        """Extracts the ratings from a dictionary of movies.
            Returns:
                list: A list of the movie ratings."""
        ratings = []
        for movie in self.storage.list_movies().values():
            try:
                rating = float(movie["rating"])
                ratings.append(rating)
            except ValueError:
                pass
        return ratings

    def average_rating(self):
        """Calculates the average rating for the list of movies."""
        lst_ratings = self.get_ratings()
        if len(lst_ratings) == 0:
            print(f"{Fore.LIGHTMAGENTA_EX}No movies in the database.{Style.RESET_ALL}")
        else:
            sum_rating = 0
            for rating in lst_ratings:
                sum_rating += rating
            average = round(sum_rating / len(lst_ratings), 2)
            print(f"{Fore.LIGHTMAGENTA_EX}The average rating for movies in the database is: {Style.RESET_ALL}{average}")

    def median_range(self):
        """Calculates the median rating for the list of movies."""
        lst_ratings = self.get_ratings()
        if len(lst_ratings) == 0:
            print(f"{Fore.LIGHTMAGENTA_EX}No movies in the database.{Style.RESET_ALL}")
        else:
            sorted_movies_rating = list(sorted(lst_ratings))
            num_movies = len(sorted_movies_rating)
            if len(lst_ratings) % 2 == 0:
                median = (sorted_movies_rating[num_movies // 2] + sorted_movies_rating[num_movies // 2 + 1]) / 2
            else:
                median = round(sorted_movies_rating[num_movies // 2], 2)
            print(f"{Fore.LIGHTBLUE_EX}Median rating is:{Style.RESET_ALL} {median}")

    def the_best_movie(self):
        """Finds the movie with the highest rating in the list of movies."""
        lst_ratings = self.get_ratings()
        if len(lst_ratings) == 0:
            print(f"{Fore.LIGHTMAGENTA_EX}No movies in the database.{Style.RESET_ALL}")
        else:
            the_best = max(lst_ratings)
            best_movies = {}
            for name, info in self.storage.list_movies().items():
                val = float(info["rating"])
                if val >= the_best:
                    the_best = val
                    best_movies[name] = val
            for key, val in best_movies.items():
                print(f"{Fore.GREEN}The best movie is: {Style.RESET_ALL}{key}: {val}")

    def the_worst_movies(self):
        """Finds the movies with the lowest ratings in the list of movies."""
        lst_ratings = self.get_ratings()
        if len(lst_ratings) == 0:
            print(f"{Fore.LIGHTMAGENTA_EX}No movies in the database.{Style.RESET_ALL}")
        else:
            the_worst = min(lst_ratings)
            the_worst_movie = {}
            for name, info in self.storage.list_movies().items():
                val = float(info["rating"])
                if val <= the_worst:
                    the_worst = val
                    the_worst_movie[name] = val
            for key, value in the_worst_movie.items():
                print(f"{Fore.MAGENTA}The worst movie is: {Style.RESET_ALL}{key}: {value}")

    def random_movie(self):
        """Selects and prints a random movie from the list of movies."""
        movies = self.storage.list_movies().items()
        if len(movies) == 0:
            print("Empty file! No movies to choose from.")
        else:
            movie, data = random.choice(list(movies))
            rating = data["rating"]
            year = data["year"]
            print(f"{Fore.LIGHTGREEN_EX}The random movie for tonight is:{Style.RESET_ALL} {movie} - {rating}"
                  f"{Fore.LIGHTGREEN_EX} rating{Style.RESET_ALL}, {year}")

    def search_movie(self):
        """Allows the user to search for a movie in the list of movies based on a keyword."""
        movies = self.storage.list_movies().items()
        if len(movies) == 0:
            print("Empty file! No movies to choose from.")
        else:
            desired_movie = input(f"{Fore.YELLOW}Enter movie name to search:{Style.RESET_ALL} ")
            not_in_the_list = True
            for movie, info in movies:
                rating = info["rating"]
                year = info["year"]
                # If movie name coincide then return straight away the result
                if movie == desired_movie:
                    print(f"{Fore.LIGHTGREEN_EX}Searched movie:{Style.RESET_ALL} {movie} {Fore.LIGHTGREEN_EX}with rating:"
                          f"{Style.RESET_ALL} {rating}, {year}")
                    not_in_the_list = False
                # If not, check in the lower_case
                elif desired_movie.lower() in movie.lower():
                    print(f"{Fore.LIGHTGREEN_EX}Possible result :{Style.RESET_ALL} {movie}, {rating}, {year}")
                    not_in_the_list = False
                # If name don't match directly, then search by fuzzy similarity
                else:
                    ratio = fuzz.partial_ratio(desired_movie, movie)
                    if ratio >= 50:
                        print(
                            f"{desired_movie} {Fore.LIGHTRED_EX}not in the list, did you meant:{Style.RESET_ALL}{movie},"
                            f" {rating}, {year}")
                        not_in_the_list = False
            if not_in_the_list:
                print(
                    f"{Fore.RED}Searched movie{Style.RESET_ALL} {desired_movie} {Fore.RED}not in the list{Style.RESET_ALL}")

    def sorting_movie(self):
        """Sorts the movies in the list of movies based on their ratings in descending order."""
        movies = self.storage.list_movies().items()
        if len(movies) == 0:
            print("No movies!")
        else:
            sorted_movies_by_rating = dict(sorted(movies, key=lambda value: float(value[1]["rating"]), reverse=True))
            print(f"{Fore.YELLOW}The sorted list of movies by rating:{Style.RESET_ALL} \n")
            for movie, info in sorted_movies_by_rating.items():
                rating = info["rating"]
                year = info["year"]
                print(f"{Fore.CYAN}{movie}: {rating}, {year}{Style.RESET_ALL}")

    def rating_histogram(self):
        """Generates and displays a histogram of the movie ratings."""
        ratings = self.get_ratings()
        if ratings:
            plt.hist(ratings, bins=range(11), rwidth=0.2, edgecolor="black", color="green")
            plt.title("Movie Rating Histogram")
            plt.xlabel("Rating")
            plt.ylabel("Frequency")
            where_to_save = input("File name and/or path to save and extension: ")
            plt.savefig(where_to_save)
            plt.show()
        else:
            print(f"{Fore.LIGHTMAGENTA_EX}No movies in the database.{Style.RESET_ALL}")

    def get_command_function(self, choice):
        """Returns the corresponding command function based on the user's input."""
        command_functions = {
            "1": self.movies_list,
            "2": self.storage.add_movie,
            "3": self.storage.delete_movie,
            "4": self.storage.update_movie,
            "5": self.statistics,
            "6": self.random_movie,
            "7": self.search_movie,
            "8": self.sorting_movie,
            "9": self.rating_histogram
        }
        return command_functions[choice]
