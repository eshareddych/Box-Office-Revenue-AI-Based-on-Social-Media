#Reddit API
"""

client_id:   E3WNXitukb1syA
name: Team_swag2018
password: 12795fu
secret:  nbh4MmwXCHKWx9ml2VQsEpafIYE

"""

#
# Scrape reddit data and store into a sqlite3 database
#

import praw
import datetime
import nltk
import sqlite3 as sql
from AVL import AVL

#Sorts large sets of data into avl tree.
# movies or submissions
def sortData(file, number):
        # file = 'Movies_imdb.csv'
        tree = AVL()
        with open(file, encoding='utf-8') as movieFile:
                for row in movieFile:
                        info = row.split(",")
                        tree.add(info[number].lower())
        return tree

def createReddit():
        reddit = praw.Reddit(client_id='E3WNXitukb1syA',
                             client_secret='nbh4MmwXCHKWx9ml2VQsEpafIYE',
                             user_agent='my user agent')
        return reddit

def writeToCSV(file, comment, datetime, movietitle, movieid):
        #file =  csvfile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file.writerow([movieid, movietitle, datetime, comment])

def createDict(file):
        commentDict = defaultdict(list)
        data_id = dict()
        with open(file, encoding='utf-8') as openFile:
                for row in openFile:
                        info = row.split(",")
                        dataDict[info[1].lower()].append()
                        data_id[info[1]] = info[0]
        return commentDict, data_id
                        

#run this as many times for as many subreddits to search in
def search(subreddit, movieTitles, checkSubs, database):
        stopwords = stopwords.words('english') + list(string.punctuation)
        #store all information into database, convert from cvs to the database
        with open('visited_submissions.csv', ',a', newline='', encoding='utf-8') as submission_file:
                submission_file = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

                for submission in createReddit().subreddit(subreddit).search('movie'):
                        #add submission to data base: unique id, submission title
                        #query SELECT * FROM tablename ORDER BY column DESC LIMIT 1; returns the most recent added 
                        try:

                                # if the sub id has already been searched, then ignore
                                sub_id = submission.id
                                if checkSubs.search(sub_id): continue
                                sub_title = submission.title.lower()
                                submission_file.writerow([sub_id, sub_title])
                                
                                commentTree = submission.comments.list()
                                for comments in commentTree:
                                        new_comments =  [i for i in word_tokenize(comments.body.lower()) if i not in stop]
                                        #add this into the database
                                        # table: unique id, submission id, date, text
                                        """
                                        #if comment is this type, ignor
                                        if type(comments) == praw.models.MoreComments: continue
                                        for movie in movieTitles.keys():
                                                #check all 5000 movies if it is in a single comment
                                                if movies.lower() in comments.lower():
                                                        comments_file.writerow([movie, comments.body, datetime.datetime.utcfromtimestamp(comments.created_utc)])
                                        """
                                        
                        except Exception as exc:
                                print("error {}: {}".format(type(exc), inst.args))
                                cont = input("type 'y':")
                                if cont == 'y':
                                        continue

if __name__ == "__main__":
        #run this program per subreddit
        check = True
        tree = sortData('Movies_imdb.csv', 1)
        #movie_title_comments, movie_title_id = createDict('Movies_imdb.csv')
        check_submissions = sortData('visited_submissions.csv',0)
        conn = sql.connect("comments.db")
        
        while(check):
               try:
                       search('AskReddit', movie_title_id, check_submissions, conn)
                       
                except:
                        user_input = input("continue?")
                        if user_input == "n": check = False
                        else: continue
