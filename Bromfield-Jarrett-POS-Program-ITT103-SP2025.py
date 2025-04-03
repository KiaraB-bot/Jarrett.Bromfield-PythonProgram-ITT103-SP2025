from datetime import datetime #Only imported, due to the function being used when generating the receipts in cust_receipt
# Product dictionary created, it allows each product to have a specific ID,price and quantity
products = {
    "Milk": {"ID": 7654, "price": 750, "quantity": 12},
    "Rice": {"ID": 7655, "price": 950, "quantity": 13},
    "Flour": {"ID": 7656, "price": 935, "quantity": 16},
    "Sugar": {"ID": 7657, "price": 890, "quantity": 10},
    "Water": {"ID": 7658, "price": 125, "quantity": 16},
    "Eggs": {"ID": 7659, "price": 200, "quantity": 9},
    "Bread": {"ID": 7660, "price": 545, "quantity": 13},
    "Bleach": {"ID": 7661, "price": 465, "quantity": 23},
    "Blender": {"ID": 7662, "price": 160, "quantity": 120},
    "Broom": {"ID": 7663, "price": 795, "quantity": 18},
    "Desk Fan": {"ID": 7664, "price": 895, "quantity": 21},
    "Shopping Bag": {"ID": 7665, "price": 160, "quantity": 120}
}


cust_cart = {} # Customers cart to store the keys and values, to keep track of what's in their cart


# function created to alert cashier when stock quantities are below 5.
def low_stock():
    low_stock_items = [item for item, details in products.items() if details["quantity"] < 5]
    if low_stock_items:
        print("\nThe following items are running low:")
        for item in low_stock_items:
            print(f"- {item} (Only {products[item]['quantity']} left)")


#Function created to add, and keep track of all items the customer has in their cart (cust_cart)
def checkout_cart(item_name, quantity):
    if item_name in products and products[item_name]["quantity"] >= quantity:
        cust_cart[item_name] = cust_cart.get(item_name, 0) + quantity
        products[item_name]["quantity"] -= quantity # after added to cust_cart, the quantity is subtracted from the original quantity, this is just to keep track of stock.
        print(f"{quantity} {item_name}(s) added to cart.")
    else:
        print(f"Unfortunately, there is not enough {item_name} in stock.")



def remove_from_cart():
    product_id = int(input("Enter Product ID to remove: "))
    quantity_to_remove = int(input("Enter quantity to remove: "))

    product_name = None
    for name, details in products.items():
        if details["ID"] == product_id:
            product_name = name
            break

    if product_name and product_name in cust_cart:
        if cust_cart[product_name] >= quantity_to_remove:
            cust_cart[product_name] -= quantity_to_remove
            products[product_name]["quantity"] += quantity_to_remove
            if cust_cart[product_name] == 0:
                del cust_cart[product_name]
            print(f"{quantity_to_remove} {product_name}(s) removed from cart.")
        else:
            print("Not enough quantity in cart to remove.")
    else:
        print("Item not found in cart.")


def view_cart():
    if not cust_cart:
        print("Your cart is empty.")
    else:
        print("\n***********************Viewing Cart*****************************")
        print("{:<20} {:<10} {:<10} {:<10}".format("Item", "Qty", "Price", "Total"))

        for item, qty in cust_cart.items(): # displays all item in cart by looping through it
            price = products[item]["price"]
            total = price * qty
            print("{:<20} {:<10} ${:<10.2f} ${:<10.2f}".format(item, qty, price, total))

        print("\n****************************************************************")


# function created to handle all the arithmethics of the POS, it calculates the total,tax and discounts. It handles the calculation of the cash received and change if required.
def checkout_till():
    subtotal = sum(products[item]["price"] * qty for item, qty in cust_cart.items())
    sales_tax = subtotal * 0.10
    discount = 0.05 * subtotal if subtotal > 5000 else 0
    total_due = subtotal + sales_tax - discount

    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Sales Tax (10%): ${sales_tax:.2f}")
    print(f"Discount (5% for bills over $5000): -${discount:.2f}")
    print(f"Total Due: ${total_due:.2f}")

    while True:
        try:
            total_paid = float(input("Enter amount received: "))
            if total_paid >= total_due:
                change = total_paid - total_due
                print(f"Change due: ${change:.2f}")
                break
            else:
                print("Insufficient amount. Please enter the correct amount.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")



def cust_receipt():
    if not cust_cart:
        print("Your cart is empty. Add items before checking out.")
        return
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n************************************************")
    print("               BEST BUY RETAIL STORE             ")
    print("    123 Main Turn Street, Savanna La Mar,       ")
    print("           Westmoreland, Jamaica                ")
    print("          Phone: +1-876-982-6623                ")
    print("************************************************")

    print("{:<20} {:<10} {:<10} {:<10}".format("Item", "Qty", "Price", "Total"))

    for item, qty in cust_cart.items():
        price = products[item]["price"]
        total = price * qty
        print("{:<20} {:<10} ${:<10} ${:<10}".format(item, qty, price, total))
    print(f"Date & Time: {current_datetime}\n")
    print("************************************************")
    checkout_till() # calls function to handle all calculations
    cust_cart.clear() # empties cart after each checkout is finalized
    print("************************************************")
    print("Thank you for shopping with us!\nCome again soon!")
    print("************************************************")


# All the conditionals for the POS system, based on each selection, specific set of instructions are carried out.
def main():
    while True:
        low_stock()  # Check for low stock at the start of each run
        print("**********Best Buy Retail Store Main Menu**********")
        print("1. View Product Catalog")
        print("2. Add Item to Cart")
        print("3. Remove Item from Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for key, value in products.items():
                print(f"{key}: {value}")

        elif choice == "2":
            product_id = int(input("Enter Product ID: "))

            product_name = None
            for name, details in products.items():
                if details["ID"] == product_id:
                    product_name = name
                    break

            if product_name:
                quantity = int(input(f"Enter quantity for {product_name}: "))
                checkout_cart(product_name, quantity)
            else:
                print("Product not found.")

        elif choice == "3":
            remove_from_cart()

        elif choice == "4":
            view_cart()

        elif choice == "5":
            cust_receipt()

        elif choice == "6":
            print("You chose to exit the point of sales system.\nGoodbye!")
            break

        else:
            print("Invalid option. Please try again.")


main()

