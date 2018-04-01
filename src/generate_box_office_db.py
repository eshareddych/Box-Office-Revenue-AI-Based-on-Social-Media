import nltk
import sqlite3 as sql

#
# Generating a database of imdb_id with their box office revenue.
#
conn = sql.connect("movie_meta.db")
c = conn.cursor()
#c.execute("CREATE TABLE meta( imdb_id text, box_office integer)")
with open("movie_metadata.csv", encoding = 'utf-8') as mov_md:
        for count, row in enumerate(mov_md):
                info = row.split(",")
                try:
                        box = int(info[3])
                        
                        c.execute("INSERT INTO meta VALUES(?,?)",(info[0], box))
                        if count% 100 == 0:
                                conn.commit()
                except Exception as e:
                        print(e)
                        continue

        conn.commit()

conn.close()
