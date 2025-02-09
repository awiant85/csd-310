""" Import statements """
import mysql.connector  # Connect to MySQL
from mysql.connector import errorcode
from dotenv import dotenv_values  # Secure credentials from .env file

# Load environment variables
secrets = dotenv_values(".env")

""" Database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # Enable warnings
}

try:
    """ Try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)  # Connect to the database

    # Output connection status
    print(f"\n ✅ Database user '{config['user']}' connected to MySQL on host '{config['host']}' with database '{config['database']}'.")

    input("\n\n 🔹 Press any key to continue...")

except mysql.connector.Error as err:
    """ Handle errors """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" ❌ The supplied username or password is invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" ❌ The specified database does not exist.")

    else:
        print(err)

finally:
    """ Close the connection to MySQL """
    db.close()

