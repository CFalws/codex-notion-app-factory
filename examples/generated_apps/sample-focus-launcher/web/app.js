const form = document.getElementById("launcher-form");
const taskInput = document.getElementById("task");
const resultCard = document.getElementById("result-card");
const resultAction = document.getElementById("result-action");
const historyList = document.getElementById("history-list");

async function loadHistory() {
  const response = await fetch("/api/history");
  const data = await response.json();
  renderHistory(data.history || []);
}

function renderHistory(entries) {
  historyList.innerHTML = "";

  if (!entries.length) {
    const item = document.createElement("li");
    item.className = "empty-state";
    item.textContent = "No launches yet. Type one task and start moving.";
    historyList.appendChild(item);
    return;
  }

  entries.forEach((entry) => {
    const item = document.createElement("li");
    item.className = "history-item";
    item.innerHTML = `
      <p class="history-task">${entry.task}</p>
      <p class="history-action">${entry.first_action}</p>
    `;
    historyList.appendChild(item);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const task = taskInput.value.trim();
  if (!task) {
    return;
  }

  const response = await fetch("/api/launch", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task }),
  });

  const data = await response.json();
  if (!response.ok) {
    return;
  }

  resultAction.textContent = data.first_action;
  resultCard.hidden = false;
  renderHistory(data.history || []);
  taskInput.value = "";
  taskInput.focus();
});

loadHistory().catch(() => {
  renderHistory([]);
});
