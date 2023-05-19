# IMPORT CSV MODULE
import csv
import textwrap

# COLOUR ESCAPE SEQ
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BG_BLUE = '\033[44m'
BG_GREEN = '\033[42m'
RESET = '\033[0m'

DATASET = "movie_data.tsv" # FILE PATH FOR IMDB DATASET
fav_list = [] # LIST OF USER FAVOURITES
watch_list = [] # USER WATCH LIST
list_headers = f'{"#":<8}{"Title":<45}{"Year":<6}{"Mins":<6}{"/10":<6}{"Votes":>7}' # LIST HEADER FORMATTING

# MOVIE CLASS
class Movie:
    def __init__(self, index, title, date, runtime, genres, rating, votes):
        self.index = index          # INDEX TO SHOW IN PRINTED LIST
        self.title = title          # MOVIE TITLE
        self.date = date            # RELEASE DATE
        self.runtime = runtime      # MOVIE RUNTIME
        self.genres = genres        # GENRES
        self.rating = rating        # RATING
        self.votes = votes          # NUM VOTES

    def __str__(self):
        
        # TO PRINT GENRES LIST AS A STRING
        genre_sep = ', '
        genre_str = genre_sep.join(self.genres)
        
        # PRINT FORMAT FOR MOVIES
        return f'{self.index:<8}{textwrap.shorten(self.title, width=40, placeholder="..."):<45}{self.date:<6}{self.runtime:<6}{self.rating:<6}{self.votes:>7}'

# CLEAR TERMINAL SCREEN
def clear_screen():
    print("\033c")

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
            rating = row['averageRating']
            votes = row['numVotes']
            movie = Movie(index, title, date, runtime, genres, rating, votes)
            movies.append(movie)
    return movies

# SHOWS MOVIE LIST
def show_movies():
    clear_screen()
    movies = get_movies()

    # PRINT LIST HEADERS
    print(BG_GREEN + f'{list_headers}' + RESET)

    # PRINT EACH MOVIE
    for movie in movies:
        print(BG_BLUE + f'{movie}' + RESET)
    # PRINT LIST HEADERS AT BTM OF LIST
    print(BG_GREEN + f'{list_headers}' + RESET)
    select_user_action()

# HOME MENU FOR USER SELECTION
def home_menu():
    clear_screen()
    print(GREEN + '\nPlease select an option from the menu below:')
    print('1 - Show all movies')
    print('2 - Show favourites')
    print('3 - Show watched')
    print('4 - Show top 100')
    print('5 - Browse movies' + RESET)
    get_selection()
    
# REGISTER USERS MENU SELECTION
def get_selection():
    while True:
        try:
            selection = int(input(YELLOW + '\nPlease enter a number from the menu: ' + RESET))
        except:
            print(RED + '\nInvalid choice; please choose a valid option' + RESET)
        else:            
            if int(selection) == 1:
                show_movies()
            elif int(selection) == 2:
                show_custom_list(list=fav_list, list_name_string='favourites')
            elif int(selection) == 3:
                show_custom_list(list=watch_list, list_name_string='watch list')
            elif int(selection) == 4:
                show_top_100()
            elif int(selection) == 5:
                browse_movies()
            # TODO: OTHER SELECTIONS TO BE ADDED
            else:
                print(RED + '\nInvalid choice; please choose a valid option' + RESET)
                continue
                
    
# PROMPT USER ACTION ON MOVIES LIST 
def select_user_action(genre_results = None, top_100 = None, search_results = None):
    action = int(input(GREEN + '\nSelect from the following:\n1 - Add a favourite\n2 - Add to watched\n0 - Exit to menu\n' + RESET))
    
    # IF EXIT CHOSEN
    if action == 0:
        home_menu()
    
    # IF FAVOURITE CHOSEN
    elif action == 1:
        add_to_custom_list(genre_results, top_100, search_results, list=fav_list, list_name_string='favourites')
        
    # IF WATCH LIST CHOSEN
    elif action == 2:
        add_to_custom_list(genre_results, top_100, search_results, list=watch_list, list_name_string='watch list')
    
    # IF WATCHED (2) CHOSEN
    else:
        pass # TODO
        
    
# SHOW WATCH/FAV LIST
def show_custom_list(removed = None, list=None, list_name_string=None):
    clear_screen()
    print(list)
    print(list_name_string)
    # PRINT LIST HEADERS
    print(BG_GREEN + f'{list_headers}' + RESET)
    
    index = 0 # SETS INITIAL INDEX TO 0
    
    # IF LIST EMPTY, SHOW MESSAGE
    if len(list) == 0 or len(list) is None:
        print(RED + f'{list_name_string} list empty' + RESET)
        
    # PRINT LIST OF WATCH LIST MOVIES
    for movie in list:
        index += 1
        movie.index = index
        print(BG_BLUE + f'{movie}' + RESET)
    print(BG_GREEN + f'{list_headers}' + RESET)
    
    # PRINTS REMOVED WATCH LIST MOVIE IF APPLICABLE
    if removed:
      print(RED + f'\n{removed.title} removed from {list_name_string} list' + RESET)

    # SHOW OPTIONS MENU
    print(GREEN + '\nPlease select an option from the menu below:')
    print(f'1 - Remove from {list_name_string} list')
    print('0 - Exit to main menu' + RESET)
    
    while True:
        try:
            selection = int(input(YELLOW + '\nPlease enter a number from the menu: ' + RESET))
        except:
            print(RED + '\nInvalid choice; please choose a valid option' + RESET)
        else:
            if selection == 1:
                remove_from_custom_list(list=list, list_name_string=list_name_string)
            elif selection == 0:
                home_menu()
            else:
                print(RED + '\nInvalid choice; please choose a valid option' + RESET)
                continue
    
    
    
