import pdfplumber
from models.informacoes_seguro import InformacoesSeguro

class ExtratorBase():
    """
    Classe base para extratores de informações de seguros.
    Cada seguradora deve implementar sua própria classe extratora.
    """

    def __init__(self):
        self.nome_seguradora = ""

    def extrair_texto_completo(self, arquivo_pdf):
        """
        Extrai todo o texto do arquivo PDF.
        
        Args:
            arquivo_pdf: Caminho para o arquivo PDF
            
        Returns:
            str: Texto completo do PDF
        """
        texto_completo = ""
        try:
            with pdfplumber.open(arquivo_pdf) as pdf:
                for page in pdf.pages:
                    texto_completo += page.extract_text().upper()
            return texto_completo
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return ""
        
    def extrair_primeira_pagina(self, arquivo_pdf):
        """
        Extrai o texto apenas da primeira página do PDF.
        
        Args:
            arquivo_pdf: Caminho para o arquivo PDF
            
        Returns:
            str: Texto da primeira página do PDF
        """
        try:
            with pdfplumber.open(arquivo_pdf) as pdf:
                return pdf.pages[0].extract_text().upper()
        except Exception as e:
            print(f"Erro ao extrair primeira página do PDF: {e}")
            return ""
        
    
    def extrair_informacoes(self, texto, informacoes):
        """
        Método abstrato que deve ser implementado por cada extrator específico.
        
        Args:
            texto: Texto completo do PDF
            informacoes: Objeto InformacoesSeguro para preencher
            
        Returns:
            InformacoesSeguro: Objeto com as informações extraídas
        """
        pass

    def extrair_informacoes_pagamento(self, arquivo_pdf):
        """
        Método abstrato para extrair informações de pagamento.
        
        Args:
            arquivo_pdf: Caminho para o arquivo PDF
            
        Returns:
            dict: Dicionário com informações de pagamento
        """
        pass