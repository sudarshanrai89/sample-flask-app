import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

users = [(1, 'suddu', 'asdf'),
         (2, 'sarvanan', 'asdf'),
         (3, 'pri', 'xyz')]

insert_query = "insert into users VALUES (?,?,?)"

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print row

connection.commit()

connection.close()
