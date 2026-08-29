"""
Smart Retail AI - Demand Prediction Module

This module predicts future product demand using historical sales data.

Expected data columns:
- date: Date of sale
- product_id: Product ID
- sales: Number of units sold
"""

import pandas as pd


def prepare_sales_data(data):
    """
    Clean and prepare historical sales data.

    Returns:
        Cleaned pandas DataFrame
    """

    # Make a copy so the original data is not changed
    data = data.copy()

    # Required columns
    required_columns = ["date", "product_id", "sales"]

    # Check whether required columns exist
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing required column: {column}")

    # Convert date into datetime format
    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    # Convert sales values into numbers
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")

    # Remove rows with missing date, product ID, or sales
    data = data.dropna(
        subset=["date", "product_id", "sales"]
    )

    # Sales cannot be negative
    data = data[data["sales"] >= 0]

    # Sort sales data by date
    data = data.sort_values("date")

    return data


def predict_demand(data, product_id, days_to_predict=7):
    """
    Predict future demand for a product.

    The prediction is based on the average sales
    from the most recent 7 records.

    Args:
        data: Historical sales DataFrame
        product_id: Product ID to predict
        days_to_predict: Number of future days

    Returns:
        Dictionary containing the prediction
    """

    # Make sure the data is clean
    data = prepare_sales_data(data)

    # Select sales for the requested product
    product_data = data[
        data["product_id"] == product_id
    ]

    # Check if there is enough historical data
    if len(product_data) < 3:
        return {
            "product_id": product_id,
            "predicted_daily_demand": 0,
            "predicted_total_demand": 0,
            "days": days_to_predict,
            "status": "insufficient_data",
            "message": "Not enough historical sales data."
        }

    # Take the most recent 7 sales records
    recent_sales = product_data["sales"].tail(7)

    # Calculate average sales
    average_demand = recent_sales.mean()

    # Round to a whole number because products
    # are normally sold as whole units
    predicted_daily_demand = round(average_demand)

    # Calculate expected demand for the requested period
    predicted_total_demand = (
        predicted_daily_demand * days_to_predict
    )

    # Return a simple structured result
    return {
        "product_id": product_id,
        "predicted_daily_demand": predicted_daily_demand,
        "predicted_total_demand": predicted_total_demand,
        "days": days_to_predict,
        "status": "success",
        "message": "Demand prediction generated successfully."
    }


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    # Sample historical sales data
    sample_data = pd.DataFrame({
        "date": [
            "2026-08-01",
            "2026-08-02",
            "2026-08-03",
            "2026-08-04",
            "2026-08-05",
            "2026-08-06",
            "2026-08-07",
            "2026-08-08"
        ],

        "product_id": [
            "P001",
            "P001",
            "P001",
            "P001",
            "P001",
            "P001",
            "P001",
            "P001"
        ],

        "sales": [
            10,
            12,
            8,
            15,
            11,
            14,
            10,
            13
        ]
    })

    # Predict demand for the next 7 days
    result = predict_demand(
        sample_data,
        product_id="P001",
        days_to_predict=7
    )

    print("\n========== DEMAND PREDICTION TEST ==========")
    print("Product ID:", result["product_id"])
    print("Predicted Daily Demand:",
          result["predicted_daily_demand"])
    print("Predicted Demand for 7 Days:",
          result["predicted_total_demand"])
    print("Status:", result["status"])
    print("Message:", result["message"])
    print("============================================")
