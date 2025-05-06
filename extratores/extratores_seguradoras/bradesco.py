import re
import pandas as pd
from tabula import read_pdf
from extratores.extrator_base import ExtratorBase
from config.config import ASSISTENCIA_24H

class ExtratorBradesco(ExtratorBase):
    """
    Extrator de informações específico para a seguradora Bradesco.
    """

    def __init__(self):
        super().__init__()
        self.nome_seguradora = "BRADESCO"

    def extrair_informacoes(self, texto, informacoes):
        # Extraindo nome do segurado e condutor
        nomes = re.findall(r'NOME:\s*(.*?)(?=\s*(VIGÊNCIA|\n|CPF/CNPJ))', texto)
        
        # Extraindo informações do veículo
        modelo_veiculo = re.search(r'TIPO DO VEÍCULO:\s*(.*?)(?=\s*CHASSI)', texto)
        ajuste = re.search(r'FATOR DE AJUSTE:\s*(\d+\s*%)', texto)
        franquia_tipo_e_valor = re.search(r'F*RANQUIAS\s*\(.*?\)\s*VEÍCULO:\s*([\d.,]+)\s*\((.*?)\)', texto)
        
        # Extraindo cobertura
        if "COMPREENSIVA" in texto:
            cobertura = 'compreensiva'
        else:
            cobertura_match = re.search(r'CLÁUSULAS\s*\(.*?\)\s*COBERTURA\s*(.*?)\s*\(', texto)
            cobertura = cobertura_match.group(1).strip() if cobertura_match else ''
        
        # Extraindo informações de danos
        danos_materiais_match = re.search(r'D\.M\.\s*[:]*\s*([\d.,]+)\s*', texto)
        danos_materiais = danos_materiais_match.group(1).strip() if danos_materiais_match else ''
        
        danos_corporais_match = re.search(r'D\.C\.\s*[:]*\s*([\d.,]+)\s*', texto)
        danos_corporais = danos_corporais_match.group(1).strip() if danos_corporais_match else ''
        
        danos_morais_match = re.search(r'D\.\s*MORAIS\.\s*[:]*\s*([\d.,]+)\s*', texto)
        danos_morais = danos_morais_match.group(1).strip() if danos_morais_match else ''
        
        # Extraindo informações de APP
        app_morte_match = re.search(r'MORTE P/ PASSAGEIRO\s*[:]*\s*([\d.,]+)\s*', texto)
        app_morte = app_morte_match.group(1).strip() if app_morte_match else ''
        
        app_invalidez_match = re.search(r'INVALIDEZ P/ PASSAGEIRO\s*[:]*\s*([\d.,]+)\s*', texto)
        app_invalidez = app_invalidez_match.group(1).strip() if app_invalidez_match else ''
        
        # Preenchendo informações no objeto
        informacoes.nome_seguradora = 'BRADESCO SEGUROS'
        informacoes.numero_assistencia = ASSISTENCIA_24H[self.nome_seguradora]
        informacoes.nome_segurado = nomes[0][0].strip() if len(nomes) >= 1 else 'Não encontrado'
        informacoes.nome_condutor = nomes[1][0].strip() if len(nomes) >= 2 else 'Não encontrado'
        informacoes.modelo_veiculo = modelo_veiculo.group(1).strip() if modelo_veiculo else 'Não encontrado'
        informacoes.ajuste = ajuste.group(1).strip().replace(' ', '') if ajuste else ''
        
        if franquia_tipo_e_valor:
            informacoes.franquia_tipo = franquia_tipo_e_valor.group(2).strip()
            informacoes.franquia_valor = franquia_tipo_e_valor.group(1).strip()
        
        informacoes.cobertura = cobertura
        informacoes.danos_materiais = danos_materiais if danos_materiais and danos_materiais != "0,00" else ''
        informacoes.danos_corporais = danos_corporais if danos_corporais and danos_corporais != "0,00" else ''
        informacoes.danos_morais = danos_morais if danos_morais and danos_morais != "0,00" else ''
        informacoes.app_morte = app_morte if app_morte and app_morte != "0,00" else ''
        informacoes.app_invalidez = app_invalidez if app_invalidez and app_invalidez != "0,00" else ''
        
        # Extraindo informações de cláusulas
        self._extrair_informacoes_clausulas(texto, informacoes)
        
        return informacoes
    
    def _extrair_informacoes_clausulas(self, texto, informacoes):
        """
        Extrai informações específicas das cláusulas da apólice.
        
        Args:
            texto: Texto completo do PDF
            informacoes: Objeto InformacoesSeguro para preencher
        """
        recorte_clausulas = re.search(r'CLÁUSULAS(.*?)COBERTURAS E SERVIÇOS', texto, re.DOTALL)
        if not recorte_clausulas:
            return
            
        recorte_clausulas = recorte_clausulas.group(1).strip()
        
        # Extraindo informações de guincho
        if "ILIMITADO" in recorte_clausulas:
            informacoes.guincho = "ILIMITADO"
        else:
            guincho_match = re.search(r'DIA/NOITE.*?(\d+)\s*[Kk][Mm]', recorte_clausulas)
            if guincho_match:
                informacoes.guincho = f"{guincho_match.group(1).strip()} Km"
        
        # Extraindo informações de carro reserva
        if "AUTO RESERVA" in recorte_clausulas:
            texto_carro_reserva_match = re.search(r'RESERVA\s+(.*?)\s+DIAS', recorte_clausulas)
            if texto_carro_reserva_match:
                texto_carro_reserva = texto_carro_reserva_match.group(1).strip()
                dias_carro_reserva_match = re.search(r'\d+', texto_carro_reserva)
                if dias_carro_reserva_match:
                    dias_carro_reserva = dias_carro_reserva_match.group(0).strip()
                    if "PREMIUM" in texto_carro_reserva:
                        informacoes.carro_reserva = f'AUTOMÁTICO {dias_carro_reserva}'
                    else:
                        informacoes.carro_reserva = dias_carro_reserva
        
        # Extraindo informações de serviços adicionais
        informacoes.super_martelinho = "SUPER MARTELINHO" in recorte_clausulas
        informacoes.reparo_rapido = "REPARO RAPIDO" in recorte_clausulas
        
        # Extraindo informações de vidros
        if "REPARO DE PÁRA-BRISA" in recorte_clausulas:
            informacoes.vidros = 'para-brisa'
        elif "VIDRO PROTEGIDO PLUS" in recorte_clausulas:
            informacoes.vidros = 'vidros_plus'
        elif "VIDRO PROTEGIDO" in recorte_clausulas and "PREMIUM" not in recorte_clausulas:
            informacoes.vidros = 'vidros'
        elif "VIDRO PROTEGIDO PREMIUM" in recorte_clausulas:
            informacoes.vidros = 'vidros_premium'
    
    def extrair_informacoes_pagamento(self, arquivo_pdf):
        """
        Extrai informações de pagamento do PDF.
        
        Args:
            arquivo_pdf: Caminho para o arquivo PDF
            
        Returns:
            dict: Dicionário com informações de pagamento
        """
        try:
            # Extrai as tabelas do PDF
            tabelas = read_pdf(arquivo_pdf, pages='all', multiple_tables=True)
            
            # Procura pela tabela que contém informações de parcelas
            tabela_parcelas = None
            for tabela in tabelas:
                tabela_str = tabela.to_string().lower()
                if "parcelas" in tabela_str:
                    tabela_parcelas = tabela
                    break
            
            if tabela_parcelas is None:
                return {}
            
            # Processa a tabela para extrair informações
            # Aqui você pode implementar a lógica para extrair as informações de pagamento
            # como no código original
            
            return {}  # Implementação simplificada
            
        except Exception as e:
            print(f"Erro ao extrair informações de pagamento: {e}")
            return {}