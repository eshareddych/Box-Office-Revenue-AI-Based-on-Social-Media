import sqlite3 as sql
from AVL import AVL as avl


# Summary of file
#
# Creation and test of all the databases used
#
#


"""Raw comments"""
##conn = sql.connect("data.db")
##
##c = conn.cursor()
##
##c.execute("""CREATE TABLE submissions(
##                        id integer primary key autoincrement,
##                        sub_title text,
##                        sub_id text
##                        )""")
##
##c.execute("""CREATE TABLE comments(
##                        id integer primary key autoincrement,
##                        sub_id integer,
##                        comment text,
##                        date text
##                        )""")
##
##
##
##conn.commit()
##conn.close()

"""Check number of comments and submissions"""
##conn = sql.connect("data.db")
##c = conn.cursor()
##c.execute("SELECT id FROM comments")
##com = len(c.fetchall())
##c.execute("SELECT id FROM submissions")
##sub = len(c.fetchall())
##print(c.lastrowid)
##print("comments: {}\nsubmissions {}\n".format(com, sub))
##
##conn.commit()
##conn.close()

"""Organized data"""
##conn = sql.connect("organizedData.db")
##c = conn.cursor()
##
##c.execute("""CREATE TABLE movies(
##                        id integer primary key autoincrement,
##                        imdb_id text,
##                        mov_title text)
##""")
##
##c.execute("""CREATE TABLE mov_com(
##                        com_id integer,
##                        mov_id integer,
##                        imdb_id text)
##""")
##
##
##conn.commit()
##conn.close()

"""Upload movies into sql"""
##def sortData(file, item):
##        """Organize movies"""
##        movie_list = []
##        with open(file, encoding='utf-8') as movieFile:
##                for row in movieFile:
##                        info = row.split(",")
##                        new_title = info[item].replace("'","''")
##                        movie_list.append((info[0], new_title.lower()))
##        return movie_list
##
##movie_list = sortData('Movies_imdb.csv', 1)
##
##md = sql.connect("organizedData.db")
##c = md.cursor()
##for movie in movie_list:
##        c.execute("INSERT into movies VALUES(NULL, ?, ?)",(movie[0], movie[1]))
##        md.commit()
##        c.execute("SELECT * FROM movies WHERE mov_title = ?", (movie[1],))
##
##print('complete')
##md.close()

"""Testing the sql lookup for batches"""
##conn = sql.connect("data.db")
##c = conn.cursor()
##movie = movie_list[3]
##print(movie)
##c.execute("SELECT id FROM comments WHERE id <=  '{}' AND id > '{}' AND comment LIKE '%{}%'".format(10000, 0, movie))
##com_id = c.fetchall()
##print(com_id)
##c.execute("SELECT comment FROM comments WHERE id = '{}'".format(com_id[0][0]))
##print(c.fetchall())
##conn.commit()
##conn.close()

"""Testing the comments_movie data base"""
## no need bc comments has imdb id
##conn = sql.connect("organizedData.db")
##c = conn.cursor()
##c.execute("SELECT * FROM movies")
##results = c.fetchall()
##
##print(results[:1000])
##conn.close()

"""unique Movie related comments"""
#4688711 unique comments
#8803396 total comments
#3619 unique movies

##conn = sql.connect("comments.db")
##c = conn.cursor()
##c.execute("CREATE TABLE comments(id integer, imdb_id text, body text, date text)")
##conn.close()

"""Testing data transfers"""
##conn = sql.connect("comments.db")
##c = conn.cursor()
##c.execute("SELECT * FROM comments WHERE imdb_id = 'tt1655460'")
##results = c.fetchall()
##for result in results:
##        print(results)
##        input()
##conn.close()

"""Comments2"""
#4745569 comments


##conn = sql.connect("comments2.db")
##c = conn.cursor()
###c.execute("CREATE TABLE comments(id integer primary key autoincrement, com_id integer, imdb_id text, body text)")
###c.execute("INSERT into comments VALUES(NULL, 1, 'ab123', 'fuck yo mamama' )")
##c.execute("SELECT * FROM comments WHERE  id = 2988280")
##print(c.fetchall())
##conn.commit()
##conn.close()

"""Movie_meta"""

conn = sql.connect("movie_meta.db")
c = conn.cursor()
c.execute("SELECT * FROM meta")
print(c.fetchall())
conn.close()

        
