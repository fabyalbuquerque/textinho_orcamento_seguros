#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa para extração e formatação de informações de seguros.
"""

import os
import argparse
from models.informacoes_seguro import InformacoesSeguro
from utils.helpers import identificar_seguradora
from extratores import obter_extrator
from formatadores import obter_formatador

def processar_arquivo(arquivo_pdf, salvar_resultado=True):
    """
    Processa um arquivo PDF de cotação de seguro.
    
    Args:
        arquivo_pdf: Caminho para o arquivo PDF
        salvar_resultado: Se True, salva o resultado em um arquivo de texto
        
    Returns:
        str: Texto formatado para envio por WhatsApp
    """
    # Identifica a seguradora
    seguradora = identificar_seguradora(arquivo_pdf)
    if not seguradora:
        print("Não foi possível identificar a seguradora.")
        return None
    
    print(f"Seguradora identificada: {seguradora}")
    
    # Obtém o extrator e o formatador para a seguradora
    extrator = obter_extrator(seguradora)
    formatador = obter_formatador(tipo="PADRAO")
    
    if not extrator or not formatador:
        print(f"Não foi possível obter o extrator ou formatador para a seguradora {seguradora}.")
        return None
    
    # Cria um objeto para armazenar as informações
    informacoes = InformacoesSeguro()
    
    # Extrai o texto completo do PDF
    texto_completo = extrator.extrair_texto_completo(arquivo_pdf)
    if not texto_completo:
        print("Não foi possível extrair texto do PDF.")
        return None
    
    # Extrai as informações do seguro
    informacoes = extrator.extrair_informacoes(texto_completo, informacoes)
    
    # Extrai informações de pagamento (opcional)
    try:
        informacoes.pagamento = extrator.extrair_informacoes_pagamento(arquivo_pdf)
    except Exception as e:
        print(f"Aviso: Não foi possível extrair informações de pagamento: {e}")
    
    # Formata o textinho para WhatsApp
    textinho = formatador.formatar_textinho(informacoes)
    
    # Exibe o textinho na tela
    print("\n\n=== TEXTINHO PARA WHATSAPP ===\n")
    print(textinho)
    
    # Salva o resultado em um arquivo de texto se solicitado
    if salvar_resultado:
        nome_arquivo = f"textinho_{seguradora.lower()}_{os.path.basename(arquivo_pdf).split('.')[0]}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(textinho)
        print(f"\nTextinho salvo em: {nome_arquivo}")
    
    return textinho

def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(description="Extrai informações de cotações de seguros.")
    parser.add_argument("arquivo", help="Caminho para o arquivo PDF da cotação")
    parser.add_argument("--no-save", action="store_true", help="Não salvar o resultado em arquivo")
    args = parser.parse_args()
    
    processar_arquivo(args.arquivo, not args.no_save)

if __name__ == "__main__":
    main()



# # Caminho do arquivo PDF
# arquivo_pdf = 'D:\Job\Vision\cotacao_KAMER INDUSTRIA E COMERCIO DE EQUIPAMENT_08-04717428953 (1).pdf'

# # Processar o arquivo e gerar o texto formatado
# texto_formatado = processar_arquivo_pdf(arquivo_pdf)

# # Exibir o texto formatado
# print(texto_formatado)