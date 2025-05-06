#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface web simples para o processador de cotações de seguro.
"""

import os
import tempfile
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from modelos.informacoes_seguro import InformacoesSeguro
from utils.helpers import identificar_seguradora
from extratores import obter_extrator
from formatadores import obter_formatador

# Configuração da aplicação Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'seguros_auto_uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB para uploads
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Certifica-se de que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    """Página inicial da aplicação."""
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'arquivo' not in request.files:
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        
        arquivo = request.files['arquivo']
        
        # Se o usuário não selecionar um arquivo
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        
        # Se o arquivo for válido, processamos
        if arquivo and allowed_file(arquivo.filename):
            # Salva o arquivo temporariamente
            filename = secure_filename(arquivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(filepath)
            
            # Processa o arquivo
            try:
                # Identifica a seguradora
                seguradora = identificar_seguradora(filepath)
                if not seguradora:
                    flash('Não foi possível identificar a seguradora neste arquivo', 'error')
                    return redirect(request.url)
                
                # Obtém o extrator e o formatador para a seguradora
                extrator = obter_extrator(seguradora)
                formatador = obter_formatador(seguradora)
                
                if not extrator or not formatador:
                    flash(f'Seguradora {seguradora} não suportada', 'error')
                    return redirect(request.url)
                
                # Cria um objeto para armazenar as informações
                informacoes = InformacoesSeguro()
                
                # Extrai o texto completo do PDF
                texto_completo = extrator.extrair_texto_completo(filepath)
                
                # Extrai as informações do seguro
                informacoes = extrator.extrair_informacoes(texto_completo, informacoes)
                
                # Tenta extrair informações de pagamento
                try:
                    informacoes.pagamento = extrator.extrair_informacoes_pagamento(filepath)
                except Exception as e:
                    app.logger.warning(f"Não foi possível extrair informações de pagamento: {e}")
                
                # Formata o textinho para WhatsApp
                textinho = formatador.formatar_textinho(informacoes)
                
                # Armazena o resultado na sessão
                session['textinho'] = textinho
                session['seguradora'] = seguradora
                
                return redirect(url_for('resultado'))
                
            except Exception as e:
                flash(f'Erro ao processar o arquivo: {str(e)}', 'error')
                return redirect(request.url)
            finally:
                # Remove o arquivo temporário
                try:
                    os.remove(filepath)
                except:
                    pass
        else:
            flash('Formato de arquivo não permitido. Apenas PDFs são aceitos.', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    """Página de resultado."""
    textinho = session.get('textinho', None)
    seguradora = session.get('seguradora', None)
    
    if not textinho:
        flash('Nenhum resultado disponível', 'error')
        return redirect(url_for('index'))
    
    return render_template('resultado.html', textinho=textinho, seguradora=seguradora)

if __name__ == '__main__':
    app.run(debug=True)