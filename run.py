# IMPORT CSV MODULE
import csv
import textwrap

# COLOUR ESCAPE SEQ
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BG_BLUE = "\033[44m"
BG_GREEN = "\033[42m"
RESET = "\033[0m"

DATASET = "movie_data.tsv"  # FILE PATH FOR IMDB DATASET
all_movies = []  # LIST FOR ALL MOVIES
top_100 = []  # LIST FOR TOP 100 MOVIES

# LIST HEADER FORMATTING
list_headers = (BG_GREEN
                + (
                    f'{"#":<8}'
                    f'{"Title":<45}'
                    f'{"Year":<6}'
                    f'{"Mins":<6}'
                    f'{"/10":<6}'
                    f'{"Votes":>7}'
                   )
                + RESET)


class Movies:
    def __init__(self, top_100, all_movies):
        """
        Represents collection of all movies.

        Args:
            top_100 (list): Top 100 movies list
            all_movies (list): List of all 1000 movies
        """
        self.top_100 = top_100
        self.all_movies = all_movies
        self.favourites = []
        self.watchlist = []

    def print_movies(self, movies_list):
        """
        Prints movies in list format.

        Args:
            movies_list (list): List of movies passed to function for printing
        """
        movies = movies_list.copy()
        print(list_headers)
        for index, movie in enumerate(movies_list, start=1):
            movie.index = index
            print(BG_BLUE + f"{movie}" + RESET)
        print(list_headers)


# MOVIE CLASS
class Movie:
    def __init__(self, index, title, date, runtime, genres, rating, votes):

        """
        Represents a movie.

        Attributes:
            index (int): The index to show in the printed list.
            title (str): The movie title.
            date (str): The release year of the movie.
            runtime (str): The duration of the movie in minutes.
            genres (list): The genres of the movie.
            rating (str): The average rating of the movie.
            votes (str): The number of votes received by the movie.
        """

        self.index = index  # INDEX TO SHOW IN PRINTED LIST
        self.title = title  # MOVIE TITLE
        self.date = date  # RELEASE DATE
        self.runtime = runtime  # MOVIE RUNTIME
        self.genres = genres  # GENRES
        self.rating = rating  # RATING
        self.votes = votes  # NUM VOTES

    def __str__(self):

        """
        Returns:
            str: The formatted string representation of the movie.
        """

        # PRINT FORMAT FOR MOVIES
        return (
            f'{self.index:<8}'
            f'{textwrap.shorten(self.title, width=40, placeholder="..."):<45}'
            f'{self.date:<6}'
            f'{self.runtime:<6}'
            f'{self.rating:<6}'
            f'{self.votes:>7}'
            )


# CLEAR TERMINAL SCREEN
def clear_screen():

    """
    Call to clear screen after user action.
    """

    print("\033c")


# GETS DATA FROM IMDB DATASET AND STORES IN LIST
def get_movies():

    """
    Reads tsv dataset and creates a Movie object for each instance.

    Returns:
        list: List of all movies in dataset.
    """

    with open(DATASET, "r", encoding="utf-8") as f:
        tsv_f = csv.DictReader(f, delimiter="\t")
        global all_movies
        for index, row in enumerate(tsv_f, start=1):
            title = row["primaryTitle"]
            date = row["startYear"]
            runtime = row["runtimeMinutes"]
            # CONVERT GENRE STRING TO LIST OF STRINGS
            genres = row["genres"].split(",")
            rating = row["averageRating"]
            votes = row["numVotes"]
            movie = Movie(index, title, date, runtime, genres, rating, votes)
            all_movies.append(movie)
        return all_movies


# SHOWS MOVIE LIST
def show_movies():

    """
    Prints all 1000 movies from get_movies to terminal.
    """

    clear_screen()
    movies.print_movies(all_movies)
    select_user_action()


