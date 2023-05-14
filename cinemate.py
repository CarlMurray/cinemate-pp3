# IMPORT CSV MODULE
import csv

DATASET = "movie_data.tsv" # FILE PATH FOR IMDB DATASET
fav_list = [] # LIST OF USER FAVOURITES
list_headers = f'{"#":<8}{"Title":<50}{"Release":<10}{"Runtime":<10}{"Genre":<10}' # LIST HEADER FORMATTING

# MOVIE CLASS
class Movie:
    def __init__(self, index, title, date, runtime, genres):
        self.index = index          # INDEX TO SHOW IN PRINTED LIST
        self.title = title          # MOVIE TITLE
        self.date = date            # RELEASE DATE
        self.runtime = runtime      # MOVIE RUNTIME
        self.genres = genres        # GENRES

    def __str__(self):
        
        # TO PRINT GENRES LIST AS A STRING
        genre_sep = ', '
        genre_str = genre_sep.join(self.genres)
        
        # PRINT FORMAT FOR MOVIES
        return f'{self.index:<8}{self.title:<50}{self.date:<10}{self.runtime:<10}{genre_str}'

# GETS DATA FROM IMDB DATASET AND STORES IN LIST
def get_movies():
    with open(DATASET, "r") as f:
        tsv_f = csv.DictReader(f, delimiter="\t")
        movies = []
        index = 0
        for row in tsv_f:
            index += 1
            title = row["primaryTitle"]
            date = row["startYear"]
            runtime = row["runtimeMinutes"]
            genres = row["genres"].split(',') # CONVERT GENRE STRING TO LIST OF STRINGS
            movie = Movie(index, title, date, runtime, genres)
            movies.append(movie)
    return movies

# SHOWS MOVIE LIST
def show_movies():
    movies = get_movies()

    # PRINT LIST HEADERS
    print(list_headers)

    # PRINT EACH MOVIE
    for movie in movies:
        print(movie)
    select_user_action()

# HOME MENU FOR USER SELECTION
def home_menu():
    print('\nPlease select an option from the menu below:')
    print('1. Show all movies')
    print('2. Show favourites')
    print('3. Show watched')
    get_selection()
    
# REGISTER USERS MENU SELECTION
def get_selection():
    selection = input('\nPlease enter a number: ')
    if int(selection) == 1:
        show_movies()
    elif int(selection) == 2:
        show_favourites()
    # TODO: OTHER SELECTIONS TO BE ADDED
   
# SHOW FAV LIST
def show_favourites():
    
    # PRINT LIST HEADERS
    print(list_headers)
    
    index = 0 # SETS INITIAL INDEX TO 0
    
    # PRINT LIST OF FAVOURITES
    for movie in fav_list:
        index += 1
        movie.index = index
        print(movie)
        
    # SHOW OPTIONS MENU
    print('\nPlease select an option from the menu below:')
    print('1 - Remove favourite')
    print('0 - Exit to main menu')
    selection = int(input('\nPlease enter a number: '))
    if selection == 1:
        remove_favourite()
    elif selection == 0:
        home_menu()


# REMOVE FAVOURITE
def remove_favourite():
    selection = int(input('\nType the ID of the movie and press enter to remove favourite: ')) - 1
    
    # REMOVE SELECTED MOVIE FROM FAVOURITES
    removed = fav_list.pop(selection)
    
    # SHOW FEEDBACK MSG
    print(f'\n{removed.title} removed from favourites\n')
    
    # SHOW UPDATED FAVOURITES LIST
    show_favourites()
    
# PROMPT USER ACTION ON MOVIES LIST 
def select_user_action():
    action = int(input('\nSelect from the following:\n1 - Add a favourite\n2 - Add to watched\n0 - Exit to menu\n'))
    
    # IF EXIT CHOSEN
    if action == 0:
        home_menu()
    
    # IF FAVOURITE CHOSEN
    elif action == 1:
        add_favourite()
    
    # IF WATCHED (2) CHOSEN
    else:
        pass # TODO
        
# FOR USER TO ADD A FAVOURITE TO LIST
def add_favourite():
    movies = get_movies()
    
    # ENTER # OF MOVIE
    favourite = int(input('\nType the ID of the movie and press enter to add favourite: ')) - 1
    
    # ADD CHOICE TO FAV LIST
    fav_list.append(movies[favourite])
    
    # PROMPT USER FOR Y/N TO CONTINUE
    user_continue = input('\nDo you want to add another favourite? ')
    # IF YES - ASK AGAIN
    if user_continue == 'Y':
        add_favourite()
        
    # IF NO - QUIT
    elif user_continue == 'N':
        home_menu()
    
    # IF INVALID CHOICE - KEEP ASKING
    else:
        while user_continue != 'Y' or 'N':
            user_continue = input('\nPlease enter a valid choice (Y / N): ')
            if user_continue == 'Y':
                add_favourite()
            elif user_continue == 'N':
                home_menu()

    return fav_list

get_movies()
home_menu()