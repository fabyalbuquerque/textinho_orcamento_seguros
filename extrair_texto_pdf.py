import pdfplumber
from tabula import read_pdf, convert_into
import re
import pandas as pd

seguradoras = ['BRADESCO', 'ALLIANZ', 'AZUL', 'PORTO', 'TOKIO']

assistencia_24h = {
    'BRADESCO': '0800 701 275',
    'ALLIANZ': '0800 123 456',
    'AZUL': '0800 999 888',
    'PORTO': '0800 555 444',
    'TOKIO': '0800 777 666'
}

informacoes_textinho = {
    'nome_seguradora': '',
    'numero_assistencia': '',
    'nome_segurado': '',
    'nome_condutor': '',
    'modelo_veiculo': '',
    'ajuste': '',
    'fipe': '',
    'franquia_tipo': '',
    'franquia_valor': '',
    'cobertura': '',
    'danos materiais': '',
    'danos corporais': '',
    'danos morais': '',
    'app_morte': '',
    'app_invalidez': '',
    'guincho': '',
    'vidros': '',
    'carro_reserva': '',
    'super_martelinho': False,
    'reparo_rapido': False,
    'premio_valor': '',
    'pagamento':'',

}


def cria_textinho(informacoes):
    # Cria o texto padronizado
    textinho = f"*{informacoes['nome_seguradora']} AUTO*\n"
    textinho += f"_Assistência 24 hrs: {informacoes['numero_assistencia']}_\n\n\n"
    textinho += f"*SEGURADO:* {informacoes['nome_segurado']}\n\n"
    textinho += f"*PRINCIPAL CONDUTOR:* {informacoes['nome_condutor']}\n\n\n"
    textinho += f"*VEICULO:* {informacoes['modelo_veiculo']}\n\n"
    textinho += f"*Tabela Fipe {informacoes['ajuste']}*\n"
    textinho += f"*R$ {informacoes['fipe']}*\n\n"
    textinho += f"*Franquia ({informacoes['franquia_tipo']})*📢\n"
    textinho += f"*R$ {informacoes['franquia_valor']}*\n\n\n"

    textinho += f"*COBERTURAS*\n"
    if informacoes['cobertura'] == 'compreensiva':
        textinho += f"🥇*Completo (Roubo, Furto, Colisão, Incêndio)*\n\n"
    else:
        textinho += f"*{informacoes['cobertura']}*\n\n"

    if informacoes['danos_materiais'] or informacoes['danos_corporais'] or informacoes['danos_morais']:
        textinho += f"*COBERTURAS RCF  A TERCEIROS*\n\n"

        if informacoes['danos_materiais']:
            textinho += f"▪Danos Materiais: *R$ {informacoes['danos_materiais']}*\n"
        if informacoes['danos_corporais']:
            textinho += f"▪Danos Corporais: *R$ {informacoes['danos_corporais']}*\n"
        if informacoes['danos_morais']:
            textinho += f"▪Danos Morais: *R$ {informacoes['danos_morais']}*\n"
    
    if informacoes['app_morte'] or informacoes['app_invalidez']:
        textinho += f"\n*COBERTURAS-APP*\n\n"
        if informacoes['app_morte']:
            textinho += f"▪️Acidente pessoais em caso de morte: *R$ {informacoes['app_morte']}*\n"
        if informacoes['app_invalidez']:
            textinho += f"▪️Acidente pessoais em caso de Invalidez: *R$ {informacoes['app_invalidez']}*\n"
        
    textinho += f"\n\n*Assistências e Serviços*\n\n"
    textinho += f"*GUINCHO Assist. Dia/Noite: {informacoes['guincho']}*🚜🚗\n"
    textinho += f"Mecânico 👨🏾‍🔧\nChaveiro🔧\nTáxi 🚖\nBorracheiro 🛞\n\n"

    textinho += f"*Proteção Vidros:*"
    if informacoes['vidros'] == 'para-brisa':
        textinho += f" *Para-Brisa*\n\n"
    elif informacoes['vidros'] == 'vidros':
        textinho += f"\n*Para-Brisa, Vidro Traseiro, Vidros Laterais*\n\n"
    elif informacoes['vidros'] == 'vidros_plus':
        textinho += f"\n*Para-Brisa, Vidro Traseiro, Vidros Laterais, Faróis, Lanternas e Retrovisores*\n\n"
    elif informacoes['vidros'] == 'vidros_premium':
        textinho += f"\n*Para-Brisa, Vidro Traseiro, Vidros Laterais, Faróis, Lanternas, Retrovisores e Teto Solar*\n\n"
    
    if informacoes['carro_reserva']:
        textinho += f"🚙*CARRO RESERVA:* {informacoes['carro_reserva']} DIAS\n\n"

    if informacoes['super_martelinho']:
        textinho += f"*Super Martelinho*🛠\n"
    if informacoes['reparo_rapido']:
        textinho += f"*Reparo Rápido*⚒\n\n"
    
    textinho += f"💲Valor Total: *R$ {informacoes['premio_valor']}*\n"



    return textinho

