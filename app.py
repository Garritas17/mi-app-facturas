import pdfplumber
import pandas as pd
import os
import re

def extraer_datos_baolai(ruta_pdf):
    items_finales = []
    with pdfplumber.open(ruta_pdf) as pdf:
        # Extraer cabecera de la primera página
        texto_cab = pdf.pages[0].extract_text()
        
        # Captura el Número de Factura (ej: BLA20220516)
        fact_match = re.search(r'(?:NÚMERO DE FACTURA|INVOICE NO\.)[:\s]*\n*([A-Z0-9-]+)', texto_cab, re.IGNORECASE)
        if not fact_match:
            fact_match = re.search(r'BLA\d+[A-Z0-9]*', texto_cab)
        
        num_factura = fact_match.group(1) if fact_match and len(fact_match.groups()) > 0 else (fact_match.group(0) if fact_match else "No Identificado")
        
        # Captura RUC y Fecha
        ruc_match = re.search(r'RUC[:\s]*(\d+)', texto_cab)
        fecha_match = re.search(r'(?:FECHA|DATE)[:\s]*([\d\w/-]+)', texto_cab, re.IGNORECASE)

        for page in pdf.pages:
            tablas = page.extract_tables()
            for tabla in tablas:
                for fila in tabla:
                    # Validar si es una fila de producto (Item No.)
                    if fila and fila[0] and str(fila[0]).strip().isdigit():
                        # Limpieza de celdas
                        fila_l = [str(c).replace('\n', ' ').strip() if c else "" for c in fila]
                        
                        # Captura dinámica de las últimas columnas (Precio y Total)
                        monto_total = fila_l[-1] 
                        precio_unit = fila_l[-2] 

                        items_finales.append({
                            "Factura": num_factura,
                            "Fecha": fecha_match.group(1) if fecha_match else "N/A",
                            "RUC": ruc_match.group(1) if ruc_match else "20600853318",
                            "Item": fila_l[0],
                            "Producto": fila_l[1],
                            "Grado": fila
