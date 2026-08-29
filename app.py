import streamlit as st
import pandas as pd
from pathlib import Path


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Retail AI",
    page_icon="🛒",
    layout="wide"
)


# ==========================================
# FILE SETUP
# ==========================================

DATA_FILE = Path("data/inventory.csv")
DATA_FILE.parent.mkdir(exist_ok=True)


# ==========================================
# LOAD INVENTORY
# ==========================================

def load_inventory():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)

        # Make sure old inventory files also work
        required_columns = [
            "Product Name",
            "Brand",
            "Stock Type",
            "One Item Quantity",
            "Unit",
            "Current Stock",
            "Minimum Stock",
            "Price"
        ]

        for column in required_columns:
            if column not in df.columns:
                if column == "Brand":
                    df[column] = "No Brand"
                else:
                    df[column] = 0

        return df[required_columns]

    # Empty inventory
    return pd.DataFrame(
        columns=[
            "Product Name",
            "Brand",
            "Stock Type",
            "One Item Quantity",
            "Unit",
            "Current Stock",
            "Minimum Stock",
            "Price"
        ]
    )


# ==========================================
# SAVE INVENTORY
# ==========================================

def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)


# ==========================================
# STOCK STATUS FUNCTION
# ==========================================

def get_stock_status(current_stock, minimum_stock):
    """
    Return the stock status based on current stock
    compared with the minimum stock level.

    Rules:
    - 0 stock                    -> Out of Stock
    - 1% to 50% of minimum      -> Very Low
    - >50% to 100% of minimum   -> Low
    - Above minimum             -> Good
    """

    current_stock = float(current_stock)
    minimum_stock = float(minimum_stock)

    # Out of stock
    if current_stock == 0:
        return "Out of Stock"

    # If minimum stock is 0, we cannot calculate a percentage.
    # Any positive stock is considered Good.
    if minimum_stock <= 0:
        return "Good"

    # Very Low Stock: 50% or less of minimum stock
    if current_stock <= (minimum_stock * 0.50):
        return "Very Low"

    # Low Stock: above 50% and up to minimum stock
    if current_stock <= minimum_stock:
        return "Low"

    # Above minimum stock
    return "Good"


# ==========================================
# LOAD DATA
# ==========================================

inventory = load_inventory()


# ==========================================
# TITLE
# ==========================================

st.title("🛒 Smart Retail AI")
st.subheader("AI-Powered Inventory & Price Prediction System")

st.divider()


# ==========================================
# ADD NEW PRODUCT
# ==========================================

st.header("➕ Add New Product")

