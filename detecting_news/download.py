import pandas as pd
import requests
import shelve
from urllib.request import urlopen

def extract_content(input, db):
    for i in range(0,len(input['url'])):
        try:
            response = requests.get(input.url[i], timeout=10)
            db[response.content.decode("utf-8")] = input.type[i]
            print("processing ", i, "str")
        except Exception as ex:
            pass



if __name__ == "__main__":
    input = pd.read_csv('input.csv', header=0)
    db = shelve.open('test.db', 'c')
    extract_content(input, db)

