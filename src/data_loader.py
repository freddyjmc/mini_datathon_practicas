import requests
import pandas as pd
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.covidtracking.com/v1/states"

def fetch_state_data(state: str) -> Dict[str, Any]:
    """
    Fetches historical COVID-19 data for a specific state.
    
    Args:
    state (str): Two-letter state code (e.g., 'CA' for California)
    
    Returns:
    Dict[str, Any]: JSON response from the API
    """
    url = f"{BASE_URL}/{state.lower()}/daily.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for state {state}: {e}")
        return None

def load_all_states_data() -> pd.DataFrame:
    """
    Loads historical COVID-19 data for all states and combines into a single DataFrame.
    
    Returns:
    pd.DataFrame: Combined data for all states
    """
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    all_data = []
    for state in states:
        state_data = fetch_state_data(state)
        if state_data:
            df = pd.DataFrame(state_data)
            df['state'] = state
            all_data.append(df)
        else:
            logger.warning(f"No data available for state {state}")
    
    if not all_data:
        logger.error("No data could be fetched for any state")
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)

if __name__ == "__main__":
    # Example usage
    df = load_all_states_data()
    if not df.empty:
        print(df.head())
        df.to_csv("data/raw_data.csv", index=False)
    else:
        print("No data available to save")