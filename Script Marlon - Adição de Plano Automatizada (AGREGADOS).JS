// Define um array de objetos chamado 'dados'
const dados = [
  {
    "de_val": 0.01,
    "ate_val": 20000,
    "cota": "0.7",
    "val_mensal": 350,
    "participacao": "6% nao sendo inferior a R$900.00"
  },
  {
    "de_val": 20001,
    "ate_val": 30000,
    "cota": "1.5",
    "val_mensal": 350,
    "participacao": "6% nao sendo inferior a R$900.00"
  },
  {
    "de_val": 30001,
    "ate_val": 40000,
    "cota": "2.3",
    "val_mensal": 350,
    "participacao": "6% nao sendo inferior a R$900.00"
  }
];

// Itera sobre os elementos do array 'dados'
dados.forEach((currentdados) => {
  // Itera sobre as chaves e valores de cada objeto em 'dados'
  Object.entries(currentdados).forEach(([key, value]) => {
    // Seleciona o elemento <input> com o atributo 'ng-model' igual a 'ctrl.novo.<key>'
    const inputElement = document.querySelector(input[ng-model="ctrl.novo.${key}"]);

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