# HOME MENU FOR USER SELECTION
def home_menu():

    """
    Prints home menu to terminal.
    """

    clear_screen()
    print(GREEN + "\nPlease select an option from the menu below:")
    print("1 - Show all movies")
    print("2 - Show favourites")
    print("3 - Show watched")
    print("4 - Show top 100")
    print("5 - Browse movies" + RESET)
    get_selection()


# REGISTER USERS MENU SELECTION
def get_selection():

    """
    Prompt user to choose option from home_menu and take
    appropriate action.
    """

    while True:
        try:
            selection = int(
                input(YELLOW
                      + "\nPlease enter a number from the menu: "
                      + RESET)
            )
        except ValueError:
            print(RED
                  + "\nInvalid choice; please choose a valid option"
                  + RESET)
        else:
            if selection == 1:
                show_movies()
            elif selection == 2:
                show_custom_list(custom_list=movies.favourites,
                                 list_name_string="favourites")
            elif selection == 3:
                show_custom_list(custom_list=movies.watchlist,
                                 list_name_string="watch list")
            elif selection == 4:
                show_top_100()
            elif selection == 5:
                browse_movies()
            else:
                print(RED
                      + "\nInvalid choice; please choose a valid option"
                      + RESET)
                continue


# PROMPT USER ACTION ON MOVIES LIST
def select_user_action(genre_results=None,
                       top_100=None,
                       search_results=None):

    """
    Prompt user to select an option from menu and take appropriate action.

    Args:
        genre_results: Passed if user is currently
        browsing movies by genre
        top_100: Passed if user is currently viewing
        Top 100 movies
        search_results: Passed if user is currently viewing
        search results
    """
    action = None
    while action not in range(0, 3):
        try:
            action = int(
                input(
                    GREEN
                    + '\nSelect from the following:\n'
                    '1 - Add a favourite\n'
                    '2 - Add to watched\n'
                    '0 - Exit to menu\n'
                    + RESET
                )
            )
            if action not in range(0, 3):
                raise ValueError

        except ValueError:
            print(RED
                  + "\nInvalid choice; please choose a valid option"
                  + RESET)

        else:
            # IF EXIT CHOSEN
            if action == 0:
                home_menu()

            # IF FAVOURITE CHOSEN
            elif action == 1:
                add_to_custom_list(
                    genre_results,
                    top_100,
                    search_results,
                    custom_list=movies.favourites,
                    list_name_string="favourites",
                )

            # IF WATCH LIST CHOSEN
            elif action == 2:
                add_to_custom_list(
                    genre_results,
                    top_100,
                    search_results,
                    custom_list=movies.watchlist,
                    list_name_string="watch list",
                )


# SHOW WATCH/FAV LIST
def show_custom_list(removed=None,
                     custom_list=None,
                     list_name_string=None):

    """
    Shows specified custom list to user - either
    favourites or watch list, depending on context

    Args:
        removed: Used to store Movie removed
        from custom list, if applicable
        custom_list: Specifies which list to use -
        favourites or watch list
        list_name_string: Used for printing list name
        in context to terminal ('favourites' or 'watch list')
    """

    clear_screen()

    # IF LIST EMPTY, SHOW MESSAGE
    if len(custom_list) == 0 or len(custom_list) is None:
        print(list_headers)
        print(RED + f"{list_name_string} empty" + RESET)
        print(list_headers)
        print(GREEN + "\nPlease select an option from the menu below:")
        print("0 - Exit to main menu" + RESET)
        while True:
            try:
                selection = int(
                    input(YELLOW
                        + "\nPlease enter a number from the menu: "
                        + RESET)
                )
            except ValueError:
                print(RED
                    + "\nInvalid choice; please choose a valid option"
                    + RESET)
            else:
                if selection == 0:
                    home_menu()
                else:
                    print(RED
                        + "\nInvalid choice; please choose a valid option"
                        + RESET)
                    continue

        # ELSE PRINT LIST OF MOVIES
    else:
        movies.print_movies(custom_list)

        # PRINTS REMOVED MOVIE IF APPLICABLE
        if removed:
            print(RED
                + f"\n{removed.title} removed from {list_name_string}"
                + RESET)

        # SHOW OPTIONS MENU
        print(GREEN + "\nPlease select an option from the menu below:")
        print(f"1 - Remove from {list_name_string}")
        print("0 - Exit to main menu" + RESET)

        while True:
            try:
                selection = int(
                    input(YELLOW
                        + "\nPlease enter a number from the menu: "
                        + RESET)
                )
            except ValueError:
                print(RED
                    + "\nInvalid choice; please choose a valid option"
                    + RESET)
            else:
                if selection == 1:
                    remove_from_custom_list(
                        custom_list=custom_list,
                        list_name_string=list_name_string
                    )
                elif selection == 0:
                    home_menu()
                else:
                    print(RED
                        + "\nInvalid choice; please choose a valid option"
                        + RESET)
                    continue


