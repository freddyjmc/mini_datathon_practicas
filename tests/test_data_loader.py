import pytest
from src.data_loader import fetch_state_data, load_all_states_data
import pandas as pd

def test_fetch_state_data():
    data = fetch_state_data('CA')
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'date' in data[0]
    assert 'state' in data[0]
    assert 'positive' in data[0]

def test_load_all_states_data():
    df = load_all_states_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'date' in df.columns
    assert 'state' in df.columns
    assert 'positive' in df.columns
    assert len(df['state'].unique()) > 1  # Asegurarse de que hay datos para múltiples estados