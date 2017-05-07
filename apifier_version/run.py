# coding: utf8
import requests
from peewee import *
#import MySQLdb

db = SqliteDatabase('triplets.db')

class BaseModel(Model):
    class Meta:
        database = db

class Triplets_table(BaseModel):
    url = CharField(primary_key=True)
    title = CharField()
    description = CharField()

Triplets_table.create_table(True)

if __name__ == "__main__":
    user_id = 'sk5kPLfTm9tSzodpQ'
    access_token = 'WtgTXNi9eZAsmzhJhA95Yjnm5'
    rss_crawler = requests.post('https://api.apifier.com/v1/'+user_id+'/crawlers/Rss_crawler/execute?token='+access_token+'')
    url_result = rss_crawler.json()['resultsUrl']
    rss_crawler = rss_crawler.json()['detailsUrl']

    #print rss_crawler
    status = requests.get(rss_crawler).json()['status']
    while(status!='SUCCEEDED'):
        status = requests.get(rss_crawler).json()['status']
    #print status
    rss_result = requests.get(url_result)
    triplets = rss_result.json()[0]['pageFunctionResult']
    #print (len(triplets))
    for i in range (0, len(triplets)):
        try:
            Triplets_table.create(url=triplets[i]['link'], title=triplets[i]['title'], description=triplets[i]['description'])
        except Exception:
            pass


    #print (triplets)