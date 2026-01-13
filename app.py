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
            fecha_match = re.search(r'(?:FECHA|DATE)[:\s]*([\d\w/-]+)', texto_cabecera, re.IGNORECASE)
            ruc_match = re.search(r'RUC[:\s]*(\d+)', texto_cabecera)
            
            for page in pdf.pages:
                tablas = page.extract_tables()
                for tabla in tablas:
                    for fila in tabla:
                        if fila and fila[0] and str(fila[0]).strip().isdigit():
                            fila_l = [str(c).replace('\n', ' ').strip() if c else "" for c in fila]
                            # Captura de precios y totales (últimas columnas)
                            monto_total = fila_l[-1] 
                            precio_unit = fila_l[-2] 

                            items_finales.append({
                                "Invoice_No": val_factura,
                                "Date": fecha_match.group(1) if fecha_match else "N/A",
                                "RUC_Buyer": ruc_match.group(1) if ruc_match else "N/A",
                                "Item_No": fila_l[0],
                                "Products": fila_l[1],
                                "Grade": fila_l[2] if len(fila_l) > 2 else "",
                                "Diameter": fila_l[3] if len(fila_l) > 3 else "",
                                "PRECIO_UNITARIO_USD": limpiar_valor(precio_unit),
                                "VALOR_TOTAL_USD": limpiar_valor(monto_total)
                            })
    except Exception as e:
        print(f"Error en {ruta_pdf}: {e}")
    return items_finales

if __name__ == "__main__":
    resultados = []
    archivos = [f for f in os.listdir('.') if f.lower().endswith(".pdf")]
    for arc in archivos:
        resultados.extend(extraer_datos_baolai(arc))
    if resultados:
        pd.DataFrame(resultados).to_excel("reporte_final.xlsx", index=False)
