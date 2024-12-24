from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import os
import random
import qrcode
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Caminhos dos arquivos
arquivo_pontos = 'pontos.txt'
arquivo_nomes = 'nomes.txt'
senha_administrador = 'admin123'

# Criar diretório de QR Codes, se não existir
os.makedirs('qrcodes', exist_ok=True)

def gerar_qrcode(codigo):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(codigo)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'qrcodes/{codigo}.png')

def salvar_nome(nome_completo, senha):
    codigo = str(random.randint(100000, 999999))
    with open(arquivo_nomes, 'a') as f:
        f.write(f'{nome_completo},{senha},{codigo}\n')
    gerar_qrcode(codigo)
    return codigo

def obter_pontos_ultimas_horas(horas=2):
    agora = datetime.now()
    limite = agora - timedelta(hours=horas)
    pontos_recents = []

    try:
        with open(arquivo_pontos, 'r') as f:
            for linha in f:
                try:
                    nome, acao, data_str = linha.strip().split(',')
                    data = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
                    if data > limite:
                        pontos_recents.append((data, nome, acao))
                except ValueError:
                    # Ignorar linhas que não estão no formato esperado
                    continue
    except FileNotFoundError:
        pass

    return pontos_recents

def verificar_nome(nome):
    try:
        with open(arquivo_nomes, 'r') as f:
            for linha in f:
                nome_cadastrado, _, _ = linha.strip().split(',')
                if nome_cadastrado == nome:
                    return True
    except FileNotFoundError:
        pass

    return False

def salvar_ponto(codigo, senha, acao):
    try:
        with open(arquivo_nomes, 'r') as f:
            for linha in f:
                nome_cadastrado, senha_cadastrada, codigo_cadastrado = linha.strip().split(',')
                if codigo_cadastrado == codigo and senha_cadastrada == senha:
                    with open(arquivo_pontos, 'a') as f_pontos:
                        f_pontos.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")},{codigo},{acao}\n')
                    return 'Ponto registrado com sucesso!'
    except FileNotFoundError:
        pass

    return 'Código ou senha incorretos!'

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = None
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            nome = request.form['nome'].strip()
            senha = request.form['senha'].strip()
            if nome and senha:
                if not verificar_nome(nome):
                    codigo = salvar_nome(nome, senha)
                    mensagem = f'Seu código de acesso é: {codigo}'
                else:
                    mensagem = 'Nome já cadastrado!'
            else:
                mensagem = 'Preencha todos os campos!'

        elif 'bater_ponto' in request.form:
            codigo = request.form['codigo'].strip()
            senha = request.form['senha_bater'].strip()
            acao = request.form['acao']
            if codigo and senha and acao:
                mensagem = salvar_ponto(codigo, senha, acao)
            else:
                mensagem = 'Preencha todos os campos!'
    
    return render_template('index.html', mensagem=mensagem)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        senha = request.form['senha_admin']
        if senha == senha_administrador:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_page'))
        else:
            return render_template('admin.html', erro="Senha incorreta.")
    
    return render_template('admin.html')

def obter_nomes_unicos():
    nomes_unicos = set()
    try:
        with open(arquivo_nomes, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(',')
                if len(partes) == 3:
                    nome, _, matricula = partes
                    nomes_unicos.add((nome, matricula))
    except FileNotFoundError:
        pass
    return list(nomes_unicos)

@app.route('/listar_nomes', methods=['GET'])
def listar_nomes():
    nomes_unicos = obter_nomes_unicos()
    return jsonify(nomes_unicos)

@app.route('/admin_page')
def admin_page():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    
    pontos_ultimas_horas = obter_pontos_ultimas_horas()
    nomes_unicos = obter_nomes_unicos()
    return render_template('page_admin.html', pontos=pontos_ultimas_horas, nomes=nomes_unicos)

@app.route('/baixar_qrcode/<codigo>')
def baixar_qrcode(codigo):
    file_path = f'qrcodes/{codigo}.png'
    return send_file(file_path, as_attachment=True)

@app.route('/processar_qrcode', methods=['POST'])
def processar_qrcode():
    qrcode_data = request.form.get('qrcode_data')
    if qrcode_data:
        mensagem = f"QR Code recebido: {qrcode_data}"
        return render_template('index.html', mensagem=mensagem)
    return render_template('index.html', mensagem="Erro: Nenhum QR Code recebido.")

@app.route('/leitor_qrcode', methods=['GET'])
def leitor_qrcode():
    return render_template('qr_code_camera.html')  # Certifique-se de que o arquivo HTML está no diretório templates

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)