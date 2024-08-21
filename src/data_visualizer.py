import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_cases_over_time(df: pd.DataFrame, states: list, save_path: str = None):
    """
    Plots the 7-day average of new cases over time for specified states.
    
    Args:
    df (pd.DataFrame): Processed COVID-19 data
    states (list): List of state codes to plot
    save_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    plt.figure(figsize=(12, 6))
    for state in states:
        state_data = df[df['state'] == state]
        plt.plot(state_data['date'], state_data['new_cases_7day_avg'], label=state)  # Cambiado de 'cases_7day_avg' a 'new_cases_7day_avg'
    
    plt.title('7-Day Average of New COVID-19 Cases by State')
    plt.xlabel('Date')
    plt.ylabel('7-Day Average of New Cases')
    plt.legend()
    plt.xticks(rotation=45)
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def plot_deaths_per_capita(df: pd.DataFrame, date: str, save_path: str = None):
    """
    Creates a bar plot of deaths per 100k population for each state on a specific date.
    
    Args:
    df (pd.DataFrame): Processed COVID-19 data
    date (str): Date to plot data for, in 'YYYY-MM-DD' format
    save_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    date_data = df[df['date'] == date].sort_values('deaths_per_100k', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='state', y='deaths_per_100k', data=date_data)
    plt.title(f'COVID-19 Deaths per 100k Population by State ({date})')
    plt.xlabel('State')
    plt.ylabel('Deaths per 100k Population')
    plt.xticks(rotation=90)
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def create_heatmap(df: pd.DataFrame, metric: str, save_path: str = None):
    """
    Creates a heatmap of a specific metric across all states and dates.
    
    Args:
    df (pd.DataFrame): Processed COVID-19 data
    metric (str): Column name of the metric to visualize
    save_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    pivot_df = df.pivot(index='date', columns='state', values=metric)
    
    plt.figure(figsize=(16, 10))
    sns.heatmap(pivot_df, cmap='YlOrRd')
    plt.title(f'Heatmap of {metric} Across States Over Time')
    plt.xlabel('State')
    plt.ylabel('Date')
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

if __name__ == "__main__":
    # Cargar datos
    df = pd.read_csv("data/processed_data.csv")
    
    # Convertir la columna 'date' a datetime
    df['date'] = pd.to_datetime(df['date'])
    
 
    
    # Generar visualizaciones
    plot_cases_over_time(df, ['CA', 'NY', 'FL', 'TX'], 'results/figures/cases_over_time.png')
    plot_deaths_per_capita(df, df['date'].max().strftime('%Y-%m-%d'), 'results/figures/deaths_per_capita.png')
    create_heatmap(df, 'cases_per_100k', 'results/figures/cases_heatmap.png')