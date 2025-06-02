import os
import requests
from dotenv import load_dotenv

load_dotenv()

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using exchange rates.
    
    Args:
        amount (float): The amount to convert
        from_currency (str): The source currency code (e.g., USD, EUR)
        to_currency (str): The target currency code (e.g., USD, EUR)
        
    Returns:
        str: The converted amount or an error message
    """
    API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
    if not API_KEY:
        # Fallback to mock data if no API key is available
        mock_rates = {
            "USD": 1.0,
            "EUR": 0.93,
            "GBP": 0.79,
            "JPY": 151.72,
            "CAD": 1.37,
            "AUD": 1.52,
            "ZAR": 18.41
        }
        
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency not in mock_rates or to_currency not in mock_rates:
            return f"Currency not supported in mock data: {from_currency} or {to_currency}"
        
        # Calculate conversion using mock rates
        usd_amount = amount / mock_rates[from_currency]
        converted_amount = usd_amount * mock_rates[to_currency]
        
        return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (using mock data)"
    
    # Use actual API if key is available
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    
    try:
        response = requests.get(url).json()
        if response.get("result") == "success":
            converted_amount = response.get("conversion_result")
            return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        else:
            return f"Error: {response.get('error-type', 'Unknown error')}"
    except Exception as e:
        return f"Error converting currency: {str(e)}"
