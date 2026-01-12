import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io

# 1. Configuración de la API de Google AI Studio
# REEMPLAZA LAS COMILLAS CON TU LLAVE REAL
genai.configure(api_key=AIzaSyAsSDEF7S7kq7hXS6uyFpI7P9SaVZHgQFY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuración de la página
st.set_page_config(page_title="Extractor de Facturas AI", layout="centered")

st.title("🚀 Extractor de Facturas Inteligente")
st.write("Sube tus archivos (PDF o Imagen) y Gemini extraerá los datos para tu Excel.")

# 2. Widget para subir archivos
uploaded_files = st.file_uploader("Elige tus facturas", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

if uploaded_files:
    datos_extraidos = []
    
    with st.spinner('Procesando facturas con Inteligencia Artificial...'):
        for file in uploaded_files:
            # Leer el contenido del archivo
            file_bytes = file.read()
            
            # Instrucción para la IA
            prompt = """
            Analiza esta factura y extrae los siguientes campos:
            - Fecha
            - Emisor (Nombre de la empresa)
            - RFC o Identificación Fiscal
            - Monto Total
            - Impuestos
            
            Responde ÚNICAMENTE en formato JSON puro, sin texto adicional. 
            Ejemplo: {"Fecha": "01/01/2026", "Emisor": "Tienda X", "RFC": "ABC12345", "Total": 100.00, "Impuestos": 16.00}
            """
            
            try:
                # Llamada al modelo de Google
                response = model.generate_content([
                    prompt,
                    {'mime_type': file.type, 'data': file_bytes}
                ])
                
                # Limpiar la respuesta (quitar marcas de markdown ```json )
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                # Guardar nombre del archivo para referencia
                data['Archivo_Origen'] = file.name
                datos_extraidos.append(data)
                
            except Exception as e:
                st.error(f"Error procesando {file.name}: {e}")

    if datos_extraidos:
        # 3. Mostrar tabla de resultados
        df = pd.DataFrame(datos_extraidos)
        st.success("✅ ¡Procesamiento completado!")
        st.subheader("Vista previa de datos")
        st.dataframe(df)

        # 4. Crear el archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel
