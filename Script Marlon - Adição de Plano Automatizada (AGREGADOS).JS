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

// Itera sobre os elementos do array 'dados'
dados.forEach((currentdados) => {
  // Itera sobre as chaves e valores de cada objeto em 'dados'
  Object.entries(currentdados).forEach(([key, value]) => {
    // Seleciona o elemento <input> com o atributo 'ng-model' igual a 'ctrl.novo.<key>'
    const inputElement = document.querySelector(`input[ng-model="ctrl.novo.${key}"]`);

    // Atualiza o valor do input, definindo-o como o valor correspondente do objeto 'currentdados'
    if (inputElement) {
      inputElement.value = value;
      inputElement.dispatchEvent(new Event('input'));
    }
  });

  // Seleciona o segundo botão com as classes 'btn' e 'btn-info'
  const submitButton = document.querySelectorAll('.btn.btn-info')[1];

  // Clica no botão de envio
  if (submitButton) {
    submitButton.click();
  }
});