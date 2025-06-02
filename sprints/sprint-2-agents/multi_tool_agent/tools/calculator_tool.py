import math

def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    
    Args:
        expression (str): A mathematical expression as a string (e.g., "2 + 2", "sin(30)")
        
    Returns:
        str: The result of the calculation or an error message
    """
    try:
        # Replace common mathematical functions with their math module equivalents
        expression = expression.lower()
        for func in ["sin", "cos", "tan", "sqrt", "log", "exp"]:
            if func in expression:
                expression = expression.replace(func, f"math.{func}")
        
        # Safely evaluate the expression
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"
