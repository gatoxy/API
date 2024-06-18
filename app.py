from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Função para encontrar e ler o arquivo JSON
def ler_json():
    nome_arquivo = 'dados.json'
    diretorio_base = os.path.expanduser("~")  # Diretório base, pode ser ajustado conforme necessário
    caminho_arquivo = encontrar_arquivo_json(nome_arquivo, diretorio_base)
    
    if not caminho_arquivo:
        return {"error": "Arquivo JSON não encontrado."}
    
    with open(caminho_arquivo, 'r') as file:
        dados = json.load(file)
    return dados

# Função para encontrar o arquivo JSON
def encontrar_arquivo_json(nome_arquivo, diretorio_base):
    for root, dirs, files in os.walk(diretorio_base):
        if nome_arquivo in files:
            return os.path.join(root, nome_arquivo)
    return None

# Rota padrão para verificar se o servidor está online
@app.route('/')
def home():
    return jsonify(message="Servidor está online!")

# Rota para obter dados do arquivo JSON (GET)
@app.route('/dados', methods=['GET'])
def obter_dados():
    dados = ler_json()
    return jsonify(dados)

# Rota para enviar dados ao arquivo JSON (POST)
@app.route('/dados', methods=['POST'])
def enviar_dados():
    novo_dado = request.get_json()
    dados = ler_json()
    
    # Verifica se o arquivo foi encontrado ou não
    if "error" in dados:
        return jsonify(dados), 404
    
    dados['usuarios'].append(novo_dado)
    
    nome_arquivo = 'dados.json'
    diretorio_base = os.path.expanduser("~")
    caminho_arquivo = encontrar_arquivo_json(nome_arquivo, diretorio_base)
    
    with open(caminho_arquivo, 'w') as file:
        json.dump(dados, file, indent=4)
    return jsonify(dados), 201

if __name__ == '__main__':
    app.run(debug=True)