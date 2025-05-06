
# extratores/__init__.py
from extratores.extratores_seguradoras.bradesco import ExtratorBradesco

# Dicionário de extratores por seguradora
EXTRATORES = {
    'BRADESCO': ExtratorBradesco
}

def obter_extrator(seguradora):
    """
    Obtém o extrator correto para a seguradora especificada.
    
    Args:
        seguradora: Nome da seguradora
        
    Returns:
        ExtratorBase: Instância do extrator adequado ou None se não encontrado
    """
    extrator_class = EXTRATORES.get(seguradora)
    if extrator_class:
        return extrator_class()
    return None