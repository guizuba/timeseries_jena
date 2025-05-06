import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    # Conversão segura do campo de data
    df['Date Time'] = pd.to_datetime(df['Date Time'], format="%d.%m.%Y %H:%M:%S", errors='coerce')
    
    # Verificação (opcional) de linhas com erro no parsing
    if df['Date Time'].isnull().any():
        print("⚠️ Atenção: Há datas inválidas que foram convertidas como NaT.")

    return df
