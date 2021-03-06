""" Utility functions for the Retail Market Project """

def change_detail(stock, detail):
    """ Function for admin to change details of items """

    max_id = len(stock)  # Instead of len() being computed on each iteration.
    progress = 'y'
    while progress == 'y':
        try:
            item_id = int(input("Enter item ID: "))
            if item_id < 1 or item_id > max_id:
                print("Invalid Item ID")
                continue
            value = input("Enter new %s: " % detail)
            if detail != "name":
                value = int(value)
                if value < 0:
                    print("Invalid %s!!" % detail)
                    continue
        except ValueError:
            print("Invalid input!!")
            continue
        else:
            item = stock[item_id - 1]
            item[detail] = value
            print(f"{detail} of '{item['name']}' successfully changed")
        finally:
            progress = input(
                f"Do you want to change the {detail} of another item (y/n)? ").lower()
            while progress != 'y' and progress != 'n':
                print("Invalid Input!!")
                progress = input(
                f"Do you want to change the {detail} of another item (y/n)? ").lower()
    print()


def add_items(stock):
    """ Adds new items to the stock """

    progress = 'y'
    while progress == 'y':
        try:
            name = input("Enter Item Name: ")
            price = int(input("Enter Unit Price of item: "))
            if price < 0:
                print("Invalid price!!")
                continue
            quantity = int(input("Enter item Quantity: "))
            if quantity < 0:
                print("Invalid quantity!!")
                continue
        except ValueError:
            print("Invalid input!!")
            continue
        else:
            # Add only if item doesn't already exists in stock
            for item in stock:
                if item["name"].casefold() == name.casefold():
                    print("'%s' already exists in stock!" % name)
                    break
            else:
                # No matching item in stock
                stock.append({"name": name, "price": price, "quantity": quantity})
                print("New item '%s' successfully added." % name)
        finally:
            progress = input("Do you want to add another item (y/n)? ").lower()
            while progress != 'y' and progress != 'n':
                print("Invalid Input!!")
                progress = input("Do you want to add another item (y/n)? ").lower()
    print()


def make_purchase(stock, purchase):
    """ Computes goods purchased by the customer and displays receipt

    stock: stock data; list of dicts
    purchase: purchase details; dict of the form {id: quantity, ...}
    """

    total = 0
    total_vat = 0
    unit_prices = set()  # To avoid unnecessary repetition

    width = 81
    disp_format = "| {:<30} || {:>8} || {:>3} || {:>10.2f} || {:>10.2f} |"
    print('=' * width)

    print("|%s|" % "RECEIPT".center(width - 2))
    # The above can be acheived thus, using the new style:
    # By using replacement fields within format_spec or another replacement field.
    # print(f"|{'RECEIPT':^{width-2}}|")
    # OR
    # print("|{0:^{1}}|".format("RECEIPT", width-2))
    # This last one is probably the easiest to read
    #
    # The `-2` is because of the two '|' (pipe) characters in the string.

    print('-' * width)
    print("| {:^30} || {:^8} || {:^3} || {:^10} || {:^10} |".format(
        "Item", "Unit (#)", "Qty", "VAT (#)", "Amount (#)"))
    # *Implicit line continuation* applies above
    print('-' * width)
    
    for item_id, quantity in purchase.items():
        item = stock[item_id - 1]
        unit_price = item["price"]
        amount = quantity * unit_price
        unit_prices.add(unit_price)
        
        if quantity < 5:
            vat = amount * 0.2
            amount *= 1.2  # 100% + 20%
        elif quantity > 10:
            vat = amount * 0.3
            amount *= 1.3  # 100% + 30%
        else:
            vat = 0

        print(disp_format.format(item["name"], unit_price, quantity, vat, amount))
        total_vat += vat
        total += amount

    print('-' * width)
    print(disp_format.format("Total", "", "", total_vat, total))
    if len(purchase) > 10 and min(unit_prices) >= 100:
        print('-' * width)
        print("| %s |" % "Bonus Voucher: #800".ljust(width - 4))
        # The above can also be acheived as done for "RECEIPT" above.
        # The `-4` is because of the two '| ' (pipe and space) in the string.
    print('=' * width)
    print()

    return total


def update_stock(stock, purchase):
    """ Update stock after a purchase

    stock: stock data; list of dicts
    purchase: purchase details; dict of the form {id: quantity, ...}
    """

    for item_id, quantity in purchase.items():
        stock[item_id - 1]["quantity"] -= quantity


# Note:
# The global scope of a function/class
# is the scope of the module in which it's defined,
# NOT neccessarily the module in which it's called.
# This comes into play when a function/class is imported and used in another module
# e.g the case of `_gain` in the functions below

def add_gain(amount):
    """ Computes daily gain, using a global variable """
    
    global _gain  # `_gain` will be re-assigned to
    _gain += amount


def view_gain():
    """ Display the day's Total Gain """

    output = f"| Today's Total Gain: {_gain:.2f} |"
    print('=' * len(output))
    print(output)
    print('=' * len(output))
    print()


# A leading underscore automatically makes a global name
# hidden from a wildcard (*) import of this module
# i.e any `from utils import *` in another module
# but it's still visible to functions in this module.
_gain = 0