with st.container(border=True):

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="Example: Sugar"
        )

    with col2:
        brand = st.text_input(
            "Brand (Optional)",
            placeholder="Example: Gemini"
        )

    with col3:
        stock_type = st.selectbox(
            "Stock Type",
            [
                "Bag",
                "Box",
                "Packet",
                "Bottle",
                "Piece",
                "Bundle",
                "Can",
                "Jar",
                "Other"
            ]
        )

    # Row 2
    col4, col5, col6 = st.columns(3)

    with col4:
        one_item_quantity = st.number_input(
            f"Quantity in One {stock_type}",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    with col5:
        unit = st.selectbox(
            "Unit",
            [
                "kg",
                "g",
                "litre",
                "ml",
                "piece"
            ]
        )

    with col6:
        current_stock = st.number_input(
            f"Current Stock ({stock_type}s)",
            min_value=0,
            value=0,
            step=1
        )

    # Row 3
    col7, col8 = st.columns(2)

    with col7:
        minimum_stock = st.number_input(
            f"Minimum Stock ({stock_type}s)",
            min_value=0,
            value=0,
            step=1
        )

    with col8:
        price = st.number_input(
            f"Price of One {stock_type} (₹)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    # Add button
    if st.button("Add Product", type="primary"):

        # Validation
        if not product_name.strip():
            st.error("Please enter the product name.")

        elif one_item_quantity <= 0:
            st.error(
                f"Quantity in one {stock_type.lower()} "
                "must be greater than 0."
            )

        elif current_stock < 0:
            st.error("Current stock cannot be negative.")

        else:

            # If brand is empty
            if not brand.strip():
                brand = "No Brand"

            # Check for duplicate product
            duplicate = (
                (inventory["Product Name"].astype(str).str.lower()
                 == product_name.strip().lower())
                &
                (inventory["Brand"].astype(str).str.lower()
                 == brand.strip().lower())
                &
                (inventory["Stock Type"].astype(str).str.lower()
                 == stock_type.lower())
                &
                (inventory["One Item Quantity"]
                 == one_item_quantity)
                &
                (inventory["Unit"].astype(str).str.lower()
                 == unit.lower())
            )

            if duplicate.any():
                st.error(
                    "This product with the same brand, stock type "
                    "and quantity already exists!"
                )

            else:

                new_product = pd.DataFrame(
                    [{
                        "Product Name": product_name.strip(),
                        "Brand": brand.strip(),
                        "Stock Type": stock_type,
                        "One Item Quantity": one_item_quantity,
                        "Unit": unit,
                        "Current Stock": current_stock,
                        "Minimum Stock": minimum_stock,
                        "Price": price
                    }]
                )

                inventory = pd.concat(
                    [inventory, new_product],
                    ignore_index=True
                )

                save_inventory(inventory)

                st.success(
                    f"✅ {product_name.strip()} added successfully!"
                )

                st.rerun()


# ==========================================
# DASHBOARD
# ==========================================

st.divider()

st.header("📊 Inventory Dashboard")

total_products = len(inventory)

# Default values
out_of_stock = 0
very_low_stock = 0
low_stock = 0
good_stock = 0

if len(inventory) > 0:

    # Count every stock category
    for _, row in inventory.iterrows():

        status = get_stock_status(
            row["Current Stock"],
            row["Minimum Stock"]
        )

        if status == "Out of Stock":
            out_of_stock += 1

        elif status == "Very Low":
            very_low_stock += 1

        elif status == "Low":
            low_stock += 1

        elif status == "Good":
            good_stock += 1


# ==========================================
# DASHBOARD CARDS
# ==========================================

dash1, dash2, dash3, dash4, dash5 = st.columns(5)

with dash1:
    st.markdown("📦 **Total Products**")
    st.subheader(total_products)

with dash2:
    st.markdown("🟢 **Good Stock**")
    st.subheader(good_stock)

with dash3:
    st.markdown("🟡 **Low Stock**")
    st.subheader(low_stock)

with dash4:
    st.markdown("🟠 **Very Low Stock**")
    st.subheader(very_low_stock)

with dash5:
    st.markdown("🔴 **Out of Stock**")
    st.subheader(out_of_stock)


# ==========================================
# CURRENT INVENTORY
# ==========================================

st.divider()

st.header("📋 Current Inventory")

if len(inventory) == 0:

    st.info("No products added yet.")

else:

    display_data = []

    for _, row in inventory.iterrows():

        # Total available quantity
        total_available = (
            float(row["One Item Quantity"])
            *
            int(row["Current Stock"])
        )

        # Format quantity
        if total_available.is_integer():
            total_available = int(total_available)

        total_available_text = (
            f"{total_available} {row['Unit']}"
        )

        # One item description
        one_item_text = (
            f"{row['One Item Quantity']} {row['Unit']} / "
            f"{row['Stock Type']}"
        )

        # Current stock description
        current_stock_text = (
            f"{int(row['Current Stock'])} {row['Stock Type']}s"
        )

        # New stock status
        stock_status = get_stock_status(
            row["Current Stock"],
            row["Minimum Stock"]
        )

        # Display label
        if stock_status == "Out of Stock":
            status = "🔴 Out of Stock"

        elif stock_status == "Very Low":
            status = "🟠 Very Low"

        elif stock_status == "Low":
            status = "🟡 Low"

        else:
            status = "🟢 Good"

        display_data.append(
            {
                "Product Name": row["Product Name"],
                "Brand": row["Brand"],
                "Stock Type": row["Stock Type"],
                "One Item": one_item_text,
                "Current Stock": current_stock_text,
                "Total Available": total_available_text,
                "Price per Stock Type":
                    f"₹{float(row['Price']):,.2f}",
                "Status": status
            }
        )

    display_df = pd.DataFrame(display_data)

    # Start table index from 1 instead of 0
    display_df.index = range(1, len(display_df) + 1)

    st.dataframe(
        display_df,
        use_container_width=True
    )


# ==========================================
# INVENTORY ALERTS
# ==========================================

st.divider()

st.header("⚠️ Inventory Alerts")

if len(inventory) == 0:

    st.info("Add products to see inventory alerts.")

else:

    alert_products = []

    for _, row in inventory.iterrows():

        stock_status = get_stock_status(
            row["Current Stock"],
            row["Minimum Stock"]
        )

        if stock_status == "Out of Stock":

            alert_products.append(
                (
                    "error",
                    f"🔴 {row['Product Name']} is out of stock!"
                )
            )

        elif stock_status == "Very Low":

            alert_products.append(
                (
                    "warning",
                    f"🟠 {row['Product Name']} is very low "
                    "on stock. Reorder urgently."
                )
            )

        elif stock_status == "Low":

            alert_products.append(
                (
                    "info",
                    f"🟡 {row['Product Name']} is running low. "
                    "Consider planning a reorder."
                )
            )


    if len(alert_products) == 0:

        st.success("🟢 All products have sufficient stock.")

    else:

        for alert_type, alert_message in alert_products:

            if alert_type == "error":
                st.error(alert_message)

            elif alert_type == "warning":
                st.warning(alert_message)

            else:
                st.info(alert_message)