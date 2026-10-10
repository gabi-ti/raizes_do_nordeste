from flask import Flask, jsonify, request
from flask_cors import CORS

from conexao import conectar_banco

app = Flask(__name__)
CORS(app)


@app.route("/")
def inicio():
    return "API Raízes do Nordeste funcionando!"


@app.route("/unidade")
def listar_unidades():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT AutoID, Nome, Cidade, Estado, Activa
        FROM Unidade
    """)

    unidades = []

    for unidade in cursor.fetchall():
        unidades.append({
            "id": unidade.AutoID,
            "nome": unidade.Nome,
            "cidade": unidade.Cidade,
            "estado": unidade.Estado,
            "activa": unidade.Activa
        })

    cursor.close()
    conexao.close()

    return jsonify(unidades)

@app.route("/produto")
def listar_produtos():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    id_unidade = request.args.get("unidade")

    if id_unidade:

        cursor.execute("""
            SELECT
                AutoID,
                IdUnidade,
                Nome,
                Ingredientes,
                Preco,
                Disponivel,
                Imagem
            FROM Produto
            WHERE IdUnidade = ?
        """, (id_unidade,))

    else:

        cursor.execute("""
            SELECT
                AutoID,
                IdUnidade,
                Nome,
                Ingredientes,
                Preco,
                Disponivel,
                Imagem
            FROM Produto
        """)

    produtos = []

    for produto in cursor.fetchall():

        produtos.append({
            "id": produto.AutoID,
            "id_unidade": produto.IdUnidade,
            "nome": produto.Nome,
            "ingredientes": produto.Ingredientes,
            "preco": float(produto.Preco),
            "disponivel": bool(produto.Disponivel),
            "imagem": produto.Imagem
        })

    cursor.close()
    conexao.close()

    return jsonify(produtos)

##RECEBEIMENTO DE PEDIDOS.
@app.route("/pedido", methods=["POST"])
def criar_pedido():
    dados = request.get_json()

    campos_obrigatorios = [
        "id_usuario",
        "id_unidade",
        "status",
        "valor_total"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} é obrigatório."
            }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verifica se o usuário existe
    cursor.execute("""
        SELECT AutoID
        FROM Usuario
        WHERE AutoID = ?
    """, (dados["id_usuario"],))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()

        return jsonify({
            "erro": "O usuário informado não existe."
        }), 400

    # Verifica se a unidade existe
    cursor.execute("""
        SELECT AutoID
        FROM Unidade
        WHERE AutoID = ?
    """, (dados["id_unidade"],))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()

        return jsonify({
            "erro": "A unidade informada não existe."
        }), 400

    # Cria o pedido
    cursor.execute("""
        INSERT INTO Pedido
            (IdUsuario, IdUnidade, Status, ValorTotal)
        OUTPUT INSERTED.AutoID
        VALUES (?, ?, ?, ?)
    """, (
        dados["id_usuario"],
        dados["id_unidade"],
        dados["status"],
        dados["valor_total"]
    ))

    id_pedido = cursor.fetchone()[0]

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Pedido criado com sucesso!",
        "id_pedido": id_pedido
    }), 201

@app.route("/item-pedido")
def listar_itens_pedido():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT AutoID, IdPedido, IdProduto, Quantidade, PrecoUnitario
        FROM ItemPedido
    """)

    itens = []

    for item in cursor.fetchall():
        itens.append({
            "id": item.AutoID,
            "id_pedido": item.IdPedido,
            "id_produto": item.IdProduto,
            "quantidade": item.Quantidade,
            "preco_unitario": float(item.PrecoUnitario)
        })

    cursor.close()
    conexao.close()

    return jsonify(itens)

## 2 - ITEM - PEDIDO

@app.route("/item-pedido", methods=["POST"])
def criar_item_pedido():
    dados = request.get_json()

    campos_obrigatorios = [
        "id_pedido",
        "id_produto",
        "quantidade",
        "preco_unitario"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} é obrigatório."
            }), 400
        
    if dados["quantidade"] <= 0:
        return jsonify({
             "erro": "A quantidade deve ser maior que zero."
    }), 400

    if dados["preco_unitario"] <= 0:
        return jsonify({
        "erro": "O preço deve ser maior que zero."
    }), 400
        
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verifica se o pedido existe
    cursor.execute("""
    SELECT AutoID
    FROM Pedido
    WHERE AutoID = ?
""", (dados["id_pedido"],))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()

        return jsonify({
            "erro": "O pedido informado não existe."
    }), 400

        # Verifica se o produto existe
    cursor.execute("""
        SELECT AutoID
        FROM Produto
        WHERE AutoID = ?
""", (dados["id_produto"],))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()

        return jsonify({
            "erro": "O produto informado não existe."
        }), 400

    cursor.execute("""
        INSERT INTO ItemPedido
            (IdPedido, IdProduto, Quantidade, PrecoUnitario)
        OUTPUT INSERTED.AutoID
        VALUES (?, ?, ?, ?)
    """, (
        dados["id_pedido"],
        dados["id_produto"],
        dados["quantidade"],
        dados["preco_unitario"]
    ))

    id_item = cursor.fetchone()[0]

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Item do pedido criado com sucesso!",
        "id_item": id_item
    }), 201

if __name__ == "__main__":
    app.run(debug=True)