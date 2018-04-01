
#DESCRIPTION#

#################
## This file handles scraping each IMDB review page for the reviews and putting them into a SQLite database
## There are methods to read data from the CSVs containing movie metadata since they are needed to scrape reviews.
#################

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pyrebase
import csv
import time


#Guide on how to use PyreBase
#https://github.com/thisbejim/Pyrebase

config = {
  "apiKey": "AIzaSyCDgLh7mESbHb31Lgjy4iWpUjen0f5DnlM",
  "authDomain": "box-office-ai.firebaseapp.com",
  "databaseURL": "https://box-office-ai.firebaseio.com",
  "storageBucket": "box-office-ai.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


#Adding a values to the database
#NEVER do db.child('movies).set(...), this will erase the entire DB

#Creating a new review, with ID t2236
data = {'title': 'The Dark Knight',
             'release': '7-Mar-08',
             'box': 3510000,
             'genre': 'Action',
             'director': 'Christopher Nolan',
             'main_actor': 'Christian Bale' }
#db.child('movies').child('t2236').set(data)

#Adding a new IMDB review to an existing title
review = {'title': 'yes, THIS IS THE SHIT',
          'rating': 8,
          'date': '10/2/18',
          'text': 'i luv this movie jk its the best'}

db.child('movies').child('t22378').child('reviews').child(1).set(review)

#Getting a movie is as simple as doing:
#movie = db.child("movies").child('t2236').get().val()


#Input: imdb id string
#Scrapes all reviews of that movie and returns a list of all reviews
def scrape_reviews(imdb_id):
    url = 'http://www.imdb.com/title/' + imdb_id + '/reviews'

    #In case of rejection by server, try again
    try:
        res = requests.get(url)
    except:
        print("Connection refused by server...")
        print("Sleeping...")
        time.sleep(5)
        res = requests.get(url)
    broth = BeautifulSoup(res.text,"lxml")
    count = 1
    result = []
    #Extracting the title and review
    for item in broth.select(".review-container"):
        title = item.select(".title")[0].text
        review_text = item.select(".text")[0].text
        # rating = item.select(".rating-other-user-rating")[0].text
        rating_tree = item.find("span").children
        rating = "None"
        for i, val in enumerate(rating_tree):
            if i == 3:
                rating = val.text
                break
        date = item.select(".review-date")[0].text

        review = {'title': title,
                  'rating': rating,
                  'date': date,
                  'text': review_text}
        # print(type(title))
        # db.child('movies').child(imdb_id).child('reviews').child(title).set(review)
        result.append(review)
        # print("Title: {}\n\nReview: {}\n\n".format(title,review)
        count += 1

    #Finding the tag where the link to the next set of reviews are located
    loadMore= broth.find(attrs={"class": "load-more-data"})

    while loadMore:
        #In the case of loadMore existing by having no data-key element, stop crawling
        try:
            dataKey = loadMore['data-key']
        except:
            break
        url = 'http://www.imdb.com/title/' + imdb_id + '/reviews/_ajax?paginationKey=' + dataKey
        #Issue when hitting errors when sending too many IPs at at time
        try:
            res = requests.get(url)
        except:
            print("Connection refused by server...")
            print("Sleeping...")
            time.sleep(5)
            res = requests.get(url)
        broth = BeautifulSoup(res.text, "lxml")
        for item in broth.select(".review-container"):
            title = item.select(".title")[0].text
            review_text = item.select(".text")[0].text
            date = item.select(".review-date")[0].text
            rating_tree = item.find("span").children
            rating = "None"
            for i, val in enumerate(rating_tree):
                if i == 3:
                    rating = val.text
                    break
            review = {'title': title,
                      'rating': rating,
                      'date': date,
                      'text': review_text}
            result.append(review)
            count += 1
            # print("Title: {}\n\nReview: {}\n\n".format(title, review))

        # Finding the tag where the link to the next set of reviews are located
        loadMore = broth.find(attrs={"class": "load-more-data"})

    return result

#Takes in the CSV of all movies and their metadata, and adds it into the firebase DB along with each movies corresponding reviews
def upload_movies():
    file = open('all_metadata.csv', 'r', encoding="utf8")
    reader = csv.reader(file)

    count = 0
    #Skipping the headers
    next(reader)
    for line in reader:
        count += 1
        if count >= 3176:
            movie = {'title': line[1],
                     'box': line[3],
                     'release': line[4],
                     'genre': line[5],
                     'director': line[6],
                     'main_actor': line[7]}
            db.child('movies').child(line[0]).set(movie)
            scrape_load_reviews(line[0])
            print(line[0])
            print(count)
            time.sleep(3)


def read_reviews_csv():
    # Setting up for reading
    inFile = open('all_metadata.csv', 'r', encoding="utf8")
    reader = csv.reader(inFile)

    # Setting up for writing
    outFile = open('reviews2.csv', 'a', encoding="utf8", newline='')
    fieldnames = ['imdb_id', 'title', 'date', 'score', 'review']
    writer = csv.DictWriter(outFile, fieldnames=fieldnames)
    writer.writeheader()

    count = 0
    next(reader)
    for line in reader:
        imdb_id = line[0]
        count += 1
        if count > 71:
            reviews = scrape_reviews(imdb_id)
            # budget = scrape_budget(imdb_id)
            # movie = {'title': line[1],
            #          'box': line[3],
            #          'release': line[4],
            #          'genre': line[5],
            #          'director': line[6],
            #          'main_actor': line[7],
            #          'budget': budget}
            # db.child('movies').child(line[0]).set(movie)
            for review in reviews:
                writer.writerow({'imdb_id': imdb_id, 'title': review['title'], 'date': review['date'], 'score': review['rating'],
                                 'review': review['text']})
            time.sleep(2)
            print(imdb_id)
            print(count)


read_reviews_csv()
# scrape_budget('tt0206634')