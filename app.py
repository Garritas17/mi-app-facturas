import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io

# 1. Configuración de la API (Usa gemini-1.5-flash directamente)
genai.configure(api_key="AIzaSyAsSDEF7S7kq7hXS6uyFpI7P9SaVZHgQFY")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Extractor de Facturas AI", layout="centered")

st.title("🚀 Extractor de Facturas Inteligente")
st.write("Sube tus archivos y Gemini extraerá los datos automáticamente.")

uploaded_files = st.file_uploader("Elige tus facturas", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

if uploaded_files:
    datos_extraidos = []
    
    with st.spinner('Procesando con Inteligencia Artificial...'):
        for file in uploaded_files:
            file_bytes = file.read()
            
            # PROMPT AJUSTADO PARA TU FACTURA DE PRECOR
            prompt = """
            Analiza esta factura y extrae los datos en este formato JSON exacto:
            {
              "RUC_Emisor": "RUC de quien vende",
              "Emisor": "Nombre de la empresa vendedora",
              "Serie_Numero": "Serie y número de factura (ej: F001-39541)",
              "Fecha": "Fecha de emisión",
              "Cliente": "Nombre del cliente",
              "RUC_Cliente": "RUC del cliente",
              "Moneda": "Moneda de la factura",
              "Subtotal": 0.00,
              "IGV": 0.00,
              "Total": 0.00
            }
            Responde SOLO el JSON, sin texto adicional.
            """
            
            try:
                response = model.generate_content([
                    prompt,
                    {'mime_type': file.type, 'data': file_bytes}
                ])
                
                # Limpieza de formato markdown
                texto_limpio = response.text.strip().replace("```json", "").replace("```", "")
                data = json.loads(texto_limpio)
                data['Archivo_Origen'] = file.name
                datos_extraidos.append(data)
                
            except Exception as e:
                st.error(f"Error en {file.name}: {e}")

    if datos_extraidos:
        df = pd.DataFrame(datos_extraidos)
        st.success("✅ ¡Hecho!")
        st.dataframe(df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Facturas')
        
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="reporte_facturas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
