# IMPORT CSV MODULE
import csv

DATASET = "testsheet.tsv" # FILE PATH FOR IMDB DATASET
fav_list = [] # LIST OF USER FAVOURITES

# GETS DATA FROM IMDB DATASET AND STORES IN LIST
def get_data():
    with open(DATASET, "r") as f:
        tsv_f = csv.DictReader(f, delimiter="\t")
        data = []
        for row in tsv_f:
            if row["genres"] == '\\N':
                row["genres"] = '-' # OVERRIDE DEFAULT INVALID GENRE STRING
            data.append(row)
        return data

# SHOWS MOVIE LIST
def show_movies():
    index = 0 # SETS INITIAL INDEX TO 0
    data = get_data()

    # PRINT COLUMN HEADERS
    print(f'{"#":<5}{"Title":<50}{"Release":<10}{"Runtime":<10}{"Genre":<10}')

    # PRINT EACH MOVIE
    for movie in data:
        index += 1
        print(f'{index:<5}{movie["primaryTitle"]:<50}{movie["startYear"]:<10}{movie["runtimeMinutes"]:<10}{movie["genres"]}')
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
    
    # PRINT ROW HEADERS
    print(f'{"#":<5}{"Title":<50}{"Release":<10}{"Runtime":<10}{"Genre":<10}')
    
    index = 0 # SETS INITIAL INDEX TO 0
    
    # PRINT LIST OF FAVOURITES
    for fav in fav_list:
        index += 1
        if fav["genres"] == '\\N':
            fav["genres"] = '-'
        print(f'{index:<5}{fav["primaryTitle"]:<50}{fav["startYear"]:<10}{fav["runtimeMinutes"]:<10}{fav["genres"]}')
    
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
    print(f'\n{removed["primaryTitle"]} removed from favourites\n')
    
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
    movies_list = get_data()
    
    # ENTER # OF MOVIE
    favourite = int(input('\nType the ID of the movie and press enter to add favourite: ')) - 1
    
    # ADD CHOICE TO FAV LIST
    fav_list.append(movies_list[favourite])
    
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

get_data()
home_menu()