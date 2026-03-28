import os
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix,
    ConfusionMatrixDisplay, roc_auc_score, RocCurveDisplay
)
 
warnings.filterwarnings("ignore")
 
# rutas de datos
PARQUET_PATH = "../data/processed/datos_limpios.parquet"
CSV_FALLBACK  = "../data/raw/Base_Violencia_INE_Unificada_LIMPIA.csv"
 
def cargar_datos():
    # carga parquet si existe, si no usa csv
    if os.path.exists(PARQUET_PATH):
        print(f"✔ Cargando datos desde parquet: {PARQUET_PATH}")
        return pd.read_parquet(PARQUET_PATH)
 
    print(f"⚠ No se encontró el parquet. Cargando CSV: {CSV_FALLBACK}")
    if not os.path.exists(CSV_FALLBACK):
        raise FileNotFoundError("No se encontró ningún archivo de datos")
    df = pd.read_csv(CSV_FALLBACK, low_memory=False)
    df.dropna(how="all", axis=1, inplace=True)
    return df
 
# categorías que indican violencia física
CATEGORIAS_FISICO = {
    "FÍSICA","FÍSICA-PSICOLÓGICA","FÍSICA-PSICOLÓGICA-PATRIMONIAL",
    "SEXUAL","FÍSICA-SEXUAL","FÍSICA-PSICOLÓGICA-SEXUAL",
    "FÍSICA-PATRIMONIAL","FÍSICA-SEXUAL-PATRIMONIAL",
    "FÍSICA-PSICOLÓGICA-SEXUAL-PATRIMONIAL",
}
 
def crear_variable_respuesta(df):
    # convierte tipo de agresión a binario
    if "hec_tipagre" not in df.columns:
        raise KeyError("Falta columna hec_tipagre")
 
    tipagre = (
        df["hec_tipagre"]
        .astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s*-\s*", "-", regex=True)
    )
 
    df["riesgo_violencia_fisica"] = tipagre.map(
        lambda x: 1 if x in CATEGORIAS_FISICO else (0 if pd.notna(x) else np.nan)
    )
 
    df = df.dropna(subset=["riesgo_violencia_fisica"]).copy()
    df["riesgo_violencia_fisica"] = df["riesgo_violencia_fisica"].astype(int)
    return df
 
# columnas que se usan
COLUMNAS_REQUERIDAS = [
    "edad_limpia", "total_hijos", "agr_edad",
    "vic_rel_agr", "vic_trabaja", "hec_recur_denun",
]
 
def transformar_predictores(df):
    # selecciona columnas disponibles
    disponibles = [c for c in COLUMNAS_REQUERIDAS if c in df.columns]
    df = df[disponibles + ["riesgo_violencia_fisica"]
            + (["Cluster"] if "Cluster" in df.columns else [])].copy()
 
    # imputación simple
    for col in ["edad_limpia", "agr_edad"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
 
    if "total_hijos" in df.columns:
        df["total_hijos"] = df["total_hijos"].fillna(0)
 
    # binariza denuncias
    if "hec_recur_denun" in df.columns:
        df["hec_recur_denun"] = (
            df["hec_recur_denun"]
            .astype("string")
            .str.strip()
            .str.upper()
            .map(lambda x: 1 if x not in {"NO","NO INDICA","NAN","NONE","<NA>",""} else 0)
        )
 
    # limpia si trabaja
    if "vic_trabaja" in df.columns:
        df["vic_trabaja"] = df["vic_trabaja"].astype(str).str.upper()
 
    # agrupa relación
    if "vic_rel_agr" in df.columns:
        df["vic_rel_agr"] = df["vic_rel_agr"].fillna("Otros")
 
    # escala variables numéricas
    cols_continuas = [c for c in ["edad_limpia","total_hijos","agr_edad"] if c in df.columns]
    scaler = MinMaxScaler()
    df[cols_continuas] = scaler.fit_transform(df[cols_continuas])
 
    # one hot encoding
    cols_categoricas = [c for c in ["vic_trabaja","vic_rel_agr","Cluster"] if c in df.columns]
    df = pd.get_dummies(df, columns=cols_categoricas, drop_first=True, dtype=int)
 
    return df
 
def dividir_datos(df):
    # separa X y y
    X = df.drop(columns=["riesgo_violencia_fisica"])
    y = df["riesgo_violencia_fisica"]
 
    # split train/test
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
 
def entrenar_modelos(X_train, y_train):
    # entrena 4 modelos
    modelos = {}
 
    modelos["CART"] = DecisionTreeClassifier(max_depth=6, min_samples_leaf=50).fit(X_train, y_train)
    modelos["Random Forest"] = RandomForestClassifier(n_estimators=200, max_depth=10).fit(X_train, y_train)
    modelos["KNN"] = KNeighborsClassifier(n_neighbors=11).fit(X_train, y_train)
    modelos["Regresión Logística"] = LogisticRegression(max_iter=500).fit(X_train, y_train)
 
    return modelos
 
def evaluar_modelos(modelos, X_test, y_test, feature_names):
    # evalúa cada modelo
    for nombre, modelo in modelos.items():
        y_pred = modelo.predict(X_test)
        print(f"\nModelo: {nombre}")
        print(classification_report(y_test, y_pred))
 
def graficar_feature_importance(modelos, feature_names):
    # importancia de variables
    for nombre in ["CART","Random Forest"]:
        if nombre in modelos:
            imp = pd.Series(modelos[nombre].feature_importances_, index=feature_names)
            imp.sort_values().tail(15).plot(kind="barh")
            plt.title(nombre)
            plt.show()
 
def graficar_arbol(modelo_cart, feature_names):
    # dibuja árbol
    plot_tree(modelo_cart, max_depth=3, feature_names=feature_names)
    plt.show()
 
def graficar_comparativa_accuracy(df_resumen):
    # gráfica de accuracy
    sns.barplot(data=df_resumen, x="Modelo", y="Accuracy")
    plt.show()
 
if __name__ == "__main__":
    # flujo principal
    df_raw = cargar_datos()
    df = crear_variable_respuesta(df_raw)
    df_modelo = transformar_predictores(df)
 
    X_train, X_test, y_train, y_test = dividir_datos(df_modelo)
    modelos = entrenar_modelos(X_train, y_train)
 
    evaluar_modelos(modelos, X_test, y_test, X_train.columns)