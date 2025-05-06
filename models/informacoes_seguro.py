# Modelo para armazenar informações do seguro

class InformacoesSeguro:
    def __init__(self):
        self.nome_seguradora = ''
        self.numero_assistencia = ''
        self.nome_segurado = ''
        self.nome_condutor = ''
        self.modelo_veiculo = ''
        self.ajuste = ''
        self.fipe = ''
        self.franquia_tipo = ''
        self.franquia_valor = ''
        self.cobertura = ''
        self.danos_materiais = ''
        self.danos_corporais = ''
        self.danos_morais = ''
        self.app_morte = ''
        self.app_invalidez = ''
        self.guincho = ''
        self.vidros = ''
        self.carro_reserva = ''
        self.super_martelinho = False
        self.reparo_rapido = False
        self.premio_valor = ''
        self.pagamento = {}
        
    def __str__(self):
        """Retorna uma representação em string das informações do seguro."""
        return f"Seguro {self.nome_seguradora} para {self.nome_segurado}, veículo {self.modelo_veiculo}"