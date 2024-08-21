# Análisis de COVID-19 en Estados Unidos

Este proyecto realiza un análisis exploratorio de datos (EDA) sobre la propagación del COVID-19 en los Estados Unidos, utilizando datos de The COVID Tracking Project.

## Características

- Carga de datos históricos de COVID-19 para todos los estados de EE. UU.
- Limpieza y preprocesamiento de datos
- Cálculo de métricas per cápita y otras métricas derivadas
- Visualizaciones de la evolución temporal de casos y muertes
- Análisis comparativo entre estados
- Detección de valores atípicos
- Segmentación de estados basada en métricas de COVID-19

## Requisitos

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/AI-School-F5-P3/mini_datathon_freddy
   cd covid19_usa_analysis
   ```

2. Crea un entorno virtual y actívalo:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el script de carga y procesamiento de datos:
   ```
   python src/data_processor.py
   ```

2. Ejecuta el script de visualización:
   ```
   python src/data_visualizer.py
   ```

3. Para ejecutar los tests:
   ```
   pytest tests/
   ```

## Estructura del Proyecto

```
covid19_usa_analysis/
├── data/               # Datos crudos y procesados
├── results/            # Resultados y visualizaciones
│   └── figures/
├── src/                # Código fuente
│   ├── data_loader.py
│   ├── data_processor.py
│   └── data_visualizer.py
├── tests/              # Tests unitarios
├── .gitignore
├── README.md
└── requirements.txt
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.

