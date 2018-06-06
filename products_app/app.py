import csv
import os

def menu(username="@rkober3", products_count= 100):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu


def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            #print("#",row["id"],":",row["name"])
            products.append(row)
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id","name","aisle","department","price"])
        writer.writeheader() # uses fieldnames set above
        for p  in products:
            writer.writerow(p)


def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

def run():
    # First, read products from file...
    products = read_products_from_file()
    all_ids =[]
    for p in products:
        all_ids.append(p["id"])
    # Then, prompt the user to select an operation...
    operation = input(menu(username="@Cool_Guy", products_count = len(products))) #TODO instead of printing, capture user input
    operation = operation.title()
    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    if operation == "List":
        for p in products:
            print("#",p["id"],":",p["name"].title())

    elif operation == "Show":
        pid = input("Enter a product ID to be displayed:")
        search_pid = int(pid)
        def matching_product(product_identifier = pid):
            products_list = [p for p in products if p["id"] == product_identifier]
            return products_list [0]

        if pid not in all_ids:
            print("Product not found")
        else:
            print("--------------------------")
            print("SHOWING A PRODUCT:")
            print("--------------------------")
            print(dict(matching_product(pid)))

    elif operation == "Create":
        all_ids = [int(p["id"])for p in products]
        new_id = max(all_ids)+1
        def matching_product(product_identifier):
            new_item = [p for p in products if p["id"] == product_identifier]
            return new_item[0]

        new_name = input("OK. Please input the product's 'name':")
        new_aisle = input("OK. Please input the product's 'aisle':")
        new_department = input("OK. Please input the product's 'department':")
        new_price = input("OK. Please input the product's 'price':")

#####Trying to get the price formatting right, unsuccessfully:
      # while True:
    #        try:
    #            new_price = float(input("Enter the price: "))
    #            if new_price % 1 == 0:
    #                print("Invalid input for price.")
    #
    #            else:
    #                if new_price > 0:
    #                    return new_price
    #        except ValueError:
    #       #     print("Invalid input for price.")
        new_product ={"id":new_id,"name":new_name,"aisle":new_aisle,"department":new_department,"price":new_price}
        products.append(new_product)
        print("--------------------------")
        print("CREATING A PRODUCT:")
        print("--------------------------")
        print(dict(products[len(products)-1]))

    elif operation == "Update":
        pid = input("Enter which product would you like to display for update: ")

        if pid not in all_ids:
            print("Product not found")
        else:
            matching_products = [p for p in products if int(p["id"]) == int(pid)]
            matching_product = matching_products[0]
            new_name = input("OK. Please input the product's new 'name'(currently ''"+ str(matching_product["name"])+"'):")
            new_aisle = input("OK. Please input the product's new 'aisle'(currently ''"+str(matching_product["aisle"])+"'):")
            new_department = input("OK. Please input the product's new 'department'(currently ''"+str(matching_product["department"])+"'):")
            new_price = input("OK. Please input the product's new 'price'(currently ''"+str(matching_product["price"])+"'):")

            matching_product["name"] = new_name
            matching_product["aisle"] = new_aisle
            matching_product["department"] = new_department
            matching_product["price"] = new_price
            print("--------------------------")
            print("UPDATING A PRODUCT")
            print("--------------------------")
            print(dict(matching_product))

    elif operation == "Destroy":
        product_id = input("Enter which product would you like to destroy: ")
        if product_id not in all_ids:
            print("Product not found")
        else:
            matching_products = [p for p in products if int(p["id"]) == int(product_id)]
            matching_product = matching_products[0]
            del products[products.index(matching_product)]
            print("--------------------------")
            print("DESTROYING A PRODUCT")
            print("--------------------------")
            print(dict(matching_product))


    elif operation == "Reset":
        reset_products_file()
        return #The note here was very helpful when you posted the code you wrote in class to slack

    else:
        print("Sorry, that's not valid, please run the app and try again")

    write_products_to_file(products=products)

#def auto_inc_id(products):
#    all_ids = [int(p["id"])for p in products]
#    max_id = max(all_ids)+1
#    return max_id
#def enlarge(my_number):
#    return my_number*100

    # Finally, save products to file so they persist after script is done...
    #write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
