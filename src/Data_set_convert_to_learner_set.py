import sqlite3 as sql
from collections import defaultdict

#
# Extracting from final subsets of data into two lists to enter as test and train data in the final learner
# results = list of strings
# box_offices = list of the log base 10 of box office values
# the index of each list corresponds to the same movie imdb_id
#

conn = sql.connect("movie_meta.db")
conn2 = sql.connect("comment_set1.db")

# {imdb_id: [box_office, comments],}
result_dict = defaultdict(list)

c = conn.cursor()
c2 = conn2.cursor()

c2.execute("SELECT DISTINCT imdb_id FROM comments")
unique = c2.fetchall()
unique_list = [x[0] for x in unique]

for x in unique_list:
        if x == 'tconst' : continue
        c.execute("SELECT box_office FROM meta WHERE imdb_id = ?",(x,))
        box_office = c.fetchall()[0][0]
        result_dict[x].append(box_office)
        result_dict[x].append("")

c2.execute("SELECT imdb_id, body FROM comments")
results = c2.fetchall()

for imdb_id, body in results:

        try:
                if imdb_id == 'tconst': continue
                result_dict[imdb_id][1] += body

        except Exception as e:
                continue

reviews = []
box_offices = []
for x, y in result_dict.items():
        box_offices.append(y[0])
        reviews.append(y[1])

print(len(reviews))
print(len(box_offices))
input("waiting...")
f = open("comment_set1.txt", "w", encoding = "utf-8")
f.write(str(reviews))
f.write("\n\n")
f.write(str(box_offices))
f.close()

conn.close()
conn2.close()
