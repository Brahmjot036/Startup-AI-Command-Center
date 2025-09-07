import pandas as pd

def simple_forecast(initial_revenue: float, growth_rate: float, months: int = 12):
    """Generates a simple revenue forecast over months."""
    revenues = [initial_revenue * ((1 + growth_rate) ** m) for m in range(months)]
    df = pd.DataFrame({
        "Month": list(range(1, months+1)),
        "Projected Revenue ($)": revenues
    })
    return df
