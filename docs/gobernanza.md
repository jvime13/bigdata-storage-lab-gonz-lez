# 🛡️ Gobernanza de Datos

Políticas y prácticas aplicadas en el laboratorio:
- Trazabilidad
- Calidad de datos
- Seguridad y control de accesos
# 🛡️ Gobernanza de Datos

Este documento establece las políticas y prácticas aplicadas en el laboratorio para garantizar calidad, seguridad y trazabilidad.

---

## 🌐 Origen y Linaje de Datos
- **Origen**: ficheros CSV cargados en la carpeta `/data/raw`.
- **Linaje**:
  - Raw → Bronze → Silver → Gold → KPIs.
  - Cada transformación debe registrarse con fecha, autor y script utilizado.
  - Mantener logs de ingesta y validación para auditoría.

---

## ✅ Validaciones Mínimas
- Formato de fecha correcto (`YYYY-MM-DD`).
- Campos obligatorios (`date`, `partner`, `amount`) no nulos.
- Tipo de dato coherente con el esquema canónico.
- Rango de valores monetarios: `amount` no debe superar límites definidos (ej. ±1e9).
- Detección de duplicados y registros inconsistentes.

---

## 🔐 Política de Mínimos Privilegios
- Acceso a `/data/raw`: restringido a roles de **Ingesta**.
- Acceso a `/data/bronze` y `/data/silver`: permitido a **Transformación** y **Validación**.
- Acceso a `/data/gold`: solo **Analistas** y **Product Owners**.
- Claves, tokens o credenciales nunca deben subirse al repositorio.

---

## 🧾 Trazabilidad
- Cada dataset procesado debe incluir metadatos: origen, timestamp de carga, versión del script.
- Documentación de los pasos de transformación en README o logs.
- Uso de nombres de archivo/versionado con convención clara (ej. `silver_YYYYMMDD.parquet`).

---

## 👥 Roles
- **Ingesta**: recibe y almacena datos crudos.
- **Validación**: verifica calidad y consistencia.
- **Transformación**: aplica normalización y genera capas bronze/silver.
- **Analista**: construye KPIs sobre capa silver/gold.
- **Owner**: define políticas, revisa documentación y aprueba despliegues.

---
