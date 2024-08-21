import pandas as pd
import numpy as np
from typing import Dict, Any
from scipy import stats

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y preprocesa los datos crudos de COVID-19.
    """
    # Convertir fecha a datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # Reemplazar valores negativos con NaN
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].mask(df[col] < 0, np.nan)
    
   # Calcular casos y muertes diarias
    df = df.sort_values(['state', 'date'])
    df['new_cases'] = df.groupby('state')['positive'].diff()
    df['new_deaths'] = df.groupby('state')['death'].diff()
    
    # Calcular promedio móvil de 7 días
    df['cases_7day_avg'] = df.groupby('state')['new_cases'].rolling(7).mean().reset_index(0, drop=True)
    df['deaths_7day_avg'] = df.groupby('state')['new_deaths'].rolling(7).mean().reset_index(0, drop=True)
    
    return df

def calculate_per_capita_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas per cápita para casos y muertes.
    """
    # Nota: Normalmente cargaríamos los datos de población de una fuente externa
    # Para este ejemplo, usaremos un diccionario de poblaciones ficticias
    state_populations = {
        'CA': 39512223, 'TX': 28995881, 'FL': 21477737, 'NY': 19453561,
        'PA': 12801989, 'IL': 12671821, 'OH': 11689100, 'GA': 10617423,
        'NC': 10488084, 'MI': 9986857, 'NJ': 8882190, 'VA': 8535519,
        'WA': 7614893, 'AZ': 7278717, 'MA': 6892503, 'TN': 6829174,
        'IN': 6732219, 'MO': 6137428, 'MD': 6045680, 'WI': 5822434,
        'CO': 5758736, 'MN': 5639632, 'SC': 5148714, 'AL': 4903185,
        'LA': 4648794, 'KY': 4467673, 'OR': 4217737, 'OK': 3956971,
        'CT': 3565287, 'UT': 3205958, 'IA': 3155070, 'NV': 3080156,
        'AR': 3017804, 'MS': 2976149, 'KS': 2913314, 'NM': 2096829,
        'NE': 1934408, 'ID': 1787065, 'WV': 1792147, 'HI': 1415872,
        'NH': 1359711, 'ME': 1344212, 'MT': 1068778, 'RI': 1059361,
        'DE': 973764, 'SD': 884659, 'ND': 762062, 'AK': 731545,
        'VT': 623989, 'WY': 578759
    }
    
    df['population'] = df['state'].map(state_populations)
    df['cases_per_100k'] = (df['positive'] / df['population']) * 100000
    df['deaths_per_100k'] = (df['death'] / df['population']) * 100000
    
    return df

def detect_outliers(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Detecta valores atípicos utilizando el método IQR.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return ((df[column] < lower_bound) | (df[column] > upper_bound))

def normalize_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normaliza las columnas especificadas utilizando Min-Max scaling.
    """
    for col in columns:
        df[f'{col}_normalized'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df

def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea nuevas características derivadas.
    """
    # Tasa de positividad
    df['positivity_rate'] = df['positive'] / df['totalTestResults']
    
    # Tasa de letalidad
    df['case_fatality_rate'] = df['death'] / df['positive']
    
    # Días desde el primer caso
    df['days_since_first_case'] = df.groupby('state')['date'].rank(method='dense')
    
    return df

def restructure_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reestructura los datos para el análisis.
    """
    # Seleccionar y renombrar columnas relevantes
    columns = {
        'date': 'date',
        'state': 'state',
        'positive': 'total_cases',
        'death': 'total_deaths',
        'totalTestResults': 'total_tests',
        'new_cases': 'new_cases',
        'new_deaths': 'new_deaths',
        'cases_7day_avg': 'new_cases_7day_avg',  # Cambiado de 'cases_7day_avg' a 'new_cases_7day_avg'
        'deaths_7day_avg': 'new_deaths_7day_avg',
        'cases_per_100k': 'cases_per_100k',
        'deaths_per_100k': 'deaths_per_100k',
        'positivity_rate': 'positivity_rate',
        'case_fatality_rate': 'case_fatality_rate',
        'days_since_first_case': 'days_since_first_case'
    }
    
    # Solo seleccionar las columnas que existen en el DataFrame
    existing_columns = [col for col in columns.keys() if col in df.columns]
    return df[existing_columns].rename(columns={col: columns[col] for col in existing_columns})

def process_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa los datos crudos aplicando todas las funciones de procesamiento.
    """
    df = clean_data(raw_data)
    df = calculate_per_capita_metrics(df)
    df = create_derived_features(df)
    
    # Detectar y marcar outliers
    for col in ['new_cases', 'new_deaths', 'cases_per_100k', 'deaths_per_100k']:
        if col in df.columns:
            df[f'{col}_outlier'] = detect_outliers(df, col)
    
    # Normalizar algunas columnas
    columns_to_normalize = ['positive', 'death', 'totalTestResults']
    columns_to_normalize = [col for col in columns_to_normalize if col in df.columns]
    if columns_to_normalize:
        df = normalize_data(df, columns_to_normalize)
    
    return restructure_data(df)
    print(df.columns)  # Para verificar los nombres de las columnas

if __name__ == "__main__":
    # Ejemplo de uso
    from data_loader import load_all_states_data
    
    raw_data = load_all_states_data()
    processed_data = process_data(raw_data)
    print(processed_data.head())
    processed_data.to_csv("data/processed_data.csv", index=False)