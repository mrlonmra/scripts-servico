// Defina a função para obter os dados da tabela
function obterDadosTabela() {
    // Obtenha o elemento do corpo da tabela
    const corpoTabela = document.querySelector('tbody');

    // Verifique se o corpo da tabela existe
    if (!corpoTabela) {
        console.log('Corpo da tabela não encontrado.');
        return;
    }

    // Crie um array para armazenar os dados da tabela
    const dadosTabela = [];

    // Percorra cada linha da tabela
    for (let i = 0; i < corpoTabela.children.length; i++) {
        const linha = corpoTabela.children[i];
        const dadosLinha = {};

        // Obtenha os dados de colunas específicas na linha
        dadosLinha.grupo_item = linha.children[2].innerText;
        dadosLinha.de = linha.children[3].innerText;
        dadosLinha.ate = linha.children[4].innerText;
        dadosLinha.cota = linha.children[5].innerText;
        dadosLinha.taxa_adm = linha.children[6].innerText;
        dadosLinha.adesao = linha.children[7].innerText;
        dadosLinha.mensalidade = linha.children[8].innerText;
        dadosLinha.campo_simples = linha.children[9].innerText;

        // Adicione os dados da linha ao array de dados da tabela
        dadosTabela.push(dadosLinha);
    }

    // Solicite ao usuário o tipo de saída desejada
    const tipoSaida = prompt("1 - imprimir na tela, 2 - Para imprimir JSON e 3 - Para imprimir em formato de tabela");

    // Realize a saída de acordo com o tipo selecionado
    if (tipoSaida === "1") {
        console.log(dadosTabela);
    } else if (tipoSaida === "2") {
        console.log(JSON.stringify(dadosTabela));
    } else if (tipoSaida === "3") {
        console.table(dadosTabela);
    } else {
        console.log('Valor informado é inválido!');
    }
}

// Chame a função para obter os dados da tabela
obterDadosTabela();