# FOR USER TO ADD A FAVOURITE TO LIST
def add_to_custom_list(genre_results = None, top_100 = None, search_results = None, list=None, list_name_string=None):
    
    # CHECK WHERE USER IS COMING FROM TO GET CORRECT MOVIE LIST
    if top_100:
        movies = create_top_100()
    elif genre_results:
        movies = genre_results
    elif search_results:
        movies = search_results
    else:
        movies = get_movies()
    
    add_movie = None
    while add_movie is None:
        try:
            # ENTER # OF MOVIE
            add_movie = int(input(YELLOW + f'\nType the ID of the movie and press enter to add to {list_name_string}: ' + RESET)) - 1
            
            # CHECK IF MOVIE ALREADY IN FAVOURITES
            if movies[add_movie].title not in [movie.title for movie in list]:
                # ADD CHOICE TO FAV LIST
                list.append(movies[add_movie])
                print(GREEN + f'\n{movies[add_movie].title} added to {list_name_string}' + RESET)
            
            else:
                raise TypeError
        
        # ERROR FOR INVALID CHOICE         
        except (ValueError, IndexError):
            print(RED + '\nInvalid choice; please choose a valid option' + RESET)
            add_movie = None
        
        # ERROR IF ALREADY IN FAVOURITES
        except TypeError:
            print(RED + f'\n{movies[add_movie].title} already in {list_name_string}' + RESET)
    
    user_continue = None
    while user_continue not in ['y', 'n', 'Y', 'N']:
        
        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(YELLOW + f'\nDo you want to add another movie to {list_name_string}? (Y/N) ' + RESET)

        # IF YES - ASK AGAIN
        if user_continue.lower() == 'y':
            add_to_custom_list(movies, list=list, list_name_string=list_name_string)
            
        # IF NO - QUIT
        elif user_continue.lower() == 'n':
            home_menu()
    
    # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED + '\nInvalid choice; please choose a valid option (Y/N)' + RESET)

    return list
    
    
# REMOVE FROM WATCH/FAV LIST
def remove_from_custom_list(list=None, list_name_string=None):
    selection = int(input(YELLOW + f'\nType the ID of the movie and press enter to remove from {list_name_string}: ' + RESET)) - 1
    
    # REMOVE SELECTED MOVIE FROM WATCH LIST
    removed = list.pop(selection)
    
    # SHOW FEEDBACK MSG
    print(GREEN + f'\n{removed.title} removed from {list_name_string}\n' + RESET)
    
    # SHOW UPDATED WATCH LIST
    show_custom_list(removed, list=list, list_name_string=list_name_string)


# CREATE TOP 100 MOVIES LIST
def create_top_100():
    movies = get_movies() # GET ALL MOVIES
    
    # SORT BY NUM VOTES
    sorted_by_votes = sorted(movies, key=lambda movie: int(movie.votes), reverse=True)
    
    # GET ONLY TOP 100 WITH MOST VOTES
    top_100 = sorted_by_votes[:100]
    
    # SORT MOST VOTED MOVIES BY RATING
    top_100 = sorted(top_100, key= lambda movie: float(movie.rating), reverse=True)

    return top_100

# SHOWS TOP 100 LIST OF MOVIES
def show_top_100():
    clear_screen()
    top_100 = create_top_100()
    
    # PRINT LIST OF TOP 100 MOVIES
    index = 0
    print(BG_GREEN + f'{list_headers}' + RESET)
    for movie in top_100:
        index += 1
        movie.index = index
        print(BG_BLUE + f'{movie}' + RESET)
    print(BG_GREEN + f'{list_headers}' + RESET)
    select_user_action(top_100)

# BROWSE ALL MOVIES
def browse_movies():
    clear_screen()
    action = None
    while action not in ['0', '1', '2', '3']:
        print(GREEN + '\nSelect from the following:\n1 - Search movies\n2 - Browse by genre\n3 - Browse by year\n0 - Exit to menu' + RESET + '\n')
        action = input(YELLOW + 'Please enter a number from the menu: ' + RESET)
        if action == '1':
            browse_movies_search()
        elif action == '2':
            browse_movies_genre()
        elif action == '3':
            browse_movies_year()
        elif action == '0':
            home_menu()
        else:
            print(RED + '\nInvalid choice; please choose a valid option' + RESET)
       
        
