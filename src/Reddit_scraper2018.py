import praw
import datetime
import nltk
import sqlite3 as sql
import math
from time_stamp import unixTimes
from AVL import AVL
#
#
# Program functionality:
#       scrape reddit comments with keyword
#       take all comments associated with that key word




#
#
# Reddit
#
#
def createReddit():
        reddit = praw.Reddit(client_id='E3WNXitukb1syA',
                             client_secret='nbh4MmwXCHKWx9ml2VQsEpafIYE',
                             user_agent='my user agent')
        return reddit

#def searchSubReddit(db, tree, reddit, subreddit, keyword, database):
def searchSubReddit(db, tree, reddit, subreddit, database, unixTimes):

        unixList = unixTimes.getTimes()
        datetimeList = unixTimes.getDateTimes()
        #for submission in reddit.subreddit(subreddit).search(keyword)
        # for submission in reddit.subreddit(subreddit).top(limit = 10000)
        for index, times in enumerate(unixList):
                print("start: {} ==== end: {} ".format(datetimeList[index][0],datetimeList[index][1]))
                for submission in reddit.subreddit(subreddit).submissions(times[0], times[1]):

                        try:
                                """check the submission is not in the database"""
                                if searchDataBase(database, submission.id): continue

                                """Search the submission comments, --->searchSubmission()"""
                                searchSubmission(submission, tree, database)

                                """add submission into data base"""
                                addToSubmissions(database, [submission.title.lower(), submission.id])
                                db.commit()
                                
                        except Exception as e:
                                print("ERROR searchsubreddit(): {}".format(e))
                                #should log all the crashes
                                continue
                

                        
def searchSubmission(submission, tree, database):
        ##stop = stopwords.words('english') + list(string.punctuation)
        sub_id = submission.id
        commentTree = submission.comments.list()

        for comments in commentTree:
                try:
                        if type(comments) == praw.models.MoreComments: continue
                        
                        ##need to check that the comment has movie title in the name
                        ##new_comment =  [i for i in word_tokenize(comments.body.lower()) if i not in stop]
                        time_comment = datetime.datetime.utcfromtimestamp(comments.created_utc)

                        """add comment into database"""
                        addToComments(database, [sub_id, comments.body, time_comment])
                        
                except Exception as e:
                        print("ERROR searchsubmission(): {}".format(e))
                        #log all the crashes
                        continue
                
#
#
# Data sorting
#
#
def sortData(file, item):
        tree = AVL()
        with open(file, encoding='utf-8') as movieFile:
                for row in movieFile:
                        info = row.split(",")
                        tree.add(info[item].lower())
        return tree

def searchDataBase(database, value):
        """searching if value in table exist"""
        
        database.execute("SELECT * FROM submissions WHERE sub_id = '{}'".format( str(value)))
        results = database.fetchall()
        return True if len(results) != 0 else False

def addToSubmissions(database, values):
        """values should be a list where [0] = title, [1] = subID"""
        database.execute("INSERT into submissions VALUES(NULL, ?, ?)",(values[0], values[1]))

def addToComments(database, values):
        """values should be a list where [0] = sub id it belongs to, [1] = text, [2] = date"""
        database.execute("INSERT into comments VALUES(NULL, ?, ?, ?)",(values[0], values[1], values[2]))

def printSize():
        conn = conn = sql.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM comments")
        com = c.fetchall()
        c.execute("SELECT * FROM submissions")
        sub = c.fetchall()
        conn.commit()
        conn.close()
        return (len(com), len(sub))

#
#
# Main function
#       - sql data base lock up = missed submissions
#
if __name__ == "__main__":

        tree = sortData('Movies_imdb.csv', 1)
        reddit = createReddit()
        subreddit = 'movies'
        #keyword = 'movie'
        db = sql.connect("data.db")
        database = db.cursor()
        unixTimes = unixTimes()
        
        check = True
        try:
                while(check):
                        #searchSubReddit(db, tree, reddit, subreddit, keyword, database)
                        searchSubReddit(db, tree, reddit, subreddit, database, unixTimes)

                        print(printSize())
                        check = False
                        
        except Exception as e:
                print("ERROR main(): {}".format(e))
                db.commit()
                db.close()

                
