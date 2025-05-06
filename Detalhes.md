# Gerador de Textinhos de Seguros Auto

Este projeto automatiza a extração de informações de cotações de seguros automotivos e formata um texto padronizado para envio via WhatsApp.

## Funcionalidades

- Extração automática de informações de PDFs de cotação de seguros
- Formatação padronizada para envio por WhatsApp, incluindo emojis e formatação
- Interface web para upload e processamento de arquivos PDF
- Sistema extensível para adicionar suporte a novas seguradoras

## Seguradoras suportadas

- Bradesco Seguros

## Estrutura do projeto

O projeto segue uma arquitetura modular e orientada a objetos, facilitando a adição de novas seguradoras:

```
seguros_auto/
├── main.py                      # Script para uso via linha de comando
├── app.py                       # Aplicação web Flask
├── config/                      # Configurações globais
├── extratores/                  # Classes para extração de informações
├── formatadores/                # Classes para formatação de textos
├── modelos/                     # Modelos de dados
├── templates/                   # Templates da interface web
└── utils/                       # Funções utilitárias
```

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/seguros-auto.git
cd seguros-auto
```

2. Crie um ambiente virtual e instale as dependências:
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

### Via linha de comando

```
python main.py caminho/para/arquivo.pdf
```

### Via interface web

1. Inicie a aplicação web:
```
python app.py
```

2. Acesse http://localhost:5000 no navegador
3. Faça upload do PDF de cotação
4. O sistema processará o arquivo e exibirá o textinho formatado

## Como adicionar suporte a uma nova seguradora

1. Crie uma nova classe de extrator em `extratores/extratores_seguradoras/nova_seguradora.py`
2. Crie uma nova classe de formatador em `formatadores/formatadores_seguradoras/nova_seguradora.py`
3. Registre as novas classes nos dicionários em `extratores/__init__.py` e `formatadores/__init__.py`
4. Adicione o nome da seguradora à lista `SEGURADORAS` em `config/config.py`
5. Adicione o telefone de assistência 24h no dicionário `ASSISTENCIA_24H` em `config/config.py`

## Desenvolvimento futuro

- Adicionar suporte a mais seguradoras (Allianz, Azul, Porto, Tokio, etc.)
- Melhorar a interface web com recursos adicionais
- Implementar extração de informações de pagamento
- Adicionar testes automatizados

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.