# IMPORT CSV MODULE
import csv

# GETS DATA FROM IMDB DATASET AND STORES IN LIST
def get_data():
    with open("testsheet.tsv", "r") as f:
        tsv_f = csv.DictReader(f, delimiter="\t")
        data = []
        for row in tsv_f:
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

# HOME MENU FOR USER SELECTION
def home_menu():
    print('Please select an option from the menu below:')
    print('1. Show all movies')
    print('2. Show favourites')
    print('3. Show watched')
    
# REGISTER USERS MENU SELECTION
def get_selection():
    selection = input('Please enter a number: ')
    if str(selection) == '1':
        show_movies()
    # TODO: OTHER SELECTIONS TO BE ADDED