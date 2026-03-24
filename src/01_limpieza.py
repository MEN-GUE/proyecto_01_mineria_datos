import os
import re

import pandas as pd


MISSING_TOKENS = {"", "NA", "N/A", "NO INDICA", "IGNORADO", "SIN DATO", "NAN", "<NA>"}
PATRON_NUMERICO = re.compile(r"otr[oa]s|victimas|agresores|hijos|hij", flags=re.IGNORECASE)


def corregir_mojibake(valor):
    if not isinstance(valor, str):
        return valor
    if "Ã" not in valor and "Â" not in valor:
        return valor
    try:
        return valor.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return valor


def normalizar_texto(serie):
    serie = serie.astype("string").map(corregir_mojibake)
    serie = serie.str.strip().str.upper()
    return serie.mask(serie.isin(MISSING_TOKENS))


def convertir_a_numerico(serie):
    serie = serie.astype("string")
    serie = serie.str.replace(",", ".", regex=False)
    serie = serie.str.replace(r"(?i)NINGUN[OA]", "0", regex=True)
    serie = serie.str.replace(r"(?i)(\d+)\s*Y\s*M[AÁ]S", r"\1", regex=True)
    serie = serie.str.replace(r"[^0-9.\-]", "", regex=True)
    serie = serie.mask(serie.eq(""))
    return pd.to_numeric(serie, errors="coerce")


def normalizar_variable_respuesta(df):
    if "hec_tipagre" not in df.columns:
        return df
    df["hec_tipagre"] = df["hec_tipagre"].str.replace(r"\s*-\s*", "-", regex=True)
    return df


def limpiar_datos(filepath):
    print("Cargando datos...")
    df = pd.read_csv(filepath, low_memory=False)

    # Elimina columnas completamente vacías, como la columna sin nombre del CSV fuente.
    df.dropna(how="all", axis=1, inplace=True)

    print("Normalizando variables de texto...")
    cols_texto = df.select_dtypes(include=["object", "string"]).columns
    for col in cols_texto:
        df[col] = normalizar_texto(df[col])

    cols_numericas = [col for col in df.columns if PATRON_NUMERICO.search(col)]
    if "agr_edad" in df.columns and "agr_edad" not in cols_numericas:
        cols_numericas.append("agr_edad")

    print("Transformando y limpiando variables numéricas...")
    for col in cols_numericas:
        df[col] = convertir_a_numerico(df[col])

    print("Normalizando variable respuesta...")
    df = normalizar_variable_respuesta(df)

    print("Formateando fechas...")
    if "fecha_hecho_limpia" in df.columns:
        df["fecha_hecho_limpia"] = pd.to_datetime(df["fecha_hecho_limpia"], errors="coerce")
        df = df.dropna(subset=["fecha_hecho_limpia"])

    if "hec_tipagre" in df.columns:
        clases = df["hec_tipagre"].dropna().nunique()
        print(f"Variable respuesta normalizada: hec_tipagre ({clases} clases).")

    return df

if __name__ == "__main__":
    df_limpio = limpiar_datos('../data/raw/Base_Violencia_INE_Unificada_LIMPIA.csv')
    
    # Guardamos en formato parquet para una carga mucho más rápida en los siguientes scripts
    os.makedirs('../data/processed', exist_ok=True)
    df_limpio.to_parquet('../data/processed/datos_limpios.parquet')
    print("Limpieza finalizada. Datos procesados guardados.")
