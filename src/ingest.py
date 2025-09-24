# Script de ingesta de CSVs heterogéneos
# Guarda los archivos crudos en la carpeta /data/raw

def ingest_csv(file_path, output_path="../data/raw/"):
    # TODO: implementar lógica de copia/almacenamiento
    pass

if __name__ == "__main__":
    print("Ingesta ejecutada.")
import pandas as pd
from pandas import DataFrame
from typing import List
from datetime import datetime, timezone


def tag_lineage(df: DataFrame, source_name: str) -> DataFrame:
    """
    Añade columnas de linaje:
    - source_file: nombre del archivo origen
    - ingested_at: timestamp UTC ISO
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[DataFrame]) -> DataFrame:
    """
    Concatena múltiples DataFrames con esquema canónico + linaje.
    Devuelve columnas: date, partner, amount, source_file, ingested_at
    """
    if not frames:
        return pd.DataFrame(
            columns=["date", "partner", "amount", "source_file", "ingested_at"]
        )

    bronze = pd.concat(frames, ignore_index=True)
    return bronze[["date", "partner", "amount", "source_file", "ingested_at"]]

