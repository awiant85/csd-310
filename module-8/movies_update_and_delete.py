import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Monsterhound6^6^",
        database="movies"
    )

# ✅ Function to display films
def show_films(cursor, title):
    print(f"\n-- {title} --")
    query = """
    SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS Studio
    FROM film
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id;
    """
    cursor.execute(query)
    films = cursor.fetchall()
    
    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre: {film[2]}\nStudio: {film[3]}\n")

def main():
    db = connect_db()
    cursor = db.cursor()

    # 📌 Step 1: Ensure "Gladiator" exists before displaying films
    cursor.execute("""
        INSERT INTO film (film_name, film_releaseDate, film_director, film_runtime, studio_id, genre_id)
        SELECT 'Gladiator', 2000, 'Ridley Scott', 155, 
               (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures' LIMIT 1),
               (SELECT genre_id FROM genre WHERE genre_name = 'Drama' LIMIT 1)
        WHERE NOT EXISTS (
            SELECT 1 FROM film WHERE film_name = 'Gladiator' AND film_director = 'Ridley Scott'
        );
    """)
    db.commit()

    # 📌 Step 2: Display films (Gladiator is now present)
    show_films(cursor, "DISPLAYING FILMS")

    # 📌 Step 3: Delete duplicate "Titanic" entries (Keep only one)
    cursor.execute("""
        DELETE FROM film 
        WHERE film_name = 'Titanic' 
        AND film_id NOT IN (
            SELECT film_id FROM (
                SELECT MIN(film_id) AS film_id FROM film WHERE film_name = 'Titanic'
            ) AS temp
        );
    """)
    db.commit()

    # 📌 Step 4: Insert "Titanic" if it doesn't exist
    cursor.execute("""
        INSERT INTO film (film_name, film_releaseDate, film_director, film_runtime, studio_id, genre_id)
        SELECT 'Titanic', 1997, 'James Cameron', 195, 
               (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox' LIMIT 1),
               (SELECT genre_id FROM genre WHERE genre_name = 'Drama' LIMIT 1)
        WHERE NOT EXISTS (
            SELECT 1 FROM film WHERE film_name = 'Titanic' AND film_director = 'James Cameron'
        );
    """)
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 📌 Step 5: Update "Alien" to Horror
    cursor.execute("""
        UPDATE film 
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror' LIMIT 1)
        WHERE film_name = 'Alien' LIMIT 1;
    """)
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # 📌 Step 6: Delete "Gladiator" (Only at the End)
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator' LIMIT 1;")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    # ✅ Close database connection
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