def encontra_informacoes(texto, seguradora, informacoes_textinho):


    if seguradora == 'BRADESCO':
        nomes = re.findall(r'NOME:\s*(.*?)(?=\s*(VIGÊNCIA|\n|CPF/CNPJ))', texto)
        modelo_veiculo = re.search(r'TIPO DO VEÍCULO:\s*(.*?)(?=\s*CHASSI)', texto)
        ajuste = re.search(r'FATOR DE AJUSTE:\s*(.*?%)', texto)
        franquia_tipo_e_valor = re.search(r'F*RANQUIAS\s*\(.*?\)\s*VEÍCULO:\s*([\d.,]+)\s*\((.*?)\)', texto)

        if "COMPREENSIVA" in texto:
            cobertura = 'compreensiva'
        else:
            cobertura = re.search(r'CLÁUSULAS\s*\(.*?\)\s*COBERTURA\s*(.*?)\s*\(', texto).group(1).strip()

        danos_materiais = re.search(r'D\.M\.\s*[:]*\s*([\d.,]+)\s*', texto).group(1).strip()
        danos_corporais = re.search(r'D\.C\.\s*[:]*\s*([\d.,]+)\s*', texto).group(1).strip()
        danos_morais = re.search(r'D\.\s*MORAIS\.\s*[:]*\s*([\d.,]+)\s*', texto).group(1).strip()
        app_morte = re.search(r'MORTE P/ PASSAGEIRO\s*[:]*\s*([\d.,]+)\s*', texto).group(1).strip()
        app_invalidez = re.search(r'INVALIDEZ P/ PASSAGEIRO\s*[:]*\s*([\d.,]+)\s*', texto).group(1).strip()
 
        informacoes_textinho['nome_seguradora'] = 'BRADESCO SEGUROS'
        informacoes_textinho['numero_assistencia'] = assistencia_24h[seguradora]
        informacoes_textinho['nome_segurado'] = nomes[0][0].strip() if len(nomes) >= 1 else 'Não encontrado'
        informacoes_textinho['nome_condutor'] = nomes[1][0].strip() if len(nomes) >= 2 else 'Não encontrado'
        informacoes_textinho['modelo_veiculo'] = modelo_veiculo.group(1).strip() if modelo_veiculo else 'Não encontrado'
        informacoes_textinho['ajuste'] = ajuste.group(1).strip()
        informacoes_textinho['franquia_tipo'] = franquia_tipo_e_valor.group(2).strip()
        informacoes_textinho['franquia_valor'] = franquia_tipo_e_valor.group(1).strip()
        informacoes_textinho['cobertura'] = cobertura
        informacoes_textinho['danos_materiais'] = danos_materiais if danos_materiais and danos_materiais != "0,00" else ''
        informacoes_textinho['danos_corporais'] = danos_corporais if danos_corporais and danos_corporais != "0,00" else ''
        informacoes_textinho['danos_morais'] = danos_morais if danos_morais and danos_morais != "0,00" else ''
        informacoes_textinho['app_morte'] = app_morte if app_morte and app_morte != "0,00" else ''
        informacoes_textinho['app_invalidez'] = app_invalidez if app_invalidez and app_invalidez != "0,00" else ''
        
        recorte_clausulas = re.search(r'CLÁUSULAS(.*?)COBERTURAS E SERVIÇOS', texto, re.DOTALL)
        if recorte_clausulas:
            recorte_clausulas = recorte_clausulas.group(1).strip()

            if "ILIMITADO" in recorte_clausulas:
                guincho = "ILIMITADO"
            else:
                guincho = re.search(r'DIA/NOITE.*?(\d+)\s+KM', recorte_clausulas).group(1).strip()
                guincho = guincho + " Km"

            informacoes_textinho['guincho'] = guincho

            if "AUTO RESERVA" in recorte_clausulas:
                texto_carro_reserva = re.search(r'RESERVA\s+(.*?)\s+DIAS', recorte_clausulas).group(1).strip()
                dias_carro_reserva = re.search(r'\d+', texto_carro_reserva).group(0).strip()
                if "PREMIUM" in texto_carro_reserva:
                    carro_reserva = f'AUTOMÁTICO {dias_carro_reserva}'
                else:
                    carro_reserva = dias_carro_reserva
            else:
                carro_reserva = ''
            
            informacoes_textinho['carro_reserva'] = carro_reserva

            if "SUPER MARTELINHO" in recorte_clausulas:
                informacoes_textinho['super_martelinho'] = True
            if "REPARO RAPIDO" in recorte_clausulas:
                informacoes_textinho['reparo_rapido'] = True
            
            if "REPARO DE PÁRA-BRISA" in recorte_clausulas:
                informacoes_textinho['vidros'] = 'para-brisa'

            elif "VIDRO PROTEGIDO PLUS" in recorte_clausulas:
                informacoes_textinho['vidros'] = 'vidros_plus'

            elif "VIDRO PROTEGIDO" in recorte_clausulas:
                informacoes_textinho['vidros'] = 'vidros'

            elif "VIDRO PROTEGIDO PREMIUM" in recorte_clausulas:
                informacoes_textinho['vidros'] = 'vidros_premium'
    

        return informacoes_textinho
    

