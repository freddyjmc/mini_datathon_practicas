import pytest
import pandas as pd
import matplotlib.pyplot as plt
from src.data_visualizer import plot_cases_over_time, plot_deaths_per_capita, create_heatmap

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'date': pd.date_range(start='2021-01-01', periods=10),
        'state': ['CA']*5 + ['NY']*5,
        'new_cases_7day_avg': range(10),
        'deaths_per_100k': range(10),
        'cases_per_100k': range(10)
    })

def test_plot_cases_over_time(sample_data):
    plot_cases_over_time(sample_data, ['CA', 'NY'])
    assert plt.gcf().number > 0  # Verifica que se ha creado una figura
    plt.close()

def test_plot_deaths_per_capita(sample_data):
    plot_deaths_per_capita(sample_data, '2021-01-05')
    assert plt.gcf().number > 0  # Verifica que se ha creado una figura
    plt.close()

def test_create_heatmap(sample_data):
    create_heatmap(sample_data, 'cases_per_100k')
    assert plt.gcf().number > 0  # Verifica que se ha creado una figura
    plt.close()