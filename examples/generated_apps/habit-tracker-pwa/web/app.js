const STORAGE_KEY = "mobile-habit-tracker-state-v1";
const habitForm = document.getElementById("habit-form");
const habitNameInput = document.getElementById("habit-name");
const habitList = document.getElementById("habit-list");
const completedCount = document.getElementById("completed-count");
const bestStreak = document.getElementById("best-streak");
const todayLabel = document.getElementById("today-label");
const template = document.getElementById("habit-item-template");
const installButton = document.getElementById("install-button");

let deferredInstallPrompt = null;

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function formatToday() {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  }).format(new Date());
}

function readState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : null;
    if (!parsed || !Array.isArray(parsed.habits)) {
      return { habits: [] };
    }
    return parsed;
  } catch (error) {
    return { habits: [] };
  }
}

function writeState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function streakFromDates(entries) {
  const unique = [...new Set(entries)].sort().reverse();
  let streak = 0;
  const cursor = new Date();
  cursor.setHours(0, 0, 0, 0);

  for (const entry of unique) {
    const key = cursor.toISOString().slice(0, 10);
    if (entry !== key) {
      break;
    }
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }

  return streak;
}

function bestStreakFromDates(entries) {
  const unique = [...new Set(entries)].sort();
  if (!unique.length) {
    return 0;
  }

  let best = 1;
  let current = 1;

  for (let index = 1; index < unique.length; index += 1) {
    const previous = new Date(unique[index - 1]);
    const currentDate = new Date(unique[index]);
    const diff = Math.round((currentDate - previous) / 86400000);
    if (diff === 1) {
      current += 1;
      best = Math.max(best, current);
    } else {
      current = 1;
    }
  }

  return best;
}

function render() {
  const state = readState();
  const today = todayKey();
  todayLabel.textContent = formatToday();
  habitList.innerHTML = "";

  if (!state.habits.length) {
    const empty = document.createElement("li");
    empty.className = "habit-item";
    empty.innerHTML = `
      <div class="habit-copy">
        <p class="habit-name">아직 습관이 없습니다</p>
        <p class="habit-meta">작은 일상 습관 하나를 추가하고 홈 화면에서 바로 체크하세요.</p>
      </div>
    `;
    habitList.appendChild(empty);
  }

  let completedToday = 0;
  let best = 0;

  state.habits.forEach((habit) => {
    const fragment = template.content.cloneNode(true);
    const item = fragment.querySelector(".habit-item");
    const name = fragment.querySelector(".habit-name");
    const meta = fragment.querySelector(".habit-meta");
    const checkButton = fragment.querySelector(".check-button");
    const deleteButton = fragment.querySelector(".delete-button");
    const checkedToday = habit.completed_dates.includes(today);
    const streak = streakFromDates(habit.completed_dates);
    const personalBest = bestStreakFromDates(habit.completed_dates);

    best = Math.max(best, personalBest);
    if (checkedToday) {
      completedToday += 1;
      checkButton.classList.add("is-complete");
      checkButton.textContent = "오늘 완료";
    }

    name.textContent = habit.name;
    meta.textContent = `현재 ${streak}일 연속 · 최고 ${personalBest}일`;

    checkButton.addEventListener("click", () => {
      const nextState = readState();
      const target = nextState.habits.find((entry) => entry.id === habit.id);
      if (!target) {
        return;
      }

      if (target.completed_dates.includes(today)) {
        target.completed_dates = target.completed_dates.filter((entry) => entry !== today);
      } else {
        target.completed_dates.push(today);
      }

      writeState(nextState);
      render();
    });

    deleteButton.addEventListener("click", () => {
      const nextState = readState();
      nextState.habits = nextState.habits.filter((entry) => entry.id !== habit.id);
      writeState(nextState);
      render();
    });

    item.dataset.habitId = habit.id;
    habitList.appendChild(fragment);
  });

  completedCount.textContent = String(completedToday);
  bestStreak.textContent = String(best);
}

habitForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const value = habitNameInput.value.trim();
  if (!value) {
    return;
  }

  const state = readState();
  state.habits.unshift({
    id: crypto.randomUUID(),
    name: value,
    completed_dates: [],
  });
  writeState(state);
  habitNameInput.value = "";
  render();
});

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", async () => {
  if (!deferredInstallPrompt) {
    return;
  }

  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  installButton.hidden = true;
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").catch(() => {});
  });
}

render();