# FOR USER TO ADD A MOVIE TO LIST
def add_to_custom_list(
    genre_results=None,
    top_100=None,
    search_results=None,
    custom_list=None,
    list_name_string=None,
):

    """
    Adds user-selected movie to custom list. Ensures that correct
    list of movies is referenced depending on context.

    Args:
        genre_results: Passed if user is currently
        browsing movies by genre
        top_100: Passed if user is currently viewing
        Top 100 movies
        search_results: Passed if user is currently viewing
        search results
        custom_list: Specifies which list to use -
        favourites or watch list
        list_name_string: Used for printing list name
        in context to terminal ('favourites' or 'watch list')

    Raises:
        TypeError: Movie already in custom list
        ValueError, IndexError: Incorrect value entered
        or value not in list of movies

    Returns:
        custom_list: List of movies in the custom list
    """

    # CHECK WHERE USER IS COMING FROM TO GET CORRECT MOVIE LIST
    if top_100:
        movies = top_100
    elif genre_results:
        movies = genre_results
    elif search_results:
        movies = search_results
    else:
        global all_movies
        movies = all_movies

    add_movie = None
    while add_movie is None:
        try:
            # ENTER # OF MOVIE
            add_movie = (
                int(
                    input(
                        YELLOW
                        + (f'\nType the ID of the movie and press '
                            f'enter to add to '
                            f'{list_name_string}: ')
                        + RESET
                    )
                )
                - 1
            )

            # CHECK IF MOVIE ALREADY IN LIST
            if movies[add_movie].title not in [movie.title
                                               for movie
                                               in custom_list]:
                # ADD CHOICE TO LIST
                custom_list.append(movies[add_movie])
                print(
                    GREEN
                    + f'\n{movies[add_movie].title} added to '
                    f'{list_name_string}'
                    + RESET
                )

            else:
                raise TypeError

        # ERROR FOR INVALID CHOICE
        except (ValueError, IndexError):
            print(RED
                  + "\nInvalid choice; please choose a valid option"
                  + RESET)
            add_movie = None

        # ERROR IF ALREADY IN LIST
        except TypeError:
            print(
                RED
                + f'\n{movies[add_movie].title} already in '
                f'{list_name_string}'
                + RESET
            )

    user_continue = None
    while user_continue not in ["y", "n", "Y", "N"]:

        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(
            YELLOW
            + f'\nDo you want to add another movie to '
            f' {list_name_string}? (Y/N) '
            + RESET
        )

        # IF YES - ASK AGAIN
        if user_continue.lower() == "y":
            add_to_custom_list(
                movies,
                custom_list=custom_list,
                list_name_string=list_name_string
            )

        # IF NO - QUIT
        elif user_continue.lower() == "n":
            home_menu()

        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED
                  + "\nInvalid choice; please choose a valid option (Y/N)"
                  + RESET)

    return custom_list