# SEARCH MOVIES BY TITLE
def browse_movies_search():
    clear_screen()
    movies = get_movies()
    query = input(YELLOW + "Enter a search query: " + RESET)
    search_results = []
    index = 0
    print(BG_GREEN + f'{list_headers}' + RESET)
    for movie in movies:
        if query.lower() in movie.title.lower():
            index += 1
            movie.index = index
            search_results.append(movie)
            print(BG_BLUE + f'{movie}' + RESET)
        else:
            pass
    print(BG_GREEN + f'{list_headers}' + RESET)
    if len(search_results) == 0:
        print(RED + 'No matches found' + RESET)   

    user_continue = None
    while user_continue not in ['y', 'n', 'Y', 'N']:
        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(YELLOW + '\nDo you want to enter another search query? (Y/N) ' + RESET)
        
        # IF YES - ASK AGAIN
        if user_continue.lower() == 'y':
            browse_movies_search()
            
        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == 'n':
            select_user_action(search_results)
        
        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED + '\nInvalid choice; please choose a valid option (Y/N)' + RESET)
    
# BROWSE MOVIES BY GENRE
def browse_movies_genre():
    clear_screen()
    movies = get_movies() # GET LIST OF ALL MOVIES
    genres = get_genres() # GET LIST OF GENRES
    print(GREEN + '\nSelect from the following: ' + RESET)
    i = 0 # GENRE INDEX
    
    # PRINT LIST OF GENRES TO CHOOSE
    for genre in genres:
        i += 1
        print(BG_BLUE + f'{i:<2} - {genre:<15}' + RESET)
    
    
    genre_index = None
    while genre_index is None:
        try:
            # GET USER GENRE CHOICE
            genre_index = int(input(YELLOW + '\nSelect a genre from the list: ' + RESET)) - 1
            clear_screen()
            genre_choice = genres[genre_index]
            genre_results = create_genre_results(movies, genre_choice)
            
        except (IndexError, ValueError):
            print(RED + '\nInvalid choice; please choose a valid option' + RESET)
            genre_index = None
    
    user_continue = None
    while user_continue not in ['y', 'n', 'Y', 'N']:

        # PROMPT USER FOR Y/N TO CONTINUE
        user_continue = input(YELLOW + '\nDo you want to choose a different genre? (Y/N) ' + RESET)
        
        # IF YES - ASK AGAIN
        if user_continue.lower() == 'y':
            browse_movies_genre()
            
        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == 'n':
            select_user_action(genre_results)
        
        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED + '\nInvalid choice; please choose a valid option (Y/N)' + RESET)
        
# CREATE GENRE SEARCH RESULTS MOVIE LIST
def create_genre_results(movies, genre_choice):
    search_results = []
    index = 0
    print(BG_GREEN + f'{list_headers}' + RESET)
    
    # ITERATE THROUGH ALL MOVIES
    for movie in movies:
        
        # IF USERS GENRE MATCHES MOVIE, PRINT MOVIE
        if genre_choice in movie.genres:
            index += 1
            movie.index = index
            search_results.append(movie)
            print(BG_BLUE + f'{movie}' + RESET)
    print(BG_GREEN + f'{list_headers}' + RESET)
    return search_results  

# TO DEFINE LIST OF GENRES    
def get_genres():
    movies = get_movies()
    genres_array = [] # ARRAY TO STORE GENRES
    
    # ITERATE THROUGH ALL MOVIES, ADD GENRES TO ARRAY
    for movie in movies:
        for genre in movie.genres:
            
            # IF GENRE ALREADY IN ARRAY, SKIP
            if genre in genres_array:
                continue
            
            # ELSE ADD TO GENRES ARAY
            else: 
                genres_array.append(genre)
    return genres_array
    
def browse_movies_year():
    movies = get_movies()
    search_results = []
    index = 0
    query = None
    while query is None:
        try:
            query = input(YELLOW + '\nEnter a year from 2000 - 2023: ' + RESET)
            if 2000 > int(query) or int(query) > 2023:
                query = None
                raise ValueError
            
        except (ValueError):
            print(RED + '\nInvalid choice; please enter a year from 2000 - 2023' + RESET)
            query = None

    print(BG_GREEN + f'{list_headers}' + RESET)
    for movie in movies:
        if query in movie.date :
            index += 1
            movie.index = index
            search_results.append(movie)
            print(BG_BLUE + f'{movie}' + RESET)
        else:
            pass   
    print(BG_GREEN + f'{list_headers}' + RESET)

    # PROMPT USER FOR Y/N TO CONTINUE
    user_continue = None
    while user_continue not in ['y', 'n', 'Y', 'N']:
        user_continue = input(YELLOW + '\nDo you want to choose a different year? (Y/N) ' + RESET)

        # IF YES - ASK AGAIN
        if user_continue.lower() == 'y':
            browse_movies_year()
            
        # IF NO - SHOW OPTIONS
        elif user_continue.lower() == 'n':
            select_user_action(search_results)
        
        # IF INVALID CHOICE - KEEP ASKING
        else:
            print(RED + '\nInvalid choice; please choose a valid option (Y/N)' + RESET)
    
get_movies()
create_top_100()
home_menu()