const form = document.getElementById("demand-form");
const loadButton = document.getElementById("load-demands-btn");
const statusBox = document.getElementById("status-box");
const summaryBox = document.getElementById("summary-box");
const demandList = document.getElementById("demand-list");
const API_BASE = "http://localhost:8000";
async function fetchDemands() {
 const response = await fetch(`${API_BASE}/demands`);
 const data = await response.json();
 return data.demands;
}
async function fetchSummary() {
 const response = await fetch(`${API_BASE}/summary`);
 return await response.json();
}
function renderSummary(summary) {
 summaryBox.innerHTML = `
 <strong>Total:</strong> ${summary.total}<br>
 <strong>Pendentes:</strong> ${summary.pending}<br>
 <strong>Em andamento:</strong> ${summary.in_progress}<br>
 <strong>Concluídas:</strong> ${summary.done}
 `;
}
function renderDemands(demands) {
 demandList.innerHTML = "";
 if (!demands || demands.length === 0) {
 demandList.innerHTML = "<li>Nenhuma demanda encontrada.</li>";
 return;
 }
 demands.forEach((demand) => {
 const item = document.createElement("li");
 item.innerHTML = `
 <strong>${demand.title}</strong><br>
 Categoria: ${demand.category}<br>
 Descrição: ${demand.description}<br>
 Status: ${demand.status}<br>
 Responsável: ${demand.owner}<br>
 Data: ${demand.created_at}<br>
 <button onclick="removeDemand(${demand.id})">Excluir</button>
 `;
 demandList.appendChild(item);
 });
}
async function loadAllData() {
  statusBox.textContent = "Carregando demandas...";
  try {
  const demands = await fetchDemands();
  const summary = await fetchSummary();
  renderDemands(demands);
  renderSummary(summary);
  statusBox.textContent = `Foram carregadas ${demands.length} demandas.`;
  } catch (error) {
  statusBox.textContent =
  "Erro ao carregar os dados. Verifique se a API está em execução.";
  console.error(error);
  }
 }
 async function createDemand(event) {
  event.preventDefault();
  const newDemand = {
  title: document.getElementById("title").value,
  category: document.getElementById("category").value,
  description: document.getElementById("description").value,
  status: document.getElementById("status").value,
  owner: document.getElementById("owner").value,
  created_at: document.getElementById("created_at").value,
  };
  try {
  await fetch(`${API_BASE}/demands`, {
  method: "POST",
  headers: {
  "Content-Type": "application/json",
  },
  body: JSON.stringify(newDemand),
  });
  form.reset();
  await loadAllData();
  } catch (error) {
  statusBox.textContent = "Erro ao cadastrar demanda.";
  console.error(error);
  }
 }
 async function removeDemand(id) {
  try {
  await fetch(`${API_BASE}/demands/${id}`, {
  method: "DELETE",
  });
  await loadAllData();
  } catch (error) {
  statusBox.textContent = "Erro ao excluir demanda.";
  console.error(error);
  }
 }
 form.addEventListener("submit", createDemand);
 loadButton.addEventListener("click", loadAllData);