# REMOVE FROM WATCH/FAV LIST
def remove_from_custom_list(custom_list=None, list_name_string=None):

    """
    Removes user-selected movie from custom list.

    Args:
        custom_list: Specifies which list to use -
        favourites or watch list
        list_name_string: Used for printing list name
        in context to terminal ('favourites' or 'watch list')
    """

    selection = None
    while selection is None:
        try:
            selection = (
                int(
                    input(
                        YELLOW
                        + (f'\nType the ID of the movie and press '
                            f'enter to remove from '
                           f'{list_name_string}: ')
                        + RESET
                    )
                )
                - 1
            )

            # REMOVE SELECTED MOVIE FROM LIST
            removed = custom_list.pop(selection)
        except (ValueError, IndexError):
            print(RED
                  + "\nInvalid choice; please choose a valid option"
                  + RESET)
            selection = None

        else:
            # SHOW FEEDBACK MSG
            print(GREEN
                  + f"\n{removed.title} removed from {list_name_string}\n"
                  + RESET)

            # SHOW UPDATED LIST
            show_custom_list(
                removed,
                custom_list=custom_list,
                list_name_string=list_name_string
            )


# CREATE TOP 100 MOVIES LIST
def create_top_100():

    """
    Runs on initialisation.
    Creates list of Top 100 movies based on number of votes.

    Returns:
        top_100: List of Top 100 rated movies
    """
    global top_100
    global all_movies
    movies = all_movies.copy()  # GET ALL MOVIES

    # SORT BY NUM VOTES
    sorted_by_votes = sorted(movies,
                             key=lambda movie: int(movie.votes),
                             reverse=True)

    # GET ONLY TOP 100 WITH MOST VOTES
    top_100 = sorted_by_votes[:100]

    # SORT MOST VOTED MOVIES BY RATING
    top_100 = sorted(top_100,
                     key=lambda movie: float(movie.rating),
                     reverse=True)


# SHOWS TOP 100 LIST OF MOVIES
def show_top_100():

    """
    Prints list of Top 100 to terminal.
    """

    clear_screen()
    movies.print_movies(top_100)
    select_user_action(top_100)


# BROWSE ALL MOVIES
def browse_movies():

    """
    Shows menu of options to user to choose browsing method
    """

    clear_screen()
    action = None
    while action not in ["0", "1", "2", "3"]:
        print(
            GREEN
            + "\nSelect from the following:\n"
            "1 - Search movies\n"
            "2 - Browse by genre\n"
            "3 - Browse by year\n"
            "0 - Exit to menu"
            + RESET
            + "\n"
        )
        action = input(
            YELLOW
            + "Please enter a number from the menu: "
            + RESET
            )
        if action == "1":
            browse_movies_search()
        elif action == "2":
            browse_movies_genre()
        elif action == "3":
            browse_movies_year()
        elif action == "0":
            home_menu()
        else:
            print(
                RED
                + "\nInvalid choice; please choose a valid option"
                + RESET
                )


# SEARCH MOVIES BY TITLE
def browse_movies_search():

    """
    Shows list of movies with title containing a user's
    search query
    """

    clear_screen()
    query = input(
        YELLOW
        + "Enter a search query: "
        + RESET
        )
    search_results = []
    for movie in movies.all_movies:
        if query.lower() in movie.title.lower():
            search_results.append(movie)
        else:
            pass
    if len(search_results) == 0:
        print(RED + "No matches found" + RESET)

    else:
        movies.print_movies(search_results)

    user_continue = None
    while user_continue not in ["y", "n", "Y", "N"]:
        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(
            YELLOW
            + "\nDo you want to enter another search query? (Y/N) "
            + RESET
        )

        # IF YES - ASK AGAIN
        if user_continue.lower() == "y":
            browse_movies_search()

        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == "n":
            if len(search_results) > 0:
                select_user_action(search_results)
            else:
                home_menu()

        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(
                RED
                + "\nInvalid choice; please choose a valid option (Y/N)"
                + RESET
                )


