# Script de validación de datos (esquemas, tipos, valores nulos, etc.)

def validate_data(input_path):
    # TODO: implementar validaciones
    return True

if __name__ == "__main__":
    print("Validación completada.")
import pandas as pd
from pandas import DataFrame
from typing import List


def basic_checks(df: DataFrame) -> List[str]:
    """
    Realiza validaciones mínimas sobre un DataFrame canónico.
    Retorna lista de errores encontrados.
    """
    errors: List[str] = []

    # Verificar columnas presentes
    expected = {"date", "partner", "amount"}
    missing = expected - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas: {missing}")

    # Verificar date en datetime
    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            errors.append("Columna 'date' no es datetime")

    # Verificar amount numérico y >= 0
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("Columna 'amount' no es numérica")
        elif (df["amount"] < 0).any():
            errors.append("Existen valores negativos en 'amount'")

    return errors
