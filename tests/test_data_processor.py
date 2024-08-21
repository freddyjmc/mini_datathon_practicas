import pytest
import pandas as pd
import numpy as np
from src.data_processor import clean_data, calculate_per_capita_metrics, detect_outliers, normalize_data, create_derived_features, process_data

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'date': ['20210101', '20210102', '20210103'],
        'state': ['CA', 'CA', 'CA'],
        'positive': [1000, 1100, 1210],
        'death': [10, 12, 15],
        'totalTestResults': [5000, 5500, 6000],
    })

def test_clean_data(sample_data):
    cleaned = clean_data(sample_data)
    assert 'new_cases' in cleaned.columns
    assert 'new_deaths' in cleaned.columns
    assert 'cases_7day_avg' in cleaned.columns
    assert 'deaths_7day_avg' in cleaned.columns

def test_calculate_per_capita_metrics(sample_data):
    result = calculate_per_capita_metrics(sample_data)
    assert 'cases_per_100k' in result.columns
    assert 'deaths_per_100k' in result.columns

def test_detect_outliers(sample_data):
    outliers = detect_outliers(sample_data, 'positive')
    assert isinstance(outliers, pd.Series)
    assert len(outliers) == len(sample_data)

def test_normalize_data(sample_data):
    normalized = normalize_data(sample_data, ['positive'])
    assert 'positive_normalized' in normalized.columns
    assert normalized['positive_normalized'].max() <= 1
    assert normalized['positive_normalized'].min() >= 0

def test_create_derived_features(sample_data):
    result = create_derived_features(sample_data)
    assert 'positivity_rate' in result.columns
    assert 'case_fatality_rate' in result.columns
    assert 'days_since_first_case' in result.columns

def test_process_data(sample_data):
    processed = process_data(sample_data)
    assert 'total_cases' in processed.columns
    assert 'total_deaths' in processed.columns
    assert 'new_cases_7day_avg' in processed.columns
    assert 'new_deaths_7day_avg' in processed.columns