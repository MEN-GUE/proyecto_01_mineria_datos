import pandas as pd
import numpy as np
import re
import os

def limpiar_datos(filepath):
    print("Cargando datos...")
    # Se recomienda usar low_memory=False para datasets grandes
    df = pd.read_csv(filepath, low_memory=False)
    
    # Equivalente a remove_empty("cols")
    df.dropna(how='all', axis=1, inplace=True)
    
    # matches("otr[oa]s|victimas|agresores|hijos|hij")
    patron = re.compile(r'otr[oa]s|victimas|agresores|hijos|hij', flags=re.IGNORECASE)
    cols_numericas = [col for col in df.columns if patron.search(col)]
    if 'agr_edad' in df.columns and 'agr_edad' not in cols_numericas:
        cols_numericas.append('agr_edad')
        
    print("Transformando y limpiando variables numéricas...")
    for col in cols_numericas:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace('98 y más', '98')
        df[col] = df[col].str.replace(r'(?i)ningun[oa]', '0', regex=True)
        df[col] = df[col].replace(['Ignorado', 'No indica', 'NA', 'nan', '<NA>'], np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Limpieza de Fechas: ymd(fecha_hecho_limpia)
    print("Formateando fechas...")
    if 'fecha_hecho_limpia' in df.columns:
        df['fecha_hecho_limpia'] = pd.to_datetime(df['fecha_hecho_limpia'], errors='coerce')
        # Filtro de Seguridad
        df = df.dropna(subset=['fecha_hecho_limpia'])
        
    return df

if __name__ == "__main__":
    df_limpio = limpiar_datos('../data/raw/Base_Violencia_INE_Unificada_LIMPIA.csv')
    
    # Guardamos en formato parquet para una carga mucho más rápida en los siguientes scripts
    os.makedirs('../data/processed', exist_ok=True)
    df_limpio.to_parquet('../data/processed/datos_limpios.parquet')
    print("Limpieza finalizada. Datos procesados guardados.")