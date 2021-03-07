import sqlite3
import csv
import os
import datetime as dt

os.chdir('.\\data')

#currentDir = os.getcwd()
#currentFileCSV = currentDir +"\\" + csvFilename
#print(currentFileCSV)

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute("delete from auth_user_customuser")
c.execute("delete from api_title")
c.execute("delete from api_review")
c.execute("delete from api_title_genre")
c.execute("delete from api_genre")
c.execute("delete from api_comment")
c.execute("delete from api_category")

csvFilename = 'users.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        username = row['username']
        email = row['email']
        role = row['role']
        desc = row['description']
        first_name = row['first_name']
        last_name = row['last_name']
        #c.execute("INSERT INTO  auth_user_customuser(username, email, role, bio, first_name, last_name, password, is_superuser, is_staff, is_active, date_joined) \
                  #VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, email, role, desc, first_name, last_name, '111', 0, 0, 1, dt.datetime.now()))

csvFilename = 'titles.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row['name']
        year = row['year']
        cat = row['category']
        c.execute("INSERT INTO  api_title(name, year, category_id) \
                  VALUES(?, ?, ?)", (name, year, cat))


csvFilename = 'review.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        title = row['title_id']
        text = row['text']
        author = row['author']
        score = row['score']
        pub_date = row['pub_date']
        #c.execute("INSERT INTO  api_review(title_id, text, author_id, score, pub_date) \
                  #VALUES(?, ?, ?, ?, ?)", (title, text, author, score, pub_date))

csvFilename = 'genre_title.csv'
with open(csvFilename, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        title = row['title_id']
        text = row['genre_id']
        #c.execute("INSERT INTO  api_title_genre(title_id, genre_id) \
        #          VALUES(?, ?)", (title, text))

csvFilename = 'genre.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row['name']
        slug = row['slug']
        c.execute("INSERT INTO  api_genre(name, slug) \
                  VALUES(?, ?)", (name, slug))

csvFilename = 'comments.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        review_id = row['review_id']
        text = row['text']
        author = row['author']
        pub_date = row['pub_date']
        #c.execute("INSERT INTO  api_comment(review_id, text, author_id, pub_date) \
        #          VALUES(?, ?, ?, ?)", (review_id, text, author, pub_date))

csvFilename = 'category.csv'
with open(csvFilename, "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row['name']
        slug = row['slug']
        c.execute("INSERT INTO  api_category(name, slug) \
                  VALUES(?, ?)", (name, slug))

conn.commit()
conn.close()