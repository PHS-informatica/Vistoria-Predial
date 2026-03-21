import requests
import base64
import json  # <--- Adicione este se não houver
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from datetime import datetime
import pytz # Se não tiver instalado, rode: pip install pytz
import os

# 1. INICIALIZAÇÃO (Sempre no topo)
app = Flask(__name__)
app.secret_key = 'vistoria_key_2026' # Agora o app existe, podemos dar a chave

# --- CONFIGURAÇÕES ORACLE ---
# Gaveta das Vistorias
ORDS_URL = "https://g4ee096b668ea70-vistoriadb.adb.sa-vinhedo-1.oraclecloudapps.com/ords/admin/soda/latest/VISTORIAS_JSON"

# Gaveta dos Usuários (Nova coleção que você criou)
USUARIOS_URL = "https://g4ee096b668ea70-vistoriadb.adb.sa-vinhedo-1.oraclecloudapps.com/ords/admin/soda/latest/USUARIOS_JSON"

# Credenciais de Acesso (Não mudam)
USUARIO = os.environ.get('ORACLE_USER') 
SENHA = os.environ.get('ORACLE_PASS')

# 2. FUNÇÕES AUXILIARES
def upload_imgbb(file):
    api_key = "202ff1bcc9198a37ec87b4020d309899"
    file.seek(0) 
    img_base64 = base64.b64encode(file.read()).decode('utf-8')
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key, "image": img_base64}
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()['data']['url']
    return None

# 3. ROTAS DE ACESSO (LOGIN/LOGOUT)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        # Filtro: Procuramos o documento onde o campo "usuario" seja igual ao digitado
        filtro = {"usuario": user_input}
        
        try:
            # Fazemos o GET passando o filtro na URL (?q=...)
            resposta = requests.get(f"{USUARIOS_URL}?q={json.dumps(filtro)}", auth=(USUARIO, SENHA))
            
            if resposta.status_code == 200:
                dados = resposta.json()
                
                # Se a lista 'items' não estiver vazia, o usuário existe
                if dados.get('items'):
                    # O SODA retorna o conteúdo dentro de ['value']
                    user_data = dados['items'][0]['value']
                    
                    # Verificamos a senha (lembrando que no seu JSON a senha é "123")
                    if str(user_data['senha']) == str(senha_input):
                        session['usuario_logado'] = user_data['nome'] # Aqui pegamos o Nome Real (ex: "Paulo Henrique")
                        session['perfil'] = user_data['perfil']
                        return redirect(url_for('index'))
                
                # Se cair aqui, ou o usuário não existe ou a senha está errada
                return render_template('login.html', erro='Usuário ou senha inválidos')
            
            return f"Erro no Banco: {resposta.status_code}"
            
        except Exception as e:
            return f"Erro de Conexão: {str(e)}"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

# 4. ROTAS DO SISTEMA
@app.route('/')
def index():
    # Proteção: Se não estiver logado, vai para o login
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session: return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        # --- LÓGICA DE FUSO HORÁRIO BRASÍLIA ---
        fuso_br = pytz.timezone('America/Sao_Paulo')
        agora_br = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')
        # ---------------------------------------
        fotos = request.files.getlist('foto_principal')
        links_fotos = []
        for foto in fotos:
            if foto and foto.filename != '':
                url_gerada = upload_imgbb(foto)
                if url_gerada: links_fotos.append(url_gerada)

        if not links_fotos:
            links_fotos = ["https://via.placeholder.com/150"]

        nova_vistoria = {
            "nome_predio": request.form.get('nome_predio'),
            "vistoriador": request.form.get('vistoriador'),
            "endereco": request.form.get('endereco'),
            "data_vistoria": request.form.get('data_vistoria'),
            "proxima_vistoria": request.form.get('proxima_vistoria'),
            "alvara_vencimento": request.form.get('alvara_vencimento'),
            "pintura": request.form.get('pintura'),
            "fachada": request.form.get('fachada'),
            "piso": request.form.get('piso'),
            "eletrica": request.form.get('eletrica'),
            "hidraulica": request.form.get('hidraulica'),
            "cobertura": request.form.get('cobertura'),
            "itens_seguranca": request.form.get('itens_seguranca'),
            "sistema_ventilacao": request.form.get('sistema_ventilacao'),
            "laudo_estrutural": request.form.get('laudo_estrutural'),
            "observacao": request.form.get('observacao'),
            "url_fotos": links_fotos 
        }

        resposta = requests.post(ORDS_URL, json=nova_vistoria, auth=(USUARIO, SENHA))
        if resposta.status_code in [200, 201]:
            return redirect(url_for('relatorio'))
        return f"Erro na Oracle: {resposta.status_code}"
    except Exception as e:
        return f"Erro ao salvar: {str(e)}"

