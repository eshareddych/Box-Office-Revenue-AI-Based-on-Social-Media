from AVL import AVL
import sqlite3 as sql
import nltk
from collections import defaultdict

#
# Level 1 sorting of the comments
# takign the raw data extracted from Reddit and puttin them into a data base with the relevant information
#

def sortData(file, item):
        """Organize movies"""
        tree = AVL()
        with open(file, encoding='utf-8') as movieFile:
                for row in movieFile:
                        info = row.split(",")
                        new_title = info[item].replace("'","''")
                        tree.add(new_title.lower())
        return tree


def checkLimit(cursor, curr_id):
        """check if the upper bound of batch exists"""
        cursor.execute("SELECT id FROM comments WHERE id = ?", (curr_id + 10000,))
        exists = len(cursor.fetchall())
        return True if exists == 0 else False


def checkMovie(movie):
        check_movie = movie.split()
        if len(check_movie) == 1:
                if len(check_movie[0]) < 4:
                        return True

        
def checkBatch(cursor, curr_id, ocursor, movie_list, rc):
        """returning 10,000 comments"""
        upper_id = curr_id + 10000
        for movie in movie_list:
                
                ocursor.execute("SELECT * FROM movies WHERE mov_title = ?", (movie,))
                mov_id = ocursor.fetchall()
                if len(mov_id) == 0: continue
                
                cursor.execute("SELECT id FROM comments WHERE id < '{}' AND id >= '{}' AND comment LIKE '% {} %'".format(upper_id, curr_id, movie))
                com_id = cursor.fetchall() # List of ids , com_id[x][0]
                if (len(com_id) == 0): continue
                
                for comments in com_id:
                        comments_id = int(comments[0])
                        movie_id = int(mov_id[0][0])
                        imdb_id = mov_id[0][1]
                        ocursor.execute("INSERT into mov_com VALUES(?, ?, ?)", (comments_id, movie_id, imdb_id))

                        cursor.execute("SELECT * FROM comments WHERE id = ?",(comments_id,))
                        results = cursor.fetchall()

                        rc.execute("INSERT into comments VALUES(?, ?, ?, ?)", (comments_id, imdb_id, results[0][2], results[0][3]))
                                                                                                                                        #raw_data_id, imdb_id, body, date
        

if __name__ == "__main__":

        """list of movies to search with """
        tree = sortData('Movies_imdb.csv', 1)
        movie_list = [x for x,y in tree.returnString().items() if not checkMovie(x) ]
        
        """organizing sql with movies and movie comment relationship"""
        od = sql.connect("organizedData.db")
        organize = od.cursor()

        """getting the comments data"""
        conn = sql.connect("data.db")
        c = conn.cursor()

        """Comments with a movie in the body"""
        relcom = sql.connect("comments.db")
        rc = relcom.cursor()

        curr_id = 300001 # lower bound
        # continue the curr_id from the one left off if broken
        
        while(True):
                """check curr_id + 10000 exists in the table"""
                if checkLimit(c, curr_id):
                        """print information"""
                        print("Comments organized up to: {}".format(curr_id))
                        break

                """Get the 10,000 batch of comments"""
                try:
                        checkBatch(c, curr_id, organize, movie_list, rc)
                        
                except Exception as e:
                        print("Curr_id: {} uncommited".format(curr_id))
                        print("Error: {}".format(e))
                        break
        
                print("Batch commited: {} -> {}".format(curr_id, curr_id+10000))
                od.commit()
                relcom.commit()
                
                curr_id = curr_id + 10000

                #should be select distinct
                rc.execute("SELECT id FROM comments")
                total_unique = rc.fetchall()
                print("Unique comments: {}".format(len( total_unique)))
                
                if ((len(total_unique) % 10000) == 0):
                      if (input("Stop: ") == 'n'):
                              break

        od.close()
        conn.close()
        relcom.close()

        
