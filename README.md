# Extractor de Facturas Comerciales - Tianjin Baolai 📈

[cite_start]Este proyecto automatiza la extracción de datos técnicos, logísticos y financieros desde facturas PDF de **Tianjin Baolai International Trade Co., Ltd**.

## 📋 Información Extraída
El script organiza los siguientes datos en un archivo Excel:

* [cite_start]**Cabecera:** Número de factura (ej. BLA20210326A), fecha y RUC del comprador (20600853318)[cite: 3, 8, 41].
* [cite_start]**Logística:** Puerto de carga (Xingang, China) y puerto de descarga (Callao, Perú)[cite: 13, 14, 46, 47].
* [cite_start]**Especificaciones:** * Productos como Tubos Redondos y Cuadrados (A500 Grado A)[cite: 12, 15, 45].
    * [cite_start]Dimensiones: Diámetro, espesor de pared y longitud[cite: 15, 31, 48].
* [cite_start]**Finanzas:** * Precio unitario (USD/TON)[cite: 15, 31, 48].
    * [cite_start]Valor total por ítem y monto total de factura (ej. US$1,723,176.49)[cite: 15, 49].

## 🚀 Uso
1. Sube tus facturas PDF al repositorio.
2. [cite_start]Asegúrate de tener instaladas las librerías de `requirements.txt`[cite: 52].
3. Ejecuta `app.py` para generar el consolidado en Excel.