# BROWSE MOVIES BY GENRE
def browse_movies_genre():

    """
    Prints a list of genres for user to select from.
    """

    clear_screen()
    genres = get_genres()  # GET LIST OF GENRES
    print(GREEN + "\nSelect from the following: " + RESET)

    # PRINT LIST OF GENRES TO CHOOSE
    for index, genre in enumerate(genres, start=1):
        print(BG_BLUE + f"{index:<2} - {genre:<15}" + RESET)

    genre_index = None
    while genre_index is None:
        try:
            # GET USER GENRE CHOICE
            genre_index = (
                int(input(
                    YELLOW
                    + "\nSelect a genre from the list: "
                    + RESET)) - 1
            )
            genre_choice = genres[genre_index]

        except (IndexError, ValueError):
            print(
                RED
                + "\nInvalid choice; please choose a valid option"
                + RESET)
            genre_index = None

        else:
            clear_screen()
            genre_results = create_genre_results(movies, genre_choice)

    user_continue = None
    while user_continue not in ["y", "n", "Y", "N"]:

        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(
            YELLOW
            + "\nDo you want to choose a different genre? (Y/N) "
            + RESET
        )

        # IF YES - ASK AGAIN
        if user_continue.lower() == "y":
            browse_movies_genre()

        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == "n":
            select_user_action(genre_results)

        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(
                RED
                + "\nInvalid choice; please choose a valid option (Y/N)"
                + RESET
                  )


# CREATE GENRE SEARCH RESULTS MOVIE LIST
def create_genre_results(movies, genre_choice):

    """
    Creates list of movies containing user-selected genre.

    Returns:
        list: List of movies to print to screen.
    """
    search_results = []

    # ITERATE THROUGH ALL MOVIES
    for movie in movies.all_movies:

        # IF USERS GENRE MATCHES MOVIE, PRINT MOVIE
        if genre_choice in movie.genres:
            search_results.append(movie)
            movie.index = len(search_results)
    movies.print_movies(search_results)
    return search_results


# TO DEFINE LIST OF GENRES
def get_genres():

    """
    Iterates through all movies in IMDB list and creates a list of
    unique genres to print on screen for user to select from.

    Returns:
        list: List of unique genres in entire dataset
    """

    genres_array = []  # ARRAY TO STORE GENRES

    # ITERATE THROUGH ALL MOVIES, ADD GENRES TO ARRAY
    for movie in movies.all_movies:
        for genre in movie.genres:

            # IF GENRE ALREADY IN ARRAY, SKIP
            if genre in genres_array:
                continue

            # ADD TO GENRES ARAY
            genres_array.append(genre)
    return genres_array


def browse_movies_year():

    """
    Shows list of movies based on user-selected release year.

    Raises:
        ValueError: Year entered outside of accepted range.
    """
    search_results = []
    query = None
    while query is None:
        try:
            query = input(YELLOW
                          + "\nEnter a year from 2000 - 2023: "
                          + RESET)
            if 2000 > int(query) or int(query) > 2023:
                query = None
                raise ValueError

        except ValueError:
            print(
                RED
                + "\nInvalid choice; please enter a year from 2000 - 2023"
                + RESET
            )
            query = None

    for movie in movies.all_movies:
        if query in movie.date:
            search_results.append(movie)
            movie.index = len(search_results)
        else:
            pass

    movies.print_movies(search_results)

    # PROMPT USER FOR Y/N TO CONTINUE
    user_continue = None
    while user_continue not in ["y", "n", "Y", "N"]:
        user_continue = input(
            YELLOW
            + "\nDo you want to choose a different year? (Y/N) "
            + RESET
        )

        # IF YES - ASK AGAIN
        if user_continue.lower() == "y":
            browse_movies_year()

        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == "n":
            select_user_action(search_results)

        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED
                  + "\nInvalid choice; please choose a valid option (Y/N)"
                  + RESET)


get_movies()
create_top_100()
movies = Movies(top_100, all_movies)
home_menu()
