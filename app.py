from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def ler_estoque():
    with open('estoque.json', 'r') as f:
        return json.load(f)

def salvar_estoque(estoque):
    with open('estoque.json', 'w') as f:
        json.dump(estoque, f, indent=2)

@app.route('/estoque', methods=['GET'])
def listar_estoque():
    estoque = ler_estoque()
    return jsonify(estoque)

@app.route('/estoque', methods=['POST'])
def adicionar_produto():
    novo_produto = request.json
    estoque = ler_estoque()
    novo_produto['id'] = len(estoque) + 1
    estoque.append(novo_produto)
    salvar_estoque(estoque)
    return jsonify(novo_produto), 201

@app.route('/estoque/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    dados = request.json
    estoque = ler_estoque()
    for produto in estoque:
        if produto['id'] == produto_id:
            produto.update(dados)
            salvar_estoque(estoque)
            return jsonify(produto)
    return jsonify({'erro': 'Produto não encontrado'}), 404

@app.route('/estoque/<int:produto_id>', methods=['DELETE'])
def remover_produto(produto_id):
    estoque = ler_estoque()
    estoque = [p for p in estoque if p['id'] != produto_id]
    salvar_estoque(estoque)
    return jsonify({'mensagem': 'Produto removido'})

if __name__ == '__main__':
    app.run(debug=True)