const btnCadastro = document.getElementById("btnCadastro");
const btnPonto = document.getElementById("btnPonto");
const container = document.getElementById("container");
const btnCadastrarAluno = document.getElementById("btnCadastrarAluno");
const bater_ponto = document.getElementById("bater_ponto");

btnCadastro.addEventListener("click", () => {
  console.log("voce clicoui aquii");

  container.classList.add("ativaMudanca");
});

btnPonto.addEventListener("click", () => {
  console.log("voce clicou");
  container.classList.remove("ativaMudanca");
});

btnCadastrarAluno.addEventListener("click", () => {
  console.log("Voce foi cadastrado, nao esqueca de bater o ");
  container.classList.remove("ativaMudanca");
});

// aqui ainda e so teste pode tirar e so pra ver se o botao esta funcionando e tals

bater_ponto.addEventListener("click", () => {
  alert("Seu ponto foi registrado com sucesso!");
});




// Seleciona o item de "Relatórios" e os itens adicionais
const toggleRelatorios = document.getElementById('toggleRelatorios');
const relatorioItems = document.getElementById('relatorioItems');

// Adiciona o evento de clique
toggleRelatorios.addEventListener('click', () => {
    // Alterna a visibilidade dos itens
    relatorioItems.classList.toggle('hidden');
});
