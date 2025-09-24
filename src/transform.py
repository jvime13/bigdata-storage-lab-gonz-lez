# Script de normalización y transformación
# Genera capas bronze y silver

def transform_data(input_path, output_path="../data/bronze/"):
    # TODO: implementar transformaciones
    pass

if __name__ == "__main__":
    print("Transformación ejecutada.")
import pandas as pd
from pandas import DataFrame
from typing import Dict


def normalize_columns(df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
    """
    Renombra y normaliza columnas según el esquema canónico.
    - mapping: dict con {columna_origen: columna_canónica}
    - Normaliza:
        * date → datetime ISO (YYYY-MM-DD)
        * partner → strip espacios
        * amount → float en EUR (quita € y comas europeas)
    """
    # Renombrar columnas según mapping
    df = df.rename(columns=mapping)

    # Asegurar columnas canónicas presentes
    expected = {"date", "partner", "amount"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas canónicas: {missing}")

    # Parsear fechas
    df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")

    # Limpiar partner
    df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount (quita símbolos y convierte a float)
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(".", "", regex=False)  # quitar separador miles
        .str.replace(",", ".", regex=False)  # coma decimal → punto
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df[["date", "partner", "amount"]]


def to_silver(bronze: DataFrame) -> DataFrame:
    """
    Agrega montos por partner y mes.
    - month: primer día del mes (timestamp)
    """
    bronze = bronze.copy()
    bronze["month"] = bronze["date"].dt.to_period("M").dt.to_timestamp()

    silver = (
        bronze.groupby(["partner", "month"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_amount"})
    )

    return silver