@app.route('/relatorio')
def relatorio():
    if 'usuario_logado' not in session: return redirect(url_for('login'))
    try:
        resposta = requests.get(ORDS_URL, auth=(USUARIO, SENHA))
        if resposta.status_code == 200:
            dados = resposta.json()
            return render_template('relatorio.html', vistorias=dados['items'])
        return f"Erro na Oracle: {resposta.status_code}"
    except Exception as e:
        return f"Erro: {str(e)}"

@app.route('/excluir/<key>', methods=['POST'])
def excluir(key):
    try:
        url_delete = f"{ORDS_URL}/{key}"
        resposta = requests.delete(url_delete, auth=(USUARIO, SENHA))
        return (jsonify({"status": "sucesso"}), 200) if resposta.status_code in [200, 204] else (jsonify({"status": "erro"}), 400)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/editar/<id>')
def editar(id):
    if 'usuario_logado' not in session: return redirect(url_for('login'))
    try:
        url_get = f"{ORDS_URL}/{id}"
        resposta = requests.get(url_get, auth=(USUARIO, SENHA))
        if resposta.status_code == 200:
            item = resposta.json()
            dados_finais = item.get('value') if 'value' in item else item
            return render_template('cadastro.html', dados=dados_finais, id=id, modo="edicao")
        return "Não encontrado", 404
    except Exception as e:
        return str(e), 500

@app.route('/salvar_edicao/<id>', methods=['POST'])
def salvar_edicao(id):
    try:
        links_fotos = []
        novas_fotos = request.files.getlist('foto_principal')
        for foto in novas_fotos:
            if foto and foto.filename != '':
                url_gerada = upload_imgbb(foto)
                if url_gerada: links_fotos.append(url_gerada)

        if not links_fotos:
            links_fotos = ["https://via.placeholder.com/150"]

        dados_atualizados = {
            "nome_predio": request.form.get('nome_predio'),
            "vistoriador": request.form.get('vistoriador'),
            "endereco": request.form.get('endereco'),
            "data_vistoria": request.form.get('data_vistoria'),
            "proxima_vistoria": request.form.get('proxima_vistoria'),
            "alvara_vencimento": request.form.get('alvara_vencimento'),
            "pintura": request.form.get('pintura'),
            "fachada": request.form.get('fachada'),
            "piso": request.form.get('piso'),
            "eletrica": request.form.get('eletrica'),
            "hidraulica": request.form.get('hidraulica'),
            "cobertura": request.form.get('cobertura'),
            "itens_seguranca": request.form.get('itens_seguranca'),
            "sistema_ventilacao": request.form.get('sistema_ventilacao'),
            "laudo_estrutural": request.form.get('laudo_estrutural'),
            "observacao": request.form.get('observacao'),
            "url_fotos": links_fotos
        }

        url_put = f"{ORDS_URL}/{id}"
        resposta = requests.put(url_put, json=dados_atualizados, auth=(USUARIO, SENHA))
        return redirect(url_for('relatorio')) if resposta.status_code in [200, 204] else f"Erro: {resposta.status_code}"
    except Exception as e:
        return str(e)

# 5. EXECUÇÃO
if __name__ == '__main__':
    app.run(debug=True)