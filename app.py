import pdfplumber
import pandas as pd
import os
import re

def limpiar_valor(v):
    if v is None or v == "": return 0.0
    limpio = re.sub(r'[^\d.]', '', str(v).replace(',', ''))
    try: return float(limpio)
    except: return 0.0

def extraer_datos_baolai(ruta_pdf):
    items_finales = []
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto_cabecera = pdf.pages[0].extract_text()
            factura_match = re.search(r'BLA\d+[A-Z0-9]*', texto_cabecera)
            val_factura = factura_match.group(0) if factura_match else "No Identificado"
            
            for page in pdf.pages:
                tablas = page.extract_tables()
                for tabla in tablas:
                    for fila in tabla:
                        if fila and fila[0] and str(fila[0]).strip().isdigit():
                            fila_l = [str(c).replace('\n', ' ').strip() if c else "" for c in fila]
                            items_finales.append({
                                "Invoice_No": val_factura,
                                "Item_No": fila_l[0],
                                "Products": fila_l[1],
                                "PRECIO_UNITARIO_USD": limpiar_valor(fila_l[-2]),
                                "VALOR_TOTAL_USD": limpiar_valor(fila_l[-1])
                            })
    except Exception as e:
        print(f"Error: {e}")
    return items_finales

if __name__ == "__main__":
    resultados = []
    archivos = [f for f in os.listdir('.') if f.lower().endswith(".pdf")]
    for arc in archivos:
        resultados.extend(extraer_datos_baolai(arc))
    if resultados:
        pd.DataFrame(resultados).to_excel("reporte_final.xlsx", index=False)
