function executeCode() {

var selectElement = angular.element(document.querySelector('select[ng-model="ctrl.novo.id_categoria"]')); // Seleciona o elemento <select> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = selectElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.id_categoria = scope.ctrl.categorias[0].id; // Define o valor da opção desejada no modelo usando o índice 0 para "Leves"
});

// Dispare um evento 'change' no elemento <select> para refletir a alteração no UI
selectElement.triggerHandler('change');
var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.de_val"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.de_val = '15.000,00'; // Define o valor desejado no modelo
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.ate_val"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.ate_val = '15.000,00'; // Define o valor desejado no modelo
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.cota"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.cota = '2.0'; // Define o valor desejado no modelo
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.adesao"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.adesao = '72'; // Define o valor desejado no modelo
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.val_mensal"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.val_mensal = '100'; // Define o valor desejado no modelo
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.participacao"]')); // Seleciona o elemento <input> usando o atributo 'ng-model' e o encapsula com angular.element()
var scope = inputElement.scope(); // Obtém o escopo do elemento
scope.$apply(function() {
  scope.ctrl.novo.participacao = '6% da Tabela FIPE'; // Define o valor desejado no modelo
});

var submitButton = document.querySelectorAll('.btn.btn-info')[1]; // Seleciona o segundo botão com a classe 'btn btn-info'
submitButton.click(); // Aciona o evento de clique no botão

}

// Chama a função para executar o código inicialmente
executeCode();

// Depois, você pode chamar a função novamente quando quiser que o código seja executado novamente
// Por exemplo, após algum evento específico ou em um intervalo de tempo
setInterval(executeCode, 5000); // Executa o código a cada 5 segundos (5000 milissegundos)