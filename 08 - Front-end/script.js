
//================================CARREGAR UNIDADES================================//


const listaUnidades = document.getElementById("listaUnidades");

if (listaUnidades) {

    fetch("http://127.0.0.1:5000/unidade")
        .then(response => response.json())
        .then(unidades => {

            listaUnidades.innerHTML = "";

            unidades.forEach(unidade => {

                const botao = document.createElement("button");

                botao.classList.add("unidade");

                botao.textContent =
                    `${unidade.nome} - ${unidade.cidade}/${unidade.estado}`;

                botao.onclick = function () {

                    localStorage.setItem(
                        "unidadeSelecionada",
                        JSON.stringify(unidade)
                    );

                    window.location.href = "cardapio.html";
                };

                listaUnidades.appendChild(botao);
            });

        })
        .catch(erro => {

            console.error("Erro ao carregar unidades:", erro);

            listaUnidades.innerHTML =
                "<p>Não foi possível carregar as unidades.</p>";
        });
}



// ================================CARREGAR CARDÁPIO================================//

const listaProdutos = document.getElementById("listaProdutos");
const unidadeEscolhida = document.getElementById("unidadeEscolhida");

if (listaProdutos) {

    const unidadeSalva =
        localStorage.getItem("unidadeSelecionada");

    if (!unidadeSalva) {

        unidadeEscolhida.textContent =
            "Nenhuma unidade foi selecionada.";

        listaProdutos.innerHTML =
            "<p>Selecione uma unidade para visualizar o cardápio.</p>";

    } else {

        const unidade = JSON.parse(unidadeSalva);

        unidadeEscolhida.textContent =
            `${unidade.nome} - ${unidade.cidade}/${unidade.estado}`;

        fetch(
            `http://127.0.0.1:5000/produto?unidade=${unidade.id}`
        )
            .then(response => response.json())
            .then(produtos => {

                listaProdutos.innerHTML = "";

                if (produtos.length === 0) {

                    listaProdutos.innerHTML =
                        "<p>Nenhum produto disponível nesta unidade.</p>";

                    return;
                }

                produtos.forEach(produto => {

    const card = document.createElement("div");

    card.classList.add("produto");

    let acaoProduto;

    if (produto.disponivel) {

        acaoProduto = `
            <button class="btn-adicionar" data-id="${produto.id}">
                Adicionar
            </button>
        `;

    } else {

        acaoProduto = `
            <span class="indisponivel">
                Indisponível
            </span>
        `;
    }

    card.innerHTML = `
        <img
            src="Imagens_Cardapio/Produtos/${produto.imagem}"
            alt="${produto.nome}"
        >

        <h3>${produto.nome}</h3>

        <p>${produto.ingredientes || ""}</p>

        <strong>
            R$ ${produto.preco.toFixed(2).replace(".", ",")}
        </strong>

        ${acaoProduto}
    `;

    listaProdutos.appendChild(card);

    if (produto.disponivel) {

    const botaoAdicionar =
        card.querySelector(".btn-adicionar");

    botaoAdicionar.addEventListener("click", function () {

        let pedido =
            JSON.parse(localStorage.getItem("pedidoAtual")) || [];

        const produtoExistente =
            pedido.find(item => item.id === produto.id);

        if (produtoExistente) {

            produtoExistente.quantidade++;

        } else {

            pedido.push({
                id: produto.id,
                nome: produto.nome,
                preco: produto.preco,
                quantidade: 1
            });
        }

        localStorage.setItem(
            "pedidoAtual",
            JSON.stringify(pedido)
        );

        window.location.href = "pedido.html";
    });
}
});
            })
            .catch(erro => {

                console.error(
                    "Erro ao carregar produtos:",
                    erro
                );

                listaProdutos.innerHTML =
                    "<p>Não foi possível carregar o cardápio.</p>";


//================================CARREGAR PEDIDO================================//


const listaPedido = document.getElementById("listaPedido");
const totalPedido = document.getElementById("totalPedido");

if (listaPedido) {

    const pedido =
        JSON.parse(localStorage.getItem("pedidoAtual")) || [];

    if (pedido.length === 0) {

        listaPedido.innerHTML =
            "<p>Seu pedido está vazio.</p>";

        totalPedido.innerHTML = "";

    } else {

        listaPedido.innerHTML = "";

        let total = 0;

        pedido.forEach(item => {

            const subtotal =
                item.preco * item.quantidade;

            total += subtotal;

            const produtoPedido =
                document.createElement("div");

            produtoPedido.classList.add("item-pedido");

            produtoPedido.innerHTML = `
                <h3>${item.nome}</h3>

                <p>
                    Quantidade: ${item.quantidade}
                </p>

                <strong>
                    R$ ${subtotal.toFixed(2).replace(".", ",")}
                </strong>
            `;

            listaPedido.appendChild(produtoPedido);
        });

        totalPedido.innerHTML = `
            <strong>
                Total: R$ ${total.toFixed(2).replace(".", ",")}
            </strong>
        `;
    }
}                    
  
            });
    }
}