# def encontra_informacoes_pagamento(arquivo_pdf, seguradora):

#     informacoes_pagamento = [
#         debito_em_conta = {'max_vezes_sem_juros': 'max_parcela_sem_juros'},
#         cartao_de_credito = {'max_vezes_sem_juros': 'max_parcela_sem_juros'}, 
#         boleto = {'max_vezes_sem_juros': 'max_parcela_sem_juros'}, 
#     ]

#     if seguradora == 'BRADESCO':
#         tabelas = read_pdf(arquivo_pdf, pages='all', multiple_tables=True)

#         tabela_parcelas = None
#         for i, tabela in enumerate(tabelas):
#             tabela_str = tabela.to_string().lower()
#             if "parcelas" in tabela_str:
#                 print(f"Tabela com 'parcelas' encontrada (índice {i}):")
#                 print(tabela)
#                 tabela_parcelas = tabela
#                 break

#         if tabela_parcelas is not None:
#             tabela_parcelas.to_csv("tabela_parcelas.csv", index=False)
#             print("Tabela salva como 'tabela_parcelas.csv'")
#         else:
#             print("Nenhuma tabela contendo a palavra 'parcelas' foi encontrada")
        
#         tabela_parcelas = pd.read_csv("tabela_parcelas.csv")

#         nova_tabela = pd.DataFrame()

#         # Iterar sobre as colunas para reorganizar as informações
#         nova_tabela['Débito em Conta Parcelas'] = tabela['Débito em Conta'].str.split(' ', expand=True)[0]
#         nova_tabela['Débito em Conta Total'] = tabela['Débito em Conta'].str.split(' ', expand=True)[1]
#         nova_tabela['Cartão de Crédito Bradesco Parcelas'] = tabela['Cartão de Crédito Bradesco'].str.split(' ', expand=True)[0]
#         nova_tabela['Cartão de Crédito Bradesco Total'] = tabela['Cartão de Crédito Bradesco'].str.split(' ', expand=True)[1]
#         nova_tabela['Cartão de Crédito Parcelas'] = tabela['Cartão de Crédito'].str.split(' ', expand=True)[0]
#         nova_tabela['Cartão de Crédito Total'] = tabela['Cartão de Crédito'].str.split(' ', expand=True)[1]
#         nova_tabela['Carnê Parcelas'] = tabela['Carnê'].str.split(' ', expand=True)[0]
#         nova_tabela['Carnê Total'] = tabela['Carnê'].str.split(' ', expand=True)[1]

#         # Adicionar a coluna "Unnamed: 0" que contém o índice das parcelas
#         nova_tabela['Parcelas'] = tabela['Unnamed: 0']

#         # Reorganizar as colunas
#         nova_tabela = nova_tabela[['Parcelas', 'Débito em Conta Parcelas', 'Débito em Conta Total',
#                                 'Cartão de Crédito Bradesco Parcelas', 'Cartão de Crédito Bradesco Total',
#                                 'Cartão de Crédito Parcelas', 'Cartão de Crédito Total',
#                                 'Carnê Parcelas', 'Carnê Total']]

#         # Salvar a tabela reorganizada em um novo arquivo CSV
#         nova_tabela.to_csv("tabela_parcelas_reorganizada.csv", index=False)

#         tabela = pd.read_csv("tabela_parcelas_reorganizada.csv")

#         valor_anterior = None
#         linha_mudanca = None
#         for i, valor in enumerate(tabela['Débito em Conta Total']):
#             if valor_anterior is not None and valor != valor_anterior:
#                 linha_mudanca = i
#                 break
#             valor_anterior = valor

#         if linha_mudanca is not None:
#             # Encontrar o valor da linha anterior (linha_mudanca - 1)
#             debito_em_conta_max_vezes_sem_juros = tabela.iloc[linha_mudanca - 1]['Parcelas']
#             debito_em_conta_max_parcela_sem_juros = tabela.iloc[linha_mudanca - 1]['Débito em Conta Parcelas']
#         informacoes_pagamento['debito_em_conta'[]]


def encontra_seguradora(arquivo_pdf):

    with pdfplumber.open(arquivo_pdf) as pdf:
        primeira_pagina = pdf.pages[0].extract_text()
        
        texto_completo = ""  
        # Itera sobre todas as páginas do PDF
        for page in pdf.pages:
            texto_completo += page.extract_text().upper() 

        # with open("saida.txt", "w", encoding="utf-8") as f:
        #     f.write(texto_completo)

        for seguradora in seguradoras:
            if seguradora in primeira_pagina.upper():
                achei = True
                break
            
        if achei:
            informacoes = encontra_informacoes(texto_completo, seguradora, informacoes_textinho)
            # informacoes_pagamento = encontra_informacoes_pagamento(arquivo_pdf, seguradora)
            # informacoes_pagamento = ''

            textinho = cria_textinho(informacoes)
            print(textinho)
            print("continua...")



arquivo_pdf = 'D:\\Job\\Vision\\'


encontra_seguradora(arquivo_pdf)
