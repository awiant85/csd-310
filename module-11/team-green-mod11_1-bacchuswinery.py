# Name: Justin Morrow
# Team Green: Austin, Justin, Mark, and Tabari
# Date: 02/26/2025
# Assignment: CSD310 Module 11.1 "Bacchus Winery Mile Stone 3 - Python Query to MySQL Database"
# Modified Code from: CSD310 Module 10.1 "Bacchus Winery Mile Stone 2 - Python Query to MySQL Database"
# Updates include a user menu to choose a report. Now we have functions to streamline the reporting options


""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

# Adding this for reference of the current date/time. Formated to display AM/PM for the comment at the end of the report
from datetime import datetime
current_date_time = datetime.now()
formatted_date_time = current_date_time.strftime("%m-%d-%Y %I:%M:%S %p")

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

database_name = secrets["DATABASE"]


# This function will be used to show the suppliers and supplier_deliveries data as a report. User selects option # 1
def suppliers_report(cursor):
    print("\n************************************************************************************************")
    print(f"\n\nBracchus Winery Delivery Schedule Report     |     Generated on: {formatted_date_time}\n\n")
    cursor.execute("""
        SELECT supplier_deliveries.delivery_id, suppliers.supplier_name, supplier_deliveries.item_type, 
        supplier_deliveries.expected_delivery_date, supplier_deliveries.actual_delivery_date, supplier_deliveries.quantity_delivered
        FROM supplier_deliveries
        JOIN suppliers ON supplier_deliveries.supplier_id = suppliers.supplier_id
    """)
    deliveries = cursor.fetchall()
    for delivery in deliveries:
        print(f"Delivery ID: {delivery[0]}")
        print(f"Supplier Name: {delivery[1]}")
        print(f"Item Type: {delivery[2]}")
        print(f"Expected Delivery Date: {delivery[3]}")
        print(f"Actual Delivery Date: {delivery[4]}")
        expected_delivery_date = delivery[3] # Tuple to store the expected delivery date
        actual_delivery_date = delivery[4] # Tuple to store the actual delivery date
        if actual_delivery_date == expected_delivery_date: # If statement to calculate if the delivery was on time
            print("Shipment Delivery: On time")
        else:
            print("Shipment Delivery: Was late")
        print(f"Quantity Delivered: {delivery[5]:,.0f}\n")
    print("\nAll Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.\n\n")
    print("\n************************************************************************************************\n\n")


# This function will be used to show the distributors and wine_sales data as a report. User selects option # 2
def distributors_report(cursor):
    print("\n************************************************************************************************")
    print(f"\n\nBracchus Winery Wine Sales Report     |     Generated on: {formatted_date_time}\n\n")
    cursor.execute("""
        SELECT wine_grape_variety.wine_name, distributors.distributor_name, wine_sales.sales_quantity, wine_sales.sale_date, wine_sales.price_per_unit
        FROM wine_sales
        JOIN wine_grape_variety ON wine_sales.product_id = wine_grape_variety.product_id
        JOIN distributors ON wine_sales.distributor_id = distributors.distributor_id
    """)
    wine_sales = cursor.fetchall()
    for sale in wine_sales:
        print(f"Wine Name: {sale[0]}")
        print(f"Distributor: {sale[1]}")
        print(f"Sales Quantity: {sale[2]:,.0f}")
        print(f"Sale Date: {sale[3]}")
        print(f"Price per Unit: ${sale[4]:,.2f}")
        total_sales = sale[2] * sale[4] # Calculation of Sales Quantity (Bottles sold) * Price per Unit (Cost of each bottle)
        print(f"Total Sales: ${total_sales:,.2f}\n")
    print("All Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.")
    print("\n************************************************************************************************\n\n")


# This function will be used to show the employees data as a report. User selects option # 3
def employees_report(cursor):
    print("\n************************************************************************************************")
    print(f"\n\nBracchus Winery Employee Worked Hours Report     |     Generated on: {formatted_date_time}\n\n")
    cursor.execute("SELECT employee_id, first_name, last_name, position, total_hours_worked FROM employees")
    employees = cursor.fetchall()
    for employee in employees:
        print(f"Employee ID: {employee[0]}")
        print(f"First Name: {employee[1]}")
        print(f"Last Name: {employee[2]}")
        print(f"Position: {employee[3]}")
        print(f"Total (4 Quarters) Hours Worked: {employee[4]:,.0f}\n")
    print("All Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.")
    print("\n************************************************************************************************\n\n")


def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        print("\nWelcome to the Bacchus Winery Report Tool")

        # Display menu for the user to select a report or quit
        while True:
            print("\nPlease select a report to generate:")
            print("1) Suppliers and Delivery Schedule Report")
            print("2) Distributors and Wine Sales Report")
            print("3) Employee Hours Worked Report")
            print("Q) Quit")

            choice = input("\nEnter the number of your choice to display the report: ")

            if choice == "1":
                suppliers_report(cursor)
            elif choice == "2":
                distributors_report(cursor)
            elif choice == "3":
                employees_report(cursor)
            elif choice.upper() == "Q":
                print("\n\nThe database connection will now automatically disconnect...")
                break
            else:
                print("\nInvalid choice. Please enter a number: 1-3 to view a report, or Q to Quit.\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        else:
            print(err)

    finally:
        db.close()

if __name__ == "__main__":
    main()