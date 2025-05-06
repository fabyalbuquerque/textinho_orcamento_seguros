# formatadores/__init__.py
from formatadores.formatadores_tipos.textinho_padrao import TextinhoPadrao

# Dicionário de formatadores por seguradora
FORMATADORES = {
    'PADRAO': TextinhoPadrao
}

def obter_formatador(tipo):
    """
    Obtém o formatador correto para a seguradora especificada.
    
    Args:
        seguradora: Nome da seguradora
        
    Returns:
        FormatadorBase: Instância do formatador adequado ou None se não encontrado
    """
    formatador_class = FORMATADORES.get(tipo)
    if formatador_class:
        return formatador_class()
    return None