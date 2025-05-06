from models.informacoes_seguro import InformacoesSeguro

class FormatadorBase():
    """
    Classe base para formatadores de texto de seguros.
    Cada seguradora pode implementar seu próprio formatador.
    """

    def __init__(self):
        self.tipo_formatacao = ""

    def formatar_textinho(self, informacoes):
        """
        Método abstrato que deve ser implementado por cada formatador específico.
        
        Args:
            informacoes: Objeto InformacoesSeguro com as informações a serem formatadas
            
        Returns:
            str: Texto formatado para envio por WhatsApp
        """
        pass