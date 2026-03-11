import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import re
import os

def generar_exploracion(df):
    os.makedirs('../output/graphs', exist_ok=True)
    os.makedirs('../output/results', exist_ok=True)
    
    # 1. Resumen de Estructura y Variables Numéricas
    cols_num = df.select_dtypes(include=[np.number]).columns
    cols_num = [c for c in cols_num if not re.search(r'boleta|id|codigo', c, re.IGNORECASE)]
    df_num = df[cols_num]
    
    resumen = df_num.describe().T
    print("--- TABLA RESUMEN DE VARIABLES NUMÉRICAS ---")
    print(resumen[['mean', '50%', 'std', 'min', '25%', '75%', 'max']])
    resumen.to_csv('../output/results/resumen_estadistico.csv')
    
    # 2. Histogramas Múltiples
    print("Generando histogramas de distribución...")
    num_cols_count = len(cols_num)
    filas = (num_cols_count + 3) // 4
    fig = plt.figure(figsize=(16, 4 * filas))
    
    for i, col in enumerate(cols_num, 1):
        ax = fig.add_subplot(filas, 4, i)
        sns.histplot(df_num[col].dropna(), bins=30, color="#2A9D8F", edgecolor="white", alpha=0.8, ax=ax)
        ax.set_title(col, fontweight='bold', fontsize=10)
        ax.set_ylabel("Frecuencia")
        ax.set_xlabel("")
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle("Distribución de Variables Numéricas\nAnálisis de Frecuencias (INE)", y=1.02, fontsize=14)
    plt.tight_layout()
    plt.savefig('../output/graphs/histogramas_numericas.png', bbox_inches='tight')
    plt.close()

def prueba_normalidad(df):
    print("Generando Q-Q Plots...")
    df_muestra = df.sample(n=min(5000, len(df)), random_state=123)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    if 'edad_limpia' in df_muestra.columns:
        stats.probplot(df_muestra['edad_limpia'].dropna(), dist="norm", plot=axes[0])
        axes[0].set_title("Q-Q Plot: Edad Víctima")
        axes[0].get_lines()[1].set_color('red')
        
    if 'total_hijos' in df_muestra.columns:
        stats.probplot(df_muestra['total_hijos'].dropna(), dist="norm", plot=axes[1])
        axes[1].set_title("Q-Q Plot: Total Hijos")
        axes[1].get_lines()[1].set_color('red')
        
    plt.tight_layout()
    plt.savefig('../output/graphs/qq_plots.png')
    plt.close()

if __name__ == "__main__":
    df = pd.read_parquet('../data/processed/datos_limpios.parquet')
    generar_exploracion(df)
    prueba_normalidad(df)
    print("Exploración finalizada. Gráficas guardadas en output/graphs/")