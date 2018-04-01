#DESCRIPTION#

#################
## This file handles gathering data from IMDB provided TSV files, scraping IMDB for budgets,
## adding reviews & review counts into a SQLite database
#################


import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import sqlite3
import datetime


import tmdbsimple as tmdb

# keys and variables needed for tmdb & sqlite db connection
tmdb.API_KEY = '3efa96c281aa6090e6d8eba717fee22f'
sqlite_file = "C:\\Users\\Jenny Kim\\Documents\\CS175\\my_db.sqlite"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# get_titles_and_year uses the imdb provided tsv to get the imdb_id, titles & year for all movies
def get_titles_and_year(file):
    length = 0
    total = 0
    # tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
    with open(file, encoding='utf-8') as tsvfile, open('movie_year.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvfile = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        tsvfile = csv.reader(tsvfile, delimiter="\t", quotechar='"')
        for row in tsvfile:
            total += 1
            print(total)
            titleType = row[1]
            title = row[2]
            year = row[5]
            tconst = row[0]
            print(title, year == '\\N')
            if titleType == 'movie' and year != '\\N' and int(year) > 2005:
                length += 1
                csvfile.writerow([tconst, title, year])

    print("closing...")
    print(length)
    tsvfile.close()
    csvfile.close()
    return


# gathers all the movie data and inserting it into a CSV file
def scrape_movie_data(csv_filename):
    print("START")
    count = 1
    with open('new_movie_metadata.csv', 'a', newline='', encoding='utf-8') as moviecsv, \
        open(csv_filename, 'r',encoding='utf-8') as input_file:
        movie_writer = csv.writer(moviecsv, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # movie_writer.writerow(['tconst', 'Title', 'Year', 'BoxOffice', 'ReleaseDate', 'Genre', 'Director', 'MainActor', 'Budget'])
        input_file = csv.DictReader(input_file)
        for line in input_file:
            if count > 949:
                tconst = line['tconst']
                title = line['Title']
                boxOffice = line['BoxOffice']
                try:
                    int(boxOffice)
                except:
                    boxOffice = boxOffice.split(".")[0]
                    boxOffice = re.sub('[^0-9]+', '', boxOffice)
                budget = get_budget(tconst, title)
                movie_writer.writerow([tconst, title, line['Year'], boxOffice, line['ReleaseDate'],
                                      line['Genre'], line['Director'], line['MainActor'], budget])
                print("just finished line: " + str(count) + "\n")
            count += 1


# scrapes IMDB budget from each movie page
def get_imdb_budget(imdb_id, title):
    url = 'http://www.imdb.com/title/' + imdb_id
    try:
        res = requests.get(url)
    except:
        print("         SLEEPING.......")
        time.sleep(5)
        res = requests.get(url)

    broth = BeautifulSoup(res.text,"lxml")

    #budget
    try:
        txt_block = broth.select('.txt-block')
        budget_block = txt_block[9]
        budget = list(budget_block)[2].strip()
        budget = re.sub('[^0-9]+', '', budget)

        budget = 0 if budget == "" else budget
    except:
        budget = "LOOKINTO"

    print(title + ": " + str(budget))

    return budget


# uses the TMDB api to get budgets. We tried both IMDB web scraping and TMDB to get budgets & see
# which one did better in our learners. The IMDB web scraping results did better.
def get_budget(imdb_id, title):
    try:
        movie = tmdb.Movies(imdb_id)
        results = movie.info()
        budget = results["budget"]
        print(title+ ": $"+str(budget))
        return budget
    except:
        print("client error for: ", imdb_id, title)


def get_review_scores():
    with open('tester.txt', 'r', encoding='utf-8') as reviewscsv:
        reviewscsv = csv.DictReader(reviewscsv)
        for line in reviewscsv:
            score = line["score"]
            print(score)

# Returns true if comment is within 3 weeks of movie release
def three_weeks(release, comment_date):
    # Parsing the movie release date
    final_rel = datetime.datetime.strptime(release, '%d %b %Y')

    # Adding 3 weeks to the release date
    added = datetime.timedelta(days=21)
    cap_list = str((final_rel + added)).split(" ")[0].split("-")

    # Parsing the comment date
    final_comment = datetime.datetime.strptime(comment_date, '%d %B %Y')
    comment_list = str((final_comment)).split(" ")[0].split("-")

    return datetime.date(int(comment_list[0]), int(comment_list[1]), int(comment_list[2])) <= datetime.date(
        int(cap_list[0]), int(cap_list[1]), int(cap_list[2]))


# Creates and populate SQLite database w/ tables for movies & review counts.
def add_review_scores():
    # Creates table for reviews
    c.execute("DROP TABLE  IF EXISTS reviews")
    sql_create_table = """ CREATE TABLE IF NOT EXISTS reviews (
                                            id integer PRIMARY KEY,
                                            imdb_id text NOT NULL,
                                            title text,
                                            date text,
                                            score text
                                        ); """
    c.execute(sql_create_table)

    # Inserting all movies into database
    with open('reviews.csv', 'r', encoding='utf-8') as reviewscsv:
        reviewscsv = csv.DictReader(reviewscsv)
        for line in reviewscsv:
            imdb_id = line["imdb_id"]
            title = line["title"]
            date = line["date"]
            score = line["score"]
            stmt = "INSERT INTO reviews (imdb_id, date, score) VALUES (\"{0}\", \"{1}\", \"{2}\")".format(imdb_id, date,
                                                                                                          score)
            print(stmt)
            c.execute(stmt)

    conn.commit()

    # Creates table for movies
    c.execute("DROP TABLE  IF EXISTS movies")
    sql_create_table = """ CREATE TABLE IF NOT EXISTS movies (
                                            id integer PRIMARY KEY,
                                            imdb_id text NOT NULL,
                                            title text,
                                            year text,
                                            box text,
                                            release text,
                                            genre text,
                                            director text,
                                            main_actor text
                                        ); """

    c.execute(sql_create_table)

    # Inserting all movies into database
    file = open('all_metadata.csv', 'r', encoding="utf-8")
    csv_reader = csv.reader(file, delimiter=',')

    stmt = "INSERT INTO movies (imdb_id, title, year, box, release, genre, director, main_actor) " \
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    c.executemany(stmt, csv_reader)
    conn.commit()
    file.close()

    # Creates table for review scores average within 3 weeks
    c.execute("DROP TABLE  IF EXISTS reviews_score_three")
    sql_create_table = """ CREATE TABLE IF NOT EXISTS reviews_score_three (
                                            id integer PRIMARY KEY,
                                            imdb_id text NOT NULL,
                                            len integer,
                                            review_scores integer
                                        ); """
    c.execute(sql_create_table)

    # Inserting all movies into database
    conn.commit()

    # Getting all movies in the database and appending all of their movies into one string, then adding it to a new table
    movie_rows = c.execute("SELECT imdb_id, release FROM movies").fetchall()
    count = 0

    batch_insert = []
    for movie in movie_rows:
        count += 1
        if count > 1:
            total_score = 0
            score_count = 0
            avg_score = 0
            imdb_id = movie[0]
            movie_release = movie[1]

            score_rows = c.execute("SELECT date, score FROM reviews where imdb_id = '" + imdb_id + "'").fetchall()
            print("# of reviews: " + str(len(score_rows)))
            if len(score_rows) > 0:
                for row in score_rows:
                    try:
                        if three_weeks(movie_release.strip(), row[0].strip()) and row[1] != "None":
                            total_score += int(row[1])
                            score_count += 1
                    except:
                        print("Formatting does not match: {},{}".format(movie_release, row[0]))
                stmt = "INSERT INTO reviews_score_three (imdb_id, len, review_scores) VALUES (?, ?, ?)"
                if score_count > 0:
                    avg_score = total_score / score_count
                    data = (imdb_id, score_count, avg_score)
                    c.execute(stmt, data)
                    conn.commit()
                print("{}, total score: {}, score count: {}, avg score: {}".format(imdb_id, total_score, score_count,
                                                                                   avg_score))
            else:
                print(imdb_id + " no reviews~!")
            print("current count: " + str(count))




# get_titles_and_year("data.tsv")
# get_titles_and_year("tester.txt.txt")

# scrape_movie_data('movie_metadata.csv')
# show_no_budget_movies()
add_review_scores()
# get_budget("tt0200465", "The Bank Job")