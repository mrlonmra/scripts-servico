function executeCode() {

var categoria = prompt("Digite a categoria desejada:");

var selectElement = angular.element(document.querySelector('select[ng-model="ctrl.novo.id_categoria"]'));
var selectScope = selectElement.scope();
selectScope.$apply(function() {
  var categorias = selectScope.ctrl.categorias;
  for (var i = 0; i < categorias.length; i++) {
    if (categorias[i].nome === categoria) {
      selectScope.ctrl.novo.id_categoria = categorias[i].id;
      break;
    }
  }
});
var deVal = prompt("Digite o valor para 'de_val':");
var ateVal = prompt("Digite o valor para 'ate_val':");
var cota = prompt("Digite o valor para 'cota':");
var adesao = prompt("Digite o valor para 'adesao':");
var valMensal = prompt("Digite o valor para 'val_mensal':");
var participacao = prompt("Digite o valor para 'participacao':");

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.de_val"]'));
var deValScope = inputElement.scope();
deValScope.$apply(function() {
  deValScope.ctrl.novo.de_val = deVal;
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.ate_val"]'));
var ateValScope = inputElement.scope();
ateValScope.$apply(function() {
  ateValScope.ctrl.novo.ate_val = ateVal;
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.cota"]'));
var cotaScope = inputElement.scope();
cotaScope.$apply(function() {
  cotaScope.ctrl.novo.cota = cota;
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.adesao"]'));
var adesaoScope = inputElement.scope();
adesaoScope.$apply(function() {
  adesaoScope.ctrl.novo.adesao = adesao;
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.val_mensal"]'));
var valMensalScope = inputElement.scope();
valMensalScope.$apply(function() {
  valMensalScope.ctrl.novo.val_mensal = valMensal;
});

var inputElement = angular.element(document.querySelector('input[ng-model="ctrl.novo.participacao"]'));
var participacaoScope = inputElement.scope();
participacaoScope.$apply(function() {
  participacaoScope.ctrl.novo.participacao = participacao;
});

var submitButton = document.querySelectorAll('.btn.btn-info')[1];
submitButton.click();


}

// Chama a função para executar o código inicialmente
executeCode();

// Depois, você pode chamar a função novamente quando quiser que o código seja executado novamente
// Por exemplo, após algum evento específico ou em um intervalo de tempo
setInterval(executeCode, 5000); // Executa o código a cada 5 segundos (5000 milissegundos)