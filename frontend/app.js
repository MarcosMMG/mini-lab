const button = document.getElementById("load-projects-btn");
const statusBox = document.getElementById("status-box");
const projectList = document.getElementById("project-list");

async function loadProjects() {
  statusBox.textContent = "Carregando dados da API...";
  projectList.innerHTML = "";

  try {
    const response = await fetch("http://localhost:8000/projects");
    const data = await response.json();
    const projects = data.projects;

    if (!projects || projects.length === 0) {
      statusBox.textContent = "Nenhum projeto foi encontrado.";
      return;
    }

    statusBox.textContent = `Foram carregados ${projects.length} projetos.`;

    projects.forEach((project) => {
      const item = document.createElement("li");
      item.textContent = `${project.name} - ${project.category} - ${project.status}`;
      projectList.appendChild(item);
    });
  } catch (error) {
    statusBox.textContent =
      "Erro ao acessar a API. Verifique se os containers estao ativos.";
    console.error(error);
  }
}

button.addEventListener("click", loadProjects);
