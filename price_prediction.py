def validate_prices(prices):
    """
    Check whether the price data is usable.
    """

    # Make sure we received some data
    if not prices:
        return False

    # We need at least 2 prices to find a trend
    if len(prices) < 2:
        return False

    # Remove missing values
    valid_prices = [price for price in prices if price is not None]

    # Check again after removing missing values
    if len(valid_prices) < 2:
        return False

    return True

def predict_price(prices, days_ahead=7):
    """
    Predict the future price using recent price trends.
    """

    # Check if there is enough data
    if not validate_prices(prices):
        return None

    # Remove missing values
    valid_prices = [price for price in prices if price is not None]

    # Use only the most recent prices
    recent_prices = valid_prices[-5:]

    # Calculate the average change between recent prices
    changes = []

    for i in range(1, len(recent_prices)):
        change = recent_prices[i] - recent_prices[i - 1]
        changes.append(change)

    average_change = sum(changes) / len(changes)

    # Predict the future price
    last_price = recent_prices[-1]
    predicted_price = last_price + (average_change * days_ahead)

    # Price cannot be negative
    predicted_price = max(0, predicted_price)

    return round(predicted_price, 2)

def get_price_trend(prices):
    """
    Identify whether the price is increasing, decreasing, or stable.
    """

    # Check if there is enough data
    if not validate_prices(prices):
        return "Insufficient data"

    # Remove missing values
    valid_prices = [price for price in prices if price is not None]

    first_price = valid_prices[0]
    last_price = valid_prices[-1]

    # Calculate the percentage change
    percentage_change = ((last_price - first_price) / first_price) * 100

    # Decide the trend
    if percentage_change > 2:
        return "Increasing"
    elif percentage_change < -2:
        return "Decreasing"
    else:
        return "Stable"

def analyze_price(prices, days_ahead=7):
        """Analyze historical prices and return useful information."""
    
   

    
        if not validate_prices(prices):
            return {
                "current_price": None,
                "predicted_price": None,
                "trend": "Insufficient data",
                "percentage_change": None,
                "recommendation": "Not enough price data for prediction."
            }

        # Remove missing values
        valid_prices = [price for price in prices if price is not None]

        current_price = valid_prices[-1]
        predicted_price = predict_price(valid_prices, days_ahead)
        trend = get_price_trend(valid_prices)

        # Calculate percentage change
        percentage_change = (
            (predicted_price - current_price) / current_price
        ) * 100

        # Give a simple recommendation
        if trend == "Increasing":
            recommendation = "Consider purchasing earlier."
        elif trend == "Decreasing":
            recommendation = "You may wait before purchasing."
        else:
            recommendation = "Price is relatively stable."

        return {
            "current_price": round(current_price, 2),
            "predicted_price": round(predicted_price, 2),
            "trend": trend,
            "percentage_change": round(percentage_change, 2),
            "recommendation": recommendation
        }