# inventory.py

# Inventory Management Module

# Dictionary to store products
# Format:
# product_id: {
#     "name": product name,
#     "quantity": available quantity,
#     "price": product price
# }

inventory = {}

# Minimum quantity before a low-stock alert is shown
LOW_STOCK_LIMIT = 5


def add_product(product_id, name, quantity, price):
    """Add a new product to the inventory."""

    if product_id in inventory:
        print("Product already exists.")
        return False

    inventory[product_id] = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    print(f"Product '{name}' added successfully.")
    return True


def update_quantity(product_id, quantity):
    """Update the quantity of an existing product."""

    if product_id not in inventory:
        print("Product not found.")
        return False

    if quantity < 0:
        print("Quantity cannot be negative.")
        return False

    inventory[product_id]["quantity"] = quantity

    print(
        f"Quantity of '{inventory[product_id]['name']}' "
        f"updated to {quantity}."
    )

    return True


def delete_product(product_id):
    """Delete a product from the inventory."""

    if product_id not in inventory:
        print("Product not found.")
        return False

    product_name = inventory[product_id]["name"]
    del inventory[product_id]

    print(f"Product '{product_name}' deleted successfully.")
    return True


def display_inventory():
    """Display all products currently in inventory."""

    if not inventory:
        print("Inventory is empty.")
        return

    print("\n========== CURRENT INVENTORY ==========")

    print(
        f"{'ID':<10}"
        f"{'Product Name':<25}"
        f"{'Quantity':<12}"
        f"{'Price':<10}"
    )

    print("-" * 57)

    for product_id, product in inventory.items():
        print(
            f"{product_id:<10}"
            f"{product['name']:<25}"
            f"{product['quantity']:<12}"
            f"₹{product['price']:<10.2f}"
        )

    print("=" * 57)


def low_stock_alert():
    """Display products whose quantity is below the low-stock limit."""

    low_stock_products = []

    for product_id, product in inventory.items():
        if product["quantity"] <= LOW_STOCK_LIMIT:
            low_stock_products.append(
                (product_id, product)
            )

    if not low_stock_products:
        print("\nNo low-stock products.")
        return

    print("\n========== LOW STOCK ALERT ==========")

    for product_id, product in low_stock_products:
        print(
            f"⚠️ {product['name']} "
            f"(ID: {product_id}) - "
            f"Only {product['quantity']} left!"
        )

    print("=" * 38)


def get_product(product_id):
    """Return product details."""

    if product_id not in inventory:
        return None

    return inventory[product_id]


def search_product(product_id):
    """Search for a product and display its details."""

    product = get_product(product_id)

    if product is None:
        print("Product not found.")
        return None

    print("\nProduct Details")
    print("----------------------")
    print(f"ID       : {product_id}")
    print(f"Name     : {product['name']}")
    print(f"Quantity : {product['quantity']}")
    print(f"Price    : ₹{product['price']:.2f}")

    return product


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    # Add products
    add_product("P001", "Rice 5kg", 20, 350)
    add_product("P002", "Milk 1L", 3, 60)
    add_product("P003", "Bread", 10, 45)

    # Display inventory
    display_inventory()

    # Update quantity
    update_quantity("P002", 8)

    # Search product
    search_product("P001")

    # Low stock check
    low_stock_alert()

    # Delete product
    delete_product("P003")

    # Display final inventory
    display_inventory()
