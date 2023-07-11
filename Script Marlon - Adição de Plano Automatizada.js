// Define um array de objetos chamado 'dados'
const dados = [
  {
    de_val: 0.01,
    ate_val: 26000,
    cota: 1,
    adesao: 800,
    val_mensal: 304.06,
    participacao: "5% da tabela FIPE não sendo inferior a R$2.000,00",
  },
];

// Seleciona o elemento <select> com o atributo 'ng-model' igual a 'ctrl.novo.id_categoria'
const selecionarElemento = document.querySelector('select[ng-model="ctrl.novo.id_categoria"]');

// Obtém o escopo associado ao elemento selecionado
const scope = angular.element(selecionarElemento).scope();

// Atualiza o valor do 'id_categoria' no escopo, definindo-o como o primeiro ID da lista 'ctrl.categorias'
scope.$apply(() => {
  scope.ctrl.novo.id_categoria = scope.ctrl.categorias[2].id;
});

// Itera sobre os elementos do array 'dados'
dados.forEach((currentdados) => {
  // Itera sobre as chaves e valores de cada objeto em 'dados'
  Object.entries(currentdados).forEach(([key, value]) => {
    // Seleciona o elemento <input> com o atributo 'ng-model' igual a 'ctrl.novo.<key>'
    const inputElement = document.querySelector(`input[ng-model="ctrl.novo.${key}"]`);

    // Obtém o escopo associado ao elemento selecionado
    const inputScope = angular.element(inputElement).scope();

    // Atualiza o valor do input no escopo, definindo-o como o valor correspondente do objeto 'currentdados'
    inputScope.$apply(() => {
      inputScope.ctrl.novo[key] = value;
    });
  });

  // Seleciona o segundo botão com as classes 'btn' e 'btn-info'
  const submitButton = document.querySelectorAll('.btn.btn-info')[1];

  // Clica no botão de envio
  submitButton.click();
});
