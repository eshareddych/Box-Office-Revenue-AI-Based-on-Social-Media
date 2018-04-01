import random
from AVL import AVL
import sqlite3 as sql
import nltk
from collections import defaultdict
from movie_count_text_reader import whitelist , shortbus


#
# Generates subset databases of 100000 comments
#

total = 4745569 # add one because range is up to but not including
conn1 = sql.connect("comments2.db")
c1 = conn1.cursor()

samples = random.sample(range(1,4745570), 4745569)
ver = 1
a = 0
b = 100000
while(b < 4800001):
        s = samples[a:b]
        print(a, b, len(s))
        file_name = "comment_set{}.db".format(ver)
        conn = sql.connect(file_name)
        c = conn.cursor()
        c.execute("CREATE TABLE comments(id integer primary key , com_id integer, imdb_id text, body text)")
        for num, row_id in enumerate(s):
                c1.execute("SELECT * FROM comments WHERE id = ?",(row_id,))
                value = c1.fetchall()
                c.execute("INSERT into comments VALUES(?, ?, ?, ? )",(value[0][0],value[0][1],value[0][2],value[0][3]))
                if num%1000 == 0:
                        print("commit {}".format(num))
                        conn.commit()
        conn.close()
        print(ver, a, b)
        a = a + 100000
        b = b + 100000
        ver += 1
        input("check")
conn1.close()
