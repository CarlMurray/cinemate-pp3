import pandas as pd

# CHOOSE PATH FOR NEW TSV OUTPUT
OUTPUT_PATH = '/Users/carl.murray/Documents/cinemate-pp3/movie_data.tsv'

# OPEN IMDB TSV FILES
df_basics = pd.read_table('title.basics.tsv', low_memory=False)
df_ratings = pd.read_table('title.ratings.tsv', low_memory=False)

# REMOVE UNUSED COLUMNS
df_basics.drop(columns=['endYear', 'isAdult', 'originalTitle'], inplace=True)

# FILTER DATA - MOVIES ONLY, MUST HAVE VALID DATA
df_basics = df_basics.loc[
    (df_basics['titleType'] == 'movie') & 
    (df_basics['runtimeMinutes'] != '\\N') &
    (df_basics['genres'] != '\\N') &
    (df_basics['startYear'] != '\\N')
]

# CONVERT COLUMNS TO INT 
df_basics['startYear'] = df_basics['startYear'].astype(int)
df_basics['runtimeMinutes'] = df_basics['runtimeMinutes'].astype(int)

# FILTER BY DATE AND RUNTIME
df_basics = df_basics.loc[
    (df_basics['runtimeMinutes'] > 100) &
    (df_basics['startYear'] > 2015)
]

# MERGE TSVs - ONLY MOVIES WITH RATINGS INCLUDED
combined = pd.merge(df_basics, df_ratings, on='tconst')

# DEFINE OUTPUT COLUMNS
columns = ['primaryTitle', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'numVotes']

# OUTPUT TO NEW TSV FILE
combined.to_csv(OUTPUT_PATH , sep='\t', header=True, index=False, columns=columns)