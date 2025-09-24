# Streamlit app de visualización de KPIs
import streamlit as st

st.title("📊 KPIs desde la capa Silver")
st.write("App inicial en Streamlit. Conéctala con tus datos transformados.")
import io
import pandas as pd
import streamlit as st

# Importar funciones del pipeline
from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks


# --- Configuración de la página ---
st.set_page_config(
    page_title="Data Lab - Bronze/Silver",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 De CSVs heterogéneos a un almacén analítico confiable")
st.markdown("Este laboratorio unifica datos en **Bronze** y **Silver**, "
            "aplica validaciones y genera KPIs básicos.")


# --- Configuración de columnas origen ---
st.sidebar.header("⚙️ Configuración de columnas origen")
col_date = st.sidebar.text_input("Columna origen → date", value="date")
col_partner = st.sidebar.text_input("Columna origen → partner", value="partner")
col_amount = st.sidebar.text_input("Columna origen → amount", value="amount")

mapping = {
    col_date: "date",
    col_partner: "partner",
    col_amount: "amount"
}

# --- Subida de archivos ---
uploaded_files = st.file_uploader(
    "Sube uno o varios archivos CSV",
    type=["csv"],
    accept_multiple_files=True
)

bronze_frames = []

# --- Procesamiento de cada archivo ---
if uploaded_files:
    for file in uploaded_files:
        try:
            # Intentar leer con utf-8, fallback a latin-1
            try:
                df = pd.read_csv(file, encoding="utf-8")
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(file, encoding="latin-1")

            # Normalización
            df_norm = normalize_columns(df, mapping)

            # Linaje
            df_tagged = tag_lineage(df_norm, source_name=file.name)
            bronze_frames.append(df_tagged)

        except Exception as e:
            st.error(f"Error procesando {file.name}: {e}")

# --- Concatenar Bronze ---
if bronze_frames:
    bronze = concat_bronze(bronze_frames)

    st.subheader("📂 Datos Bronze (unificados)")
    st.dataframe(bronze, use_container_width=True)

    # Validaciones
    st.subheader("✅ Validaciones")
    errors = basic_checks(bronze)

    if errors:
        st.error("Se encontraron errores:")
        for err in errors:
            st.write(f"- {err}")
    else:
        st.success("Validaciones superadas ✔️")

        # --- Silver ---
        silver = to_silver(bronze)

        st.subheader("💿 Datos Silver (aggregados por partner×mes)")
        st.dataframe(silver, use_container_width=True)

        # KPIs simples
        st.subheader("📈 KPIs")
        total_amount = silver["total_amount"].sum()
        top_partner = silver.loc[silver["total_amount"].idxmax(), "partner"]

        st.metric("Monto total (€)", f"{total_amount:,.2f}")
        st.metric("Partner con mayor facturación", top_partner)

        # Gráfico
        st.bar_chart(
            silver.groupby("month")["total_amount"].sum(),
            use_container_width=True
        )

        # --- Descargas ---
        st.subheader("⬇️ Descargas")
        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        silver_csv = silver.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Descargar Bronze CSV",
            data=bronze_csv,
            file_name="bronze.csv",
            mime="text/csv"
        )

        st.download_button(
            "Descargar Silver CSV",
            data=silver_csv,
            file_name="silver.csv",
            mime="text/csv"
        )
else:
    st.info("📥 Esperando a que subas tus archivos CSV...")
