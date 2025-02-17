import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Monsterhound6^6^",
    database="movies"
)

cursor = db.cursor()

# Query 1: Displaying Studio Records
print("\n-- DISPLAYING Studio RECORDS --")
cursor.execute("SELECT studio_id, studio_name FROM studio;")
studios = cursor.fetchall()
for studio in studios:
    print(f"Studio ID: {studio[0]}\nStudio Name: {studio[1]}\n")

# Query 2: Displaying Genre Records
print("\n-- DISPLAYING Genre RECORDS --")
cursor.execute("SELECT genre_id, genre_name FROM genre;")
genres = cursor.fetchall()
for genre in genres:
    print(f"Genre ID: {genre[0]}\nGenre Name: {genre[1]}\n")

# Query 3: Displaying Short Films (Runtime < 2 Hours)
print("\n-- DISPLAYING Short Film RECORDS --")
cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
short_films = cursor.fetchall()
for film in short_films:
    print(f"Film Name: {film[0]}\nRuntime: {film[1]}\n")

# Query 4: Displaying Films Grouped by Director
print("\n-- DISPLAYING Director RECORDS in Order --")
cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director;")
films_by_director = cursor.fetchall()
for film in films_by_director:
    print(f"Film Name: {film[0]}\nDirector: {film[1]}\n")

# Close the connection
cursor.close()
db.close()
