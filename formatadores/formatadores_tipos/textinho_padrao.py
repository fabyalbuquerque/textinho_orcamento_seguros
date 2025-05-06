from formatadores.formatador_base import FormatadorBase
from config.config import TIPOS_VIDROS

class TextinhoPadrao(FormatadorBase):
    """
    Formatador de texto específico para o tipo "Padrão".
    """

    def __init__(self):
        super().__init__()
        self.tipo_formatacao = "PADRAO"

    def formatar_textinho(self, informacoes):
        """
        Formata as informações do seguro em um texto para envio por WhatsApp.
        
        Args:
            informacoes: Objeto InformacoesSeguro com as informações a serem formatadas
            
        Returns:
            str: Texto formatado para envio por WhatsApp
        """
        textinho = f"*{informacoes.nome_seguradora} AUTO*\n"
        textinho += f"_Assistência 24 hrs: {informacoes.numero_assistencia}_\n\n\n"
        
        # Informações do segurado e condutor
        textinho += f"*SEGURADO:* {informacoes.nome_segurado}\n\n"
        textinho += f"*PRINCIPAL CONDUTOR:* {informacoes.nome_condutor}\n\n\n"
        
        # Informações do veículo
        textinho += f"*VEICULO:* {informacoes.modelo_veiculo}\n\n"
        textinho += f"*Tabela Fipe {informacoes.ajuste}*\n"
        textinho += f"*R$ {informacoes.fipe}*\n\n"
        textinho += f"*Franquia ({informacoes.franquia_tipo})*📢\n"
        textinho += f"*R$ {informacoes.franquia_valor}*\n\n\n"
        
        # Coberturas
        textinho += f"*COBERTURAS*\n"
        if informacoes.cobertura == 'compreensiva':
            textinho += f"🥇*Completo (Roubo, Furto, Colisão, Incêndio)*\n\n"
        else:
            textinho += f"*{informacoes.cobertura}*\n\n"
        
        # Coberturas RCF a terceiros
        if informacoes.danos_materiais or informacoes.danos_corporais or informacoes.danos_morais:
            textinho += f"*COBERTURAS RCF  A TERCEIROS*\n\n"
            
            if informacoes.danos_materiais:
                textinho += f"▪Danos Materiais: *R$ {informacoes.danos_materiais}*\n"
            if informacoes.danos_corporais:
                textinho += f"▪Danos Corporais: *R$ {informacoes.danos_corporais}*\n"
            if informacoes.danos_morais:
                textinho += f"▪Danos Morais: *R$ {informacoes.danos_morais}*\n"
        
        # Coberturas APP
        if informacoes.app_morte or informacoes.app_invalidez:
            textinho += f"\n*COBERTURAS-APP*\n\n"
            if informacoes.app_morte:
                textinho += f"▪️Acidente pessoais em caso de morte: *R$ {informacoes.app_morte}*\n"
            if informacoes.app_invalidez:
                textinho += f"▪️Acidente pessoais em caso de Invalidez: *R$ {informacoes.app_invalidez}*\n"
        
        # Assistências e serviços
        textinho += f"\n\n*Assistências e Serviços*\n\n"
        textinho += f"*GUINCHO Assist. Dia/Noite: {informacoes.guincho}*🚜🚗\n"
        textinho += f"Mecânico 👨🏾‍🔧\nChaveiro🔧\nTáxi 🚖\nBorracheiro 🛞\n\n"
        
        # Proteção de vidros
        textinho += f"*Proteção Vidros:*"
        if informacoes.vidros in TIPOS_VIDROS:
            textinho += f"\n*{TIPOS_VIDROS[informacoes.vidros]}*\n\n"
        else:
            textinho += " Não contratado\n\n"
            
        # Carro reserva
        if informacoes.carro_reserva:
            textinho += f"🚙*CARRO RESERVA:* {informacoes.carro_reserva} DIAS\n\n"
        
        # Serviços adicionais
        if informacoes.super_martelinho:
            textinho += f"*Super Martelinho*🛠\n"
        if informacoes.reparo_rapido:
            textinho += f"*Reparo Rápido*⚒\n\n"
        
        # Valor total
        textinho += f"💲Valor Total: *R$ {informacoes.premio_valor}*\n"
        
        return textinho