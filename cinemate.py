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

print(get_data())