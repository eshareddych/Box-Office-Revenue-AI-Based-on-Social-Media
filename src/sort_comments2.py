from AVL import AVL
import sqlite3 as sql
import nltk
from collections import defaultdict
from movie_count_text_reader import whitelist , shortbus
#Get the entire data base so that i can batch organize it
#loop every 100,000 comments, organize, and store

#removing movies with more than 100,000 comments = 13 movies
# removing movies with less than 500 comments =
if __name__ == "__main__":
        
        conn = sql.connect("comments.db")
        conn2 = sql.connect("comments2.db")
        c = conn.cursor()
        c2 = conn2.cursor()

        #blacklist + whtelist = 3619 entire movie corpus
        black_list = ['tt0493464','tt1726085','tt5129656','tt6645608','tt3800816','tt1844678','tt6244898','tt1853619','tt1190130','tt1869538','tt1127886','tt2291230','tt4700756']
        white_list = whitelist
        
        #109 movies over 10,000 comments
        short_bus = shortbus
        
        for movies in whitelist:
                print(movies[0])
                try:
                        
                        c.execute("SELECT id, imdb_id, body FROM comments WHERE imdb_id = ?", (movies[0],))
                        comments = c.fetchall()
                        
                        for comment in comments:
                                c2.execute("INSERT INTO comments VALUES(NULL, ?, ?, ?)", (comment[0], comment[1], comment[2]))
                        conn2.commit()
                except Exception as e:
                        print(e)
                        continue

        print("close")
        conn.close()
        conn2.close()
