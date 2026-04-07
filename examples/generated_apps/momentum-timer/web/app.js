const form = document.getElementById("momentum-form");
const taskInput = document.getElementById("task");
const resultCard = document.getElementById("result-card");
const resultAction = document.getElementById("result-action");
const timerValue = document.getElementById("timer-value");
const historyList = document.getElementById("history-list");

let timerHandle = null;

function formatSeconds(totalSeconds) {
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function startTimer(totalSeconds) {
  if (timerHandle) {
    clearInterval(timerHandle);
  }

  let remaining = totalSeconds;
  timerValue.textContent = formatSeconds(remaining);

  timerHandle = setInterval(() => {
    remaining -= 1;
    timerValue.textContent = formatSeconds(Math.max(remaining, 0));

    if (remaining <= 0) {
      clearInterval(timerHandle);
      timerHandle = null;
    }
  }, 1000);
}

function renderHistory(entries) {
  historyList.innerHTML = "";

  if (!entries.length) {
    const item = document.createElement("li");
    item.className = "empty-state";
    item.textContent = "No starts yet. Launch one task to build momentum.";
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

async function loadHistory() {
  const response = await fetch("/api/history");
  const data = await response.json();
  renderHistory(data.history || []);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const task = taskInput.value.trim();
  if (!task) {
    return;
  }

  const response = await fetch("/api/launch", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task }),
  });

  const data = await response.json();
  if (!response.ok) {
    return;
  }

  resultAction.textContent = data.first_action;
  resultCard.hidden = false;
  startTimer(data.timer_seconds || 180);
  renderHistory(data.history || []);
  taskInput.value = "";
  taskInput.focus();
});

loadHistory().catch(() => {
  renderHistory([]);
});
