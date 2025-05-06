import pdfplumber
from config.config import SEGURADORAS

def identificar_seguradora(arquivo_pdf):
    """
    Identifica qual seguradora emitiu a apólice de seguro.
    
    Args:
        arquivo_pdf: Caminho para o arquivo PDF
        
    Returns:
        str: Nome da seguradora identificada ou None se não for identificada
    """
    try:
        with pdfplumber.open(arquivo_pdf) as pdf:
            primeira_pagina = pdf.pages[0].extract_text().upper()
            
            for seguradora in SEGURADORAS:
                if seguradora in primeira_pagina:
                    return seguradora
            
            return None
    except Exception as e:
        print(f"Erro ao identificar seguradora: {e}")
        return None