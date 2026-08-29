"""
Supplier Comparison Module
Smart Retail AI - SAP Hackfest 2026

This module compares suppliers based on:
1. Product price
2. Delivery time
3. Product availability
4. Reliability rating

It recommends the supplier with the highest overall score.
"""

import pandas as pd


# ---------------------------------------------------------
# WEIGHTS
# ---------------------------------------------------------
# Total weight = 100%
PRICE_WEIGHT = 0.30
DELIVERY_WEIGHT = 0.25
AVAILABILITY_WEIGHT = 0.20
RELIABILITY_WEIGHT = 0.25


# ---------------------------------------------------------
# FUNCTION 1: CALCULATE SUPPLIER SCORES
# ---------------------------------------------------------

def compare_suppliers(suppliers):
    """
    Compare suppliers and calculate an overall score out of 100.

    Parameters:
        suppliers: pandas DataFrame containing supplier information.

    Returns:
        DataFrame containing individual scores and overall score.
    """

    # Make a copy so that the original data is not changed
    df = suppliers.copy()

    # -----------------------------------------------------
    # PRICE SCORE
    # -----------------------------------------------------
    # Lower price is better.
    # The cheapest supplier gets 100.
    # Other suppliers receive a proportional score.

    cheapest_price = df["Price"].min()

    if cheapest_price > 0:
        df["Price Score"] = (cheapest_price / df["Price"]) * 100
    else:
        df["Price Score"] = 0


    # -----------------------------------------------------
    # DELIVERY SCORE
    # -----------------------------------------------------
    # Faster delivery is better.
    # The fastest supplier gets 100.

    fastest_delivery = df["Delivery Days"].min()

    if fastest_delivery > 0:
        df["Delivery Score"] = (
            fastest_delivery / df["Delivery Days"]
        ) * 100
    else:
        df["Delivery Score"] = 0


    # -----------------------------------------------------
    # AVAILABILITY SCORE
    # -----------------------------------------------------
    # Available = 100
    # Not Available = 0

    df["Availability Score"] = df["Availability"].apply(
        lambda x: 100 if str(x).lower() in
        ["yes", "available", "true", "1"] else 0
    )


    # -----------------------------------------------------
    # RELIABILITY SCORE
    # -----------------------------------------------------
    # Reliability is assumed to be rated from 1 to 5.
    # Convert it to a score out of 100.

    df["Reliability Score"] = (
        df["Reliability"] / 5
    ) * 100


    # -----------------------------------------------------
    # OVERALL SCORE
    # -----------------------------------------------------
    # Combine all four scores using their weights.

    df["Overall Score"] = (
        df["Price Score"] * PRICE_WEIGHT
        + df["Delivery Score"] * DELIVERY_WEIGHT
        + df["Availability Score"] * AVAILABILITY_WEIGHT
        + df["Reliability Score"] * RELIABILITY_WEIGHT
    )

    # Round scores to two decimal places
    df["Price Score"] = df["Price Score"].round(2)
    df["Delivery Score"] = df["Delivery Score"].round(2)
    df["Availability Score"] = df["Availability Score"].round(2)
    df["Reliability Score"] = df["Reliability Score"].round(2)
    df["Overall Score"] = df["Overall Score"].round(2)

    # Sort suppliers from best to worst
    df = df.sort_values(
        by="Overall Score",
        ascending=False
    ).reset_index(drop=True)

    return df


# ---------------------------------------------------------
# FUNCTION 2: RECOMMEND BEST SUPPLIER
# ---------------------------------------------------------

def recommend_supplier(comparison_results):
    """
    Select the supplier with the highest overall score.

    Parameters:
        comparison_results: DataFrame returned by
                            compare_suppliers().

    Returns:
        Name of the recommended supplier.
    """

    if comparison_results.empty:
        return None

    best_supplier = comparison_results.iloc[0]

    return best_supplier["Supplier Name"]


# ---------------------------------------------------------
# FUNCTION 3: GIVE REASON FOR RECOMMENDATION
# ---------------------------------------------------------

def get_recommendation_reason(comparison_results):
    """
    Generate a simple explanation for why the supplier
    was recommended.
    """

    if comparison_results.empty:
        return "No suppliers are available for comparison."

    best_supplier = comparison_results.iloc[0]

    supplier_name = best_supplier["Supplier Name"]
    score = best_supplier["Overall Score"]

    price = best_supplier["Price"]
    delivery = best_supplier["Delivery Days"]
    availability = best_supplier["Availability"]
    reliability = best_supplier["Reliability"]

    reason = (
        f"{supplier_name} is recommended with an overall score "
        f"of {score}/100. "
        f"It offers the product at ₹{price}, delivers in "
        f"{delivery} days, has availability status '{availability}', "
        f"and has a reliability rating of {reliability}/5."
    )

    return reason


# ---------------------------------------------------------
# FUNCTION 4: COMPLETE SUPPLIER COMPARISON
# ---------------------------------------------------------

def supplier_comparison(suppliers):
    """
    Perform the complete supplier comparison.

    Returns:
        comparison_results: Detailed supplier scores
        recommended_supplier: Best supplier
        reason: Explanation for recommendation
    """

    comparison_results = compare_suppliers(suppliers)

    recommended_supplier = recommend_supplier(
        comparison_results
    )

    reason = get_recommendation_reason(
        comparison_results
    )

    return (
        comparison_results,
        recommended_supplier,
        reason
    )


# ---------------------------------------------------------
# SAMPLE DATA / TEST
# ---------------------------------------------------------
# This section runs only when this file is executed directly.
# It will NOT run when the functions are imported into app.py.

if __name__ == "__main__":

    # Sample supplier data
    sample_data = {
        "Product Name": [
            "Rice",
            "Rice",
            "Rice"
        ],

        "Supplier Name": [
            "ABC Suppliers",
            "FreshMart Wholesale",
            "Reliable Traders"
        ],

        "Price": [
            100,
            90,
            105
        ],

        "Delivery Days": [
            2,
            6,
            3
        ],

        "Availability": [
            "Yes",
            "Yes",
            "Yes"
        ],

        "Reliability": [
            4.8,
            3.6,
            4.5
        ]
    }

    # Convert sample data into a DataFrame
    suppliers = pd.DataFrame(sample_data)

    # Run comparison
    results, recommended, reason = supplier_comparison(
        suppliers
    )

    # Display results
    print("\n========================================")
    print("       SUPPLIER COMPARISON")
    print("========================================")

    print(
        results[
            [
                "Supplier Name",
                "Price",
                "Delivery Days",
                "Availability",
                "Reliability",
                "Overall Score"
            ]
        ].to_string(index=False)
    )

    print("\n========================================")
    print("RECOMMENDED SUPPLIER")
    print("========================================")

    print(recommended)

    print("\n========================================")
    print("REASON")
    print("========================================")

    print(reason)

