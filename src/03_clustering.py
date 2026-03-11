import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os

def realizar_clustering(df):
    os.makedirs('../output/graphs', exist_ok=True)
    os.makedirs('../output/results', exist_ok=True)
    
    print("Preparando variables para clustering...")
    # Seleccionamos las cuantitativas mencionadas en el reporte 
    features = ['edad_limpia', 'total_hijos']
    df_cluster = df[features].dropna().copy()
    
    # Normalización para garantizar distancias matemáticas precisas
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cluster)
    
    print("Ejecutando K-Means (k=3)...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_cluster['Cluster'] = kmeans.fit_predict(df_scaled)
    
    # 1. Extraer los centroides
    centroides = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)
    centroides.index.name = 'Cluster'
    print("\nCentroides de los clústeres resultantes:")
    print(centroides)
    centroides.to_csv('../output/results/centroides_k3.csv')
    
    # 2. Visualización 2D
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='edad_limpia', y='total_hijos', hue='Cluster', data=df_cluster, palette='viridis', alpha=0.5)
    plt.title('Segmentación de Perfiles de Víctimas (K-Means, k=3)')
    plt.savefig('../output/graphs/kmeans_clusters.png')
    plt.close()

if __name__ == "__main__":
    df = pd.read_parquet('../data/processed/datos_limpios.parquet')
    realizar_clustering(df)
    print("Clustering finalizado.")