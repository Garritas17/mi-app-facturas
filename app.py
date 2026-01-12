import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io

# 1. Configuración de la API con la versión específica para evitar el error 404
# ASEGÚRATE DE PEGAR TU API KEY AQUÍ ABAJO
genai.configure(api_key="AIzaSyAsSDEF7S7kq7hXS6uyFpI7P9SaVZHgQFY")

# Hemos cambiado el nombre del modelo a la versión estable específica
model = genai.GenerativeModel('gemini-1.5-flash-001') 

st.set_page_config(page_title="Extractor de Facturas AI", layout="centered")

st.title("🚀 Extractor de Facturas Inteligente")
st.write("Sube tus archivos de PRECOR o cualquier otra empresa y Gemini extraerá los datos.")

uploaded_files = st.file_uploader("Elige tus facturas (PDF o Imagen)", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

if uploaded_files:
    datos_extraidos = []
    
    with st.spinner('Procesando factura...'):
        for file in uploaded_files:
            file_bytes = file.read()
            
            # Prompt optimizado para tu factura de PRECOR S.A.
            prompt = """
            Actúa como un experto contable. Analiza esta factura y extrae los datos en este formato JSON exacto:
            {
              "RUC_Emisor": "RUC del vendedor",
              "Emisor": "Nombre de la empresa",
              "Comprobante": "Serie y número (ej. F001-39541)",
              "Fecha": "YYYY-MM-DD",
              "Cliente": "Nombre del cliente",
              "RUC_Cliente": "RUC del cliente",
              "Moneda": "Moneda",
              "Total": 0.00
            }
            Responde únicamente el objeto JSON.
            """
            
            try:
                # Se envía el archivo a Gemini
                response = model.generate_content([
                    prompt,
                    {'mime_type': file.type, 'data': file_bytes}
                ])
                
                # Limpiar la respuesta de posibles caracteres extraños
                texto = response.text.strip()
                if "```json" in texto:
                    texto = texto.split("```json")[1].split("```")[0]
                
                data = json.loads(texto)
                data['Archivo'] = file.name
                datos_extraidos.append(data)
                
            except Exception as e:
                st.error(f"Error en {file.name}: {e}")

    if datos_extraidos:
        df = pd.DataFrame(datos_extraidos)
        st.success("✅ Procesado correctamente")
        st.dataframe(df)

        # Botón para descargar Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="reporte_facturas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
