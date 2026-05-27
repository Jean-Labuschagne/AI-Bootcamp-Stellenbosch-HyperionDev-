import csv
from pathlib import Path


# ========The beginning of the class==========
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return (
            f"Shoe(country={self.country}, code={self.code}, "
            f"product={self.product}, cost={self.cost}, "
            f"quantity={self.quantity})"
        )


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

INVENTORY_FILE = Path(__file__).with_name("inventory.txt")


# ==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file
    represents data to create one object of shoes. You must use the try-except
    in this function for error handling. Remember to skip the first line using
    your code.
    '''
    shoe_list.clear()

    try:
        with INVENTORY_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) != 5:
                    continue
                country, code, product, cost, quantity = row
                try:
                    shoe = Shoe(country, code, product, cost, quantity)
                    shoe_list.append(shoe)
                except ValueError:
                    print(f"Skipping invalid row: {row}")
    except FileNotFoundError:
        print(f"Error: {INVENTORY_FILE.name} not found.")
    except Exception as e:
        print(f"Error while reading file: {e}")


def save_shoes_data():
    """Write current shoe_list back to inventory.txt."""
    try:
        with INVENTORY_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Code", "Product", "Cost", "Quantity"])
            for shoe in shoe_list:
                writer.writerow(
                    [shoe.country, shoe.code, shoe.product, int(shoe.cost),
                     shoe.quantity]
                )
    except Exception as e:
        print(f"Error while saving file: {e}")


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    try:
        country = input("Enter country: ").strip()
        code = input("Enter code (e.g. SKU12345): ").strip()
        product = input("Enter product name: ").strip()
        cost = float(input("Enter cost: ").strip())
        quantity = int(input("Enter quantity: ").strip())

        shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(shoe)
        save_shoes_data()
        print("Shoe added successfully.")
    except ValueError:
        print("Invalid cost or quantity. Shoe not added.")


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    if not shoe_list:
        print("No shoes available.")
        return

    print("\n{:<15} {:<10} {:<22} {:<10} {:<10}".format(
        "Country", "Code", "Product", "Cost", "Quantity"
    ))
    print("-" * 72)
    for shoe in shoe_list:
        print("{:<15} {:<10} {:<22} {:<10.2f} {:<10}".format(
            shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity
        ))


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    if not shoe_list:
        print("No shoes available.")
        return

    lowest_shoe = min(shoe_list, key=lambda s: s.quantity)
    print(f"Lowest stock item: {lowest_shoe}")

    prompt = "Do you want to add stock for this item? (yes/no): "
    choice = input(prompt).strip().lower()
    if choice in ("yes", "y"):
        try:
            add_qty = int(input("How many units to add? ").strip())
            if add_qty < 0:
                print("Quantity must be a positive number.")
                return
            lowest_shoe.quantity += add_qty
            save_shoes_data()
            print("Stock updated successfully.")
        except ValueError:
            print("Invalid quantity.")
    else:
        print("Restock cancelled.")


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    if not shoe_list:
        print("No shoes available.")
        return None

    code = input("Enter shoe code to search: ").strip()
    for shoe in shoe_list:
        if shoe.code.lower() == code.lower():
            print(shoe)
            return shoe

    print("Shoe not found.")
    return None


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    if not shoe_list:
        print("No shoes available.")
        return

    print("\n{:<10} {:<22} {:<10} {:<10} {:<12}".format(
        "Code", "Product", "Cost", "Quantity", "Value"
    ))
    print("-" * 70)
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print("{:<10} {:<22} {:<10.2f} {:<10} {:<12.2f}".format(
            shoe.code, shoe.product, shoe.cost, shoe.quantity, value
        ))


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    if not shoe_list:
        print("No shoes available.")
        return

    highest_shoe = max(shoe_list, key=lambda s: s.quantity)
    print(
        f"\nFOR SALE: {highest_shoe.product} ({highest_shoe.code}) "
        f"- Qty: {highest_shoe.quantity}"
    )


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''


def main():
    read_shoes_data()

    while True:
        print("\n===== SHOE INVENTORY MENU =====")
        print("1. Read shoes data from file")
        print("2. Capture a new shoe")
        print("3. View all shoes")
        print("4. Re-stock lowest quantity shoe")
        print("5. Search shoe by code")
        print("6. Value per item")
        print("7. Show highest quantity shoe (for sale)")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            read_shoes_data()
            print("Data loaded successfully.")
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            view_